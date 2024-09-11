import scrapy
#from items import GetdataItem
from bs4 import BeautifulSoup
import re
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
        for url in urls:
            yield scrapy.Request(url=url, callback=self.get_pages)

    def get_pages(self, response):
        # get max_page and sent requests
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")
        result = soup.find_all("li", class_="pageNav-page")
        max_page = int([li for li in result if len(li["class"]) == 1][-1].get_text())
        for page in range(1, max_page + 1):
            page_url = f"{response.url}?page={page}"
            yield scrapy.Request(url=page_url, callback=self.parse_page)

    def parse_page(self, response):
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")
        dict_user = {}
        articles = soup.find_all(
            "article", class_="message message--post js-post js-inlineModContainer"
        )

        for article in articles:
            # get list of usder id and name
            user_details = article.find("div", class_="message-userDetails")

            if user_details:

                message_name = user_details.find("a", class_="username")

                if message_name:

                    user_id = message_name.get("data-user-id")
                    user_name = message_name.text
                    dict_user[user_id] = user_name

            # get data block
            user_details_content = article.find(
                "div", class_="message-userContent lbContainer js-lbContainer"
            )
            if user_details_content:
                message_id = re.findall(r"\d+", user_details_content.get("data-lb-id"))[
                    0
                ]
                message_time = parser_time(
                    user_details_content.get("data-lb-caption-desc")
                )
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
                    ad_list.append(
                        {
                            "blockid": block_id[0],
                            "data_source": data_source[0],
                            "data_text": data_text,
                        }
                    )
                data =  {
                    "message_id": message_id,
                    "message_time": message_time,
                    "quote": ad_list,
                    "text": blockquote.getText(),
                }
        yield {"Userlist":dict_user,
               "data" : data }