from dateutil import parser
import re




def parser_time(string):
    # Phân tích và chuyển đổi chuỗi ngày giờ
    # Lấy phần ngày giờ từ chuỗi, ví dụ sử dụng biểu thức chính quy để trích xuất phần ngày giờ
    date_match = re.search(
        r"\b\w{3} \d{2}, \d{4} at \d{1,2}:\d{2} (AM|PM)\b", date_string
    )

    if date_match:
        date_str = date_match.group(0)
        # Phân tích chuỗi ngày giờ thành đối tượng datetime
        date = parser.parse(date_str)
        return date
    else:
        return "No date found in the string"
