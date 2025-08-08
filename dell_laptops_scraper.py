import os
import csv
import lxml
import requests
from bs4 import BeautifulSoup

def get_page_content(num):
    url = f'https://www.dell.com/en-us/shop/dell-laptops/scr/laptops?page={num}'
    raw = requests.get(url).content
    page = BeautifulSoup(raw, 'lxml')
    return page

def scrap_page(page, page_num):
    page_data = {}
    laptops = page.find_all('article', {'class':'variant-stack'})
    for i, laptop in enumerate(laptops):
        laptop_data = {}
        laptop_key = f'{page_num}-{i+1}'
        title = laptop.find('h3', {'class':'ps-title'}).find('a').text.strip()
        price = laptop.find('span', {'class':'ps-variant-price-amount'}).text.strip()
        laptop_data['Title'] = title
        laptop_data['Price'] = price
        specs = laptop.find('ul', {'class':'dds__more-less__target'}).find_all('dl')
        for dl in specs:
            dts = dl.find_all('dt')
            dds = dl.find_all('dd')
            if len(dts) == len(dds):
                for d in range(len(dts)):
                    laptop_data[dts[d].text.strip()] = dds[d].text.strip()
        page_data[laptop_key] = laptop_data
    return page_data

def scrap_all_pages(num):
    scraped_data = {}
    for i in range(num):
        page_num = i+1
        page_content = get_page_content(i+1)
        page_data = scrap_page(page_content, page_num)
        scraped_data.update(page_data)
    return(scraped_data)


def save_data(num):
    file_path = 'data.csv'
    file_exists = os.path.exists(file_path)
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Product Name', 'Price', 'Processor', 'OS', 'Graphics', 'Memory (RAM)', 'Storage', 'Display'])
        scraped_data = scrap_all_pages(num)
        for item in scraped_data:
            laptop_details = scraped_data[item]
            name = laptop_details.get('Title')
            price = laptop_details.get('Price')
            processor = laptop_details.get('Processor')
            op_s = laptop_details.get('OS')
            graphics = laptop_details.get('Graphics')
            memory = laptop_details.get('Memory (RAM)')
            storage = laptop_details.get('Storage')
            display = laptop_details.get('Display')
            writer.writerow([name, price, processor, op_s, graphics, memory, storage, display])

num_pages = 6
save_data(num_pages)