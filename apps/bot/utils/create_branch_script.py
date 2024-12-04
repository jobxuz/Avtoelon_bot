import asyncio
import argparse
from datetime import datetime
from app.utils.db_manager import db


async def initialize():
    await db.connect()
    await db.create_tables()
    await db.disconnect()

def parse_time(time_str):
    """Parse a time string (HH:MM) into a datetime.time object."""
    return datetime.strptime(time_str, "%H:%M").time()

async def main(branch_id, name, address, open_time, close_time, latitude, longitude):
    await db.connect()

    open_time = parse_time(open_time)
    close_time = parse_time(close_time)

    await db.create_branch(branch_id, name, address, open_time, close_time, latitude, longitude)

    print(f"Branch '{name}' with ID {branch_id} has been created.")

    await db.disconnect()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a new branch in the database")
    parser.add_argument("branch_id", type=int, help="ID of the branch")
    parser.add_argument("name", type=str, help="Name of the branch")
    parser.add_argument("address", type=str, help="Address of the branch")
    parser.add_argument("open_time", type=str, help="Opening time of the branch (HH:MM)")
    parser.add_argument("close_time", type=str, help="Closing time of the branch (HH:MM)")
    parser.add_argument("latitude", type=float, help="Latitude of the branch")
    parser.add_argument("longitude", type=float, help="Longitude of the branch")

    args = parser.parse_args()

    asyncio.run(initialize())
    asyncio.run(
        main(
            args.branch_id,
            args.name,
            args.address,
            args.open_time,
            args.close_time,
            args.latitude,
            args.longitude,
        )
    )

    asyncio.run(db.disconnect())