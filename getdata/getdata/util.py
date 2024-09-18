from dateutil import parser
import re
import csv
import os
from datetime import datetime


headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0'}


def parser_time(date_string):
    date_match = re.search(
        r"\b\w{3} \d{1,2}, \d{4} at \d{1,2}:\d{2} (AM|PM)\b", date_string
    )

    if date_match:
        date_str = date_match.group(0)
        # Phân tích chuỗi ngày giờ thành đối tượng datetime
        date = parser.parse(date_str)
        return date
    else:
        return "No date found in the string"