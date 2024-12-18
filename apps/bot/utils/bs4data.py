# import requests
# from bs4 import BeautifulSoup



# def data_id_funcsion(brand):
#     url = 'https://avtoelon.uz/uz/avto/' + brand
#     headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
# }

#     response = requests.get(url, headers=headers)  
#     #response = requests.get(url)

#     soup = BeautifulSoup(response.text, 'html.parser')
#     advert_elements = soup.find_all('div', class_='row list-item a-elem')


#     data_ids = [advert['data-id'] for advert in advert_elements[-5:]]  


#     return data_ids


import requests
from bs4 import BeautifulSoup
from apps.bot.models import AllCar,CarBrand,CarModel



def get_car_brands():
    print('ishlayabdi///////')
    url = 'https://avtoelon.uz/uz/' 
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    links_list = soup.find('ul', class_='links-list links-list--column-count-6 js-links-list')
    brands = []

    if links_list:
        for link in links_list.find_all('a', class_='links-list__link'):
            brand_name = link.get_text(strip=True).lower()
            if brand_name: 
                brands.append(brand_name)

    return brands




def get_car_brands():
    print('ishlayabdi///////')
    url = 'https://avtoelon.uz/uz/' 
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    links_list = soup.find('ul', class_='links-list links-list--column-count-6 js-links-list')
    brands = []

    if links_list:
        for link in links_list.find_all('a', class_='links-list__link'):
            brand_name = link.get_text(strip=True).lower()
            if brand_name: 
                brands.append(brand_name)

    return brands










def data_id_funcsion():
    #url = 'https://avtoelon.uz/uz/avto/' + brand 
    url = 'https://avtoelon.uz/uz/avto/?price-currency=1' 
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')
    advert_elements = soup.find_all('div', class_='row list-item a-elem')


    data_ids = [advert['data-id'] for advert in advert_elements[-5:]]  

    

    return data_ids

# print(data_id_funcsion())





def car_data(car):
    url = 'https://avtoelon.uz/uz/a/show/' + str(car)

    # response = requests.get(url)

    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.content, 'html.parser')

    images = soup.find_all('a', class_='small-thumb')
    image_urls = [img.find('img')['src'] for img in images]
    images_str = ""
    for i, img_url in enumerate(image_urls):
        images_str += f"{img_url}\n"

    title = soup.find('h1', class_='a-title__text')
    full_title = ""
    if title:
        brand = title.find('span', itemprop='brand').get_text(strip=True)
        name = title.find('span', itemprop='name').get_text(strip=True)
        full_title = f"{brand} {name}\n"

    price_text = ""
    price = soup.find('span', class_='a-price__text')
    if price:
        price_text = price.get_text(strip=True) + "\n"

    description_params = soup.find_all('dl', class_='clearfix dl-horizontal description-params')
    description_params_str = ""
    for param in description_params:
        dt_elements = param.find_all('dt', class_='value-title')
        dd_elements = param.find_all('dd', class_='value clearfix')

        for dt, dd in zip(dt_elements, dd_elements):
            title = dt.get_text(strip=True)
            value = dd.get_text(strip=True)
            description_params_str += f"{title} : {value}\n"

    phone_number = "Telefon raqami topilmadi"
    phone = soup.find('li', {'class': 'contacts-block__item'})
    if phone:
        phone_number = phone.get_text(strip=True) + "\n"

    description_text = ""
    description = soup.find('div', class_="description-text")
    if description:
        description_text = description.get_text(strip=True) + "\n"

    main_url = f"Asosiy manzil: {url}"

    data_id = ""
    note_div = soup.find('div', class_='note')
    if note_div:
        data_id = note_div.get('data-id', '') + "\n"






    car_brand = None
    car_model = None


    meta_tag = soup.find('meta', {'itemprop': 'position', 'content': '5'})

    if meta_tag:
        li_tag = meta_tag.find_parent('li')
        if li_tag:
            a_tag = li_tag.find('a', href=True)
            if a_tag:
                href = a_tag['href']
                parts = href.strip('/').split('/')
                if len(parts) >= 2:
                    car_brand = parts[-2]  
                    car_model = parts[-1]  
    
    if not car_brand or not car_model:
        meta_tag = soup.find('meta', {'itemprop': 'position', 'content': '4'})
        if meta_tag:
            li_tag = meta_tag.find_parent('li')
            if li_tag:
                a_tag = li_tag.find('a', href=True)
                if a_tag:
                    href = a_tag['href']
                    parts = href.strip('/').split('/')
                    if len(parts) >= 2:
                        car_brand = parts[-2]  
                        car_model = parts[-1]  




    
    if data_id and not AllCar.objects.filter(data_id=data_id).exists():
        try:
            AllCar.objects.create(
                carbrand=car_brand,
                carmodel=car_model,
                images_str=images_str,
                full_title=full_title,
                price_text=price_text,
                description_params_str=description_params_str,
                phone_number=phone_number,
                description_text=description_text,
                main_url=main_url,
                data_id=data_id
            )
            return "Ma'lumot bazaga saqlandi."
        except Exception as e:
            return f"Xato yuz berdi: {str(e)}"
    else:
        return "Ma'lumot allaqachon bazada mavjud yoki data_id topilmadi."
    