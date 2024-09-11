import csv


import os


import re

import scrapy


from bs4 import BeautifulSoup


from ..util import parser_time


class VozSalary(scrapy.Spider):
    name = "VozSpider"

    def start_requests(self):
        urls = [
            "https://voz.vn/t/event-box-cntt-2023-chia-se-kinh-nghiem-phong-van.694369/",
            "https://voz.vn/t/co-ai-bi-sa-thai-dot-nay-ko-ver-2-viet-tat-ten-moi-cty.855701/",
            "https://voz.vn/t/thread-tong-hop-chia-se-ve-muc-luong-tai-cac-cong-ty-part-2.515355/",
            "https://voz.vn/t/con-duong-xuat-ngoai-cho-dan-it.112157/",
            "https://voz.vn/t/thao-luan-data-analysis-ml-dl-ai-all-levels-vao-day-chem-gio-nao.156895/",
            "https://voz.vn/t/review-cong-ty-cntt-boi-het-vao-viet-tat-ten-moi-cty.677450/",
            "https://voz.vn/t/event-box-cntt-2023-chia-se-kinh-nghiem-phong-van.694369/",
        ]
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0'
        }
        for url in urls:
            yield scrapy.Request(url=url, headers=headers, callback=self.get_pages)

    def get_pages(self, response):
        # get max_page and sent requests

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0'
        }
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")
        result = soup.find_all("li", class_="pageNav-page")
        max_page = int([li for li in result if len(li["class"]) == 1][-1].get_text())
        for page in range(1, max_page + 1):
            page_url = f"{response.url}?page={page}"
            yield scrapy.Request(url=page_url, headers=headers, callback=self.parse_page)

    @staticmethod
    def parse_page(response):
        url_name = re.sub('[<>:"/\\|?*]', '-', response.url)
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")
        dict_user = {}
        articles = soup.find_all(
            "article", class_="message message--post js-post js-inlineModContainer"
        )
        text_csv = []
        for article in articles:
            user_details = article.find("div", class_="message-userDetails")
            # get list distinct usderid,username
            if user_details:
                message_name = user_details.find("a", class_="username")
                if message_name:
                    user_id = message_name.get("data-user-id")
                    user_name = message_name.text
                    dict_user[user_id] = user_name
            user_details_content = article.find(
                "div", class_="message-userContent lbContainer js-lbContainer"
            )
            # get data block
            if user_details_content:
                message_id = re.findall(r"\d+", user_details_content.get("data-lb-id"))[0]
                message_time = parser_time(user_details_content.get("data-lb-caption-desc"))
                blockquote = user_details_content.find(
                    "article", class_="message-body js-selectToQuote"
                )
                blockquote1 = user_details_content.find_all(
                    "blockquote",
                    class_="bbCodeBlock bbCodeBlock--expandable bbCodeBlock--quote js-expandWatch",
                )
                ad_list = []
                for block in blockquote1:
                    block_id = re.findall(r"\d+", block.get("data-attributes"))
                    data_source = re.findall(r"\d+", block.get("data-source"))
                    data_text = block.get_text()
                    ad_list.append(data_source)
                    ad_list.append({
                        "blockid": block_id[0],
                        "data_source": data_source[0],
                        "data_text": data_text,
                    })
            text_csv.append({
                "message_id": message_id,
                "message_time": message_time,
                "quote": ad_list,
                "text": blockquote.getText(),
            })
        # save to csv each file   
        folder_path = "D:\\Project\\Vietnam-IT-Job-Market-Analysis\\getdata\\csv_folder"
        file_data_block = os.path.join(folder_path, f"{url_name}.csv")
        file_id_name = os.path.join(folder_path, f"{url_name}userid.csv")
        os.makedirs(folder_path, exist_ok=True)
        with open(file_id_name, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["UserID", "UserName"])
            for user_id, user_name in dict_user.items():
                writer.writerow([user_id, user_name])
        with open(file_data_block, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["UserID", "MessageTime", "Quote", "Text"])
            for rows in text_csv:
                writer.writerow([
                    rows.get("message_id"),
                    rows.get("message_time"),
                    rows.get("quote"),
                    rows.get("text"),
                ])
        yield text_csv