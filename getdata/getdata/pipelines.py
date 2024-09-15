# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
import csv
import re
from itemadapter import ItemAdapter
class CsvPipeline:
    def process_item(self, item, spider):
        
        folder_path = "I:\\DE_Project\\datatest"
        file_data_block = os.path.join(folder_path, f"{item['NameContent']}page-{item['NumberPage']}.csv")
        file_id_name = os.path.join(folder_path, f"{item['NameContent']}page-{item['NumberPage']}-userid.csv")
        
        os.makedirs(folder_path, exist_ok=True)

        # Save user info
        with open(file_id_name, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["UserID", "UserName", "PageId", "nameContent"])
            writer.writerow([item["DataUserId"], item["DataUserName"], item["NumberPage"], item["NameContent"]])
        
        # Save message info
        with open(file_data_block, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                ["UserID", "MessageTime", "Quote", "Text", "PageId", "nameContent"]
            )
            for rows in item['FullText']:
                writer.writerow(
                    [
                        rows.get("message_id"),
                        rows.get("message_time"),
                        rows.get("quote"),
                        rows.get("text"),
                        item['NumberPage'],
                        item['NameContent'],
                    ]
                )
            # Xử lý thêm để lưu thông tin message tại đây
