import requests
from bs4 import BeautifulSoup
import re
import os
import random
import time
from utils import add_watermark

base_url = 'https://machtalk.xiachufang.com'
search_url = base_url + "/search/?keyword="

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}


# 获取菜谱链接列表
def parse_recipe_urls(keyword):
    search = search_url + keyword
    response = requests.get(search, headers=headers)
    content = response.text
    soup = BeautifulSoup(content, "html.parser")
    recipe_addr_list = soup.select('.recipe-96-horizon')
    return [base_url + addr.get('href') for addr in recipe_addr_list if re.search('/recipe/\d+\/$', addr.get('href')) is not None]


# 获取菜谱主图下载地址
def get_main_img_url(recipe_url):
    response = requests.get(recipe_url, headers=headers)
    content = response.text
    soup = BeautifulSoup(content, "html.parser")
    return soup.select('.recipe-main')[0].find_all('img')[0].get('src')


# 下载图片
def download_image(url, file_path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print("图片下载成功：", file_path)
    else:
        print("图片下载失败")


# 创建目录
def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


# 保存菜谱图片
def download_recipe_imgs(recipe_name):
    recipe_urls = parse_recipe_urls(recipe_name)
    save_path = f'./菜谱图片/{recipe_name}'
    create_directory(save_path)
    for i, recipe_url in enumerate(recipe_urls[:5]):
        main_img_url = get_main_img_url(recipe_url)
        dest_path = f'{save_path}/{i}.jpg'
        dest_path_mark = f'{save_path}/{i}_mark.jpg'
        # 下载图片
        download_image(main_img_url, dest_path)
        # 添加水印
        add_watermark(dest_path, dest_path_mark, 'watermark.png')

    time_to_sleep = int(random.random() * 3)
    time.sleep(time_to_sleep)


# 获取菜谱名称
def get_names(file_path):
    f = open(file_path, "r", encoding='utf-8')
    lines = f.readlines()
    name_list = []
    for line in lines:
        new_line = line.strip().split('（')[0]
        name_list.append(re.split('\d+', new_line)[0])
    f.close()
    return name_list


if __name__ == '__main__':
    name_list = get_names('./菜谱名称.txt')[:1]
    for name in name_list:
        download_recipe_imgs(name)
