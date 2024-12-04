from apps.bot.config import config
# import asyncpg


class DBManager:
    def __init__(self):
        self.pool = None

    # async def connect(self):
    #     """Connect to the database"""
    #     self.pool = await asyncpg.create_pool(dsn=config.DB_DNS)

    async def disconnect(self):
        """Disconnect from the database"""
        if self.pool is not None:
            await self.pool.close()

    async def fetch(self, query: str, *args):
        """Fetch a list of objects from the database"""
        async with self.pool.acquire() as connection:
            results = await connection.fetch(query, *args)
            return [dict(result) for result in results]

    async def fetch_one(self, query: str, *args):
        """Fetch a single object from the database"""
        async with self.pool.acquire() as connection:
            result = await connection.fetchrow(query, *args)
            return dict(result) if result else None

    async def execute(self, query, *args):
        """Execute a SQL command"""
        async with self.pool.acquire() as connection:
            await connection.execute(query, *args)

    async def create_tables(self):
        """Create database tables"""
        queries = [
            """
            CREATE TABLE IF NOT EXISTS users (
                telegram_id BIGINT PRIMARY KEY,
                language VARCHAR(16),
                phone VARCHAR(32),
                name VARCHAR(255),
                username VARCHAR(255),
                city VARCHAR(255) DEFAULT 'Toshkent'
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS branches (
                branch_id BIGINT PRIMARY KEY,
                name VARCHAR(255),
                address VARCHAR(255),
                city VARCHAR(255) DEFAULT 'Toshkent',
                open_time TIME DEFAULT '10:00',
                close_time TIME DEFAULT '04:45',
                latitude FLOAT,
                longitude FLOAT,
                max_delivery_distance FLOAT DEFAULT 0.0
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS categories (
                category_id SERIAL PRIMARY KEY,
                name VARCHAR(255),
                image VARCHAR(255)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS products (
                product_id BIGINT PRIMARY KEY,
                category_id BIGINT REFERENCES categories(category_id),
                name VARCHAR(255),
                description VARCHAR(255),
                price FLOAT,
                size VARCHAR(32),
                image VARCHAR(255)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS orders (
                order_id SERIAL PRIMARY KEY,
                user_id BIGINT REFERENCES users(telegram_id) ON DELETE CASCADE,
                order_type VARCHAR(255),
                branch_id BIGINT REFERENCES branches(branch_id) ON DELETE CASCADE,
                d_longitude FLOAT NULL,
                d_latitude FLOAT NULL,
                status VARCHAR(255) DEFAULT 'CREATED',
                total_price FLOAT DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS order_items (
                order_item_id SERIAL PRIMARY KEY,
                order_id BIGINT REFERENCES orders(order_id) ON DELETE CASCADE,
                product_id BIGINT REFERENCES products(product_id) ON DELETE CASCADE,
                quantity INT NOT NULL CHECK (quantity > 0)
            );
            """
        ]

        for query in queries:
            await self.execute(query)

        # Create functions and triggers
        await self.create_triggers()

    async def create_triggers(self):
        """Create necessary triggers and functions"""
        queries = [
            """
            CREATE OR REPLACE FUNCTION update_updated_at()
            RETURNS TRIGGER AS $$
            BEGIN
                NEW.updated_at = CURRENT_TIMESTAMP;
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
            """,
            """
            DO $$
            BEGIN
                IF NOT EXISTS (
                    SELECT 1 FROM pg_trigger WHERE tgname = 'set_updated_at_orders'
                ) THEN
                    CREATE TRIGGER set_updated_at_orders
                    BEFORE UPDATE ON orders
                    FOR EACH ROW
                    EXECUTE FUNCTION update_updated_at();
                END IF;
            END;
            $$;
            """,
            """
            DO $$
            BEGIN
                IF NOT EXISTS (
                    SELECT 1 FROM pg_trigger WHERE tgname = 'set_updated_at_order_items'
                ) THEN
                    CREATE TRIGGER set_updated_at_order_items
                    BEFORE UPDATE ON order_items
                    FOR EACH ROW
                    EXECUTE FUNCTION update_updated_at();
                END IF;
            END;
            $$;
            """
        ]

        for query in queries:
            await self.execute(query)

    async def get_user(self, telegram_id):
        """Fetch a user by Telegram ID"""
        query = "SELECT * FROM users WHERE telegram_id = $1"
        return await self.fetch_one(query, telegram_id)

    async def get_branches(self):
        """Fetch branches"""
        query = "SELECT branch_id, name, address, longitude, latitude, max_delivery_distance FROM branches"
        return await self.fetch(query)

    async def get_all_users(self):
        query = "SELECT * FROM users"
        return await self.fetch(query)

    async def create_user(self, *args):
        query = "INSERT INTO users (telegram_id, language, phone, name, username) VALUES ($1, $2, $3, $4, $5)"
        return await self.execute(query, *args)

    async def create_branch(self, *args):
        query = "INSERT INTO branches (branch_id, name, address, open_time, close_time, latitude, longitude, max_delivery_distance) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)"
        return await self.execute(query, *args)

    async def create_category(self, *args):
        query = "INSERT INTO categories (category_id, name, image) VALUES ($1, $2, $3)"
        return await self.execute(query, *args)

    async def get_category(self, category_id):
        query = "SELECT image, name FROM categories WHERE category_id = $1"
        return await self.fetch_one(query, category_id)

    async def create_category_product(self, *args):
        query = "INSERT INTO products (product_id, category_id, name, description, price, size, image) VALUES ($1, $2, $3, $4, $5, $6, $7)"
        return await self.execute(query, *args)

    async def get_categories(self):
        """Get categories"""
        query = "SELECT category_id, name FROM categories"
        return await self.fetch(query)

    async def get_products(self, category_id):
        """GET PRODUCTS"""
        query = "SELECT product_id, name FROM products WHERE category_id  = $1"
        return await self.fetch(query, category_id)

    async def get_product(self, product_id):
        query = "SELECT product_id, category_id, name, description, price, size, image FROM products WHERE product_id = $1"
        return await self.fetch_one(query, product_id)

    async def create_order(self, *args):
        query = "INSERT INTO orders (user_id, order_type, branch_id, d_longitude, d_latitude) VALUES ($1, $2, $3, $4, $5) RETURNING order_id"
        return await self.fetch_one(query, *args)

    async def get_current_order(self, user_id):
        query = "SELECT * FROM orders WHERE user_id = $1 AND status = 'CREATED'"
        return await self.fetch_one(query, user_id)

    async def create_or_update_order_items(self, order_id, product_id, quantity):
        query = "SELECT order_item_id FROM order_items WHERE order_id = $1 AND product_id = $2"
        order_item = await self.fetch_one(query, order_id, product_id)

        if not order_item:
            query = "INSERT INTO order_items (order_id, product_id, quantity) VALUES ($1, $2, $3)"
            return await self.execute(query, order_id, product_id, quantity)

        query = "UPDATE order_items SET quantity = $1 WHERE order_id = $2 AND product_id = $3 RETURNING order_item_id, order_id, product_id, quantity"
        return await self.execute(query, quantity, order_id, product_id)


db = DBManager()

# CREATE TABLE IF NOT EXISTS orders (
#                 order_id SERIAL PRIMARY KEY,
#                 user_id BIGINT REFERENCES users(telegram_id) ON DELETE CASCADE,
#                 total_price FLOAT DEFAULT 0,
#                 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#                 updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
# );
#
# CREATE TABLE IF NOT EXISTS order_items (
#                 order_item_id SERIAL PRIMARY KEY,
#                 order_id BIGINT REFERENCES order(order_id) ON DELETE CASCADE,
#                 product_id BIGINT, REFERENCES product(product_id) ON DELETE CASCADE,
#                 quantity INT NOT NULL CHECK (quantity > 0),
#                 price FLOAT NOT NULL,
#                 total_price FLOAT GENERATED ALWAYS AS (price * quantity) STORED,
#                 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#                 updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
# );
