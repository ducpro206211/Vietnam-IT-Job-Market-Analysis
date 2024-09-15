import csv


import os


import re

import scrapy


from bs4 import BeautifulSoup


from ..util import parser_time

from ..items import GetVOZdataItem


class VozSalary(scrapy.Spider):
    name = "VozSpider"

    def start_requests(self):
        urls = [
            "https://voz.vn/t/kiem-job-tai-faang-va-cac-big-tech-khac.594813/"
            # "https://voz.vn/t/event-box-cntt-2023-chia-se-kinh-nghiem-phong-van.694369/",
            # "https://voz.vn/t/co-ai-bi-sa-thai-dot-nay-ko-ver-2-viet-tat-ten-moi-cty.855701/",
            # "https://voz.vn/t/thread-tong-hop-chia-se-ve-muc-luong-tai-cac-cong-ty-part-2.515355/",
            # "https://voz.vn/t/con-duong-xuat-ngoai-cho-dan-it.112157/",
            # "https://voz.vn/t/thao-luan-data-analysis-ml-dl-ai-all-levels-vao-day-chem-gio-nao.156895/",
            # "https://voz.vn/t/review-cong-ty-cntt-boi-het-vao-viet-tat-ten-moi-cty.677450/",
            # "https://voz.vn/t/event-box-cntt-2023-chia-se-kinh-nghiem-phong-van.694369/",
        ]
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0"
        }
        for url in urls:
            yield scrapy.Request(url=url, headers=headers, callback=self.get_pages)

    def get_pages(self, response):
        # get max_page and sent requests

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0"
        }
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")
        result = soup.find_all("li", class_="pageNav-page")
        max_page = int([li for li in result if len(li["class"]) == 1][-1].get_text())
        for page in range(1, max_page + 1):
            page_url = f"{response.url}?page={page}"
            yield scrapy.Request(
                url=page_url, headers=headers, callback=self.parse_page
            )

    @staticmethod
    def parse_page(response):
        item = GetVOZdataItem()
        url_name = re.sub('[<>:"/\\|?*]', "-", response.url)
        pattern1 = r"https---voz.vn-t-(.*?)(?:--page|-page)-\d+-page=(\d+)"
        pattern2 = r"https---voz.vn-t-(.*?)--page=(\d+)"

        match1 = re.search(pattern1, url_name)
        if match1:
            nameContent = match1.group(1)
            numberPage = int(match1.group(2))
            item["NameContent"] = nameContent
            item["NumberPage"] = numberPage
        else:
            # Nếu không tìm thấy match, sử dụng giá trị mặc định
            match2 = re.search(pattern2, url_name)
            if match2:
                nameContent = match2.group(1)
                numberPage = int(match2.group(2))
                item["NameContent"] = nameContent
                item["NumberPage"] = numberPage
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
                    item["DataUserId"] = user_id
                    item["DataUserName"] = user_name
                    dict_user[user_id] = user_name
            user_details_content = article.find(
                "div", class_="message-userContent lbContainer js-lbContainer"
            )
            # get data block
            if user_details_content:
                # message_id =

                # message_time =
                dataText = user_details_content.find(
                    "article", class_="message-body js-selectToQuote"
                )

                item["ReplyId"] = re.findall(
                    r"\d+", user_details_content.get("data-lb-id")
                )[0]
                item["ReplyTime"] = parser_time(
                    user_details_content.get("data-lb-caption-desc")
                )
                item["ReplyText"] = dataText.getText()
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
                    ad_list.append(
                        {
                            "blockid": block_id,
                            "data_source": data_source,
                            "data_text": data_text,
                        }
                    )
                item["QuoteFull"] = ad_list
                # item["QuoteBlockId"] = [item["blockid"] for item in ad_list]
                # item["QuoteBlockText"] = [item["data_text"] for item in ad_list]
                # item["QuoteDataSource"] = [item["data_source"] for item in ad_list]

            text_csv.append(
                {
                    "message_id": item["ReplyId"],
                    "message_time": item["ReplyTime"],
                    "quote": item["QuoteFull"],
                    "text": item["ReplyText"],
                }
            )
        item["FullText"] = text_csv
        # save to csv each file
        yield item
        # yield
