import html, re, urllib.parse, bleach
from fastapi import HTTPException
from bs4 import BeautifulSoup

def validate_and_sanitize_input(data: dict) -> dict:
    """
    Xử lý và làm sạch toàn bộ dữ liệu người dùng trước khi lưu vào CSDL.
    - Giải mã URL encoding.
    - Làm sạch thẻ HTML, JavaScript.
    - Kiểm tra NoSQL injection.
    
    :param data: Dữ liệu người dùng gửi lên (dictionary).
    :return: Dữ liệu đã được làm sạch và kiểm tra.
    """

    # Mẫu regex kiểm tra thẻ HTML
    html_pattern = re.compile(r'<.*?>')
    
    # Mẫu regex kiểm tra NoSQL injection (các ký tự đặc biệt và từ khóa)
    nosqli_pattern = re.compile(r'(\$|\{|\}|\,|\(|\)|\:|\s|=|\'|\"|\[|\])', re.IGNORECASE)

    # Hàm để làm sạch đầu vào, giải mã URL và loại bỏ thẻ HTML
    def sanitize_input_nohtml(input_text: str) -> str:
        """
        Làm sạch đầu vào: Giải mã URL encoding, loại bỏ thẻ HTML, mã hóa ký tự đặc biệt,
        và loại bỏ khoảng trắng dư thừa. Sau đó làm sạch thêm bằng bleach và html.escape.

        Args:
            input_text (str): Chuỗi chứa đầu vào, có thể là URL encoded.

        Returns:
            str: Chuỗi đầu ra an toàn.
        """
        if not isinstance(input_text, str):
            raise ValueError("Input must be a string")

        try:
            # Giải mã URL encoding
            decoded_text = urllib.parse.unquote(input_text)
            
            # Chuyển đổi sang UTF-8 nếu cần
            utf8_text = decoded_text.encode('utf-8', errors='ignore').decode('utf-8')
            
            # Kiểm tra nếu dữ liệu có chứa thẻ HTML
            if '<' in utf8_text and '>' in utf8_text:
                soup = BeautifulSoup(utf8_text, "html.parser")
                clean_text = soup.get_text()
            else:
                clean_text = utf8_text

            # Mã hóa ký tự đặc biệt để tránh XSS
            safe_text = html.escape(clean_text)

            # Làm sạch thêm bằng bleach (Loại bỏ HTML tags, JavaScript và CSS)
            bleach_clean_text = bleach.clean(safe_text, tags=[], attributes=[], strip=True)

            # Escape lại để đảm bảo không có HTML hoặc JavaScript còn sót lại
            final_clean_text = html.escape(bleach_clean_text)

            # Loại bỏ khoảng trắng dư thừa
            return final_clean_text.strip()
        except Exception as e:
            print(f"Error processing input: {e}")
            return ""

    # Duyệt qua từng trường dữ liệu và làm sạch
    for key, value in data.items():
        if isinstance(value, str):
            # Làm sạch dữ liệu đầu vào
            cleaned_value = sanitize_input_nohtml(value)
            
            # Kiểm tra thẻ HTML
            if html_pattern.search(cleaned_value):
                raise HTTPException(status_code=400, detail=f"Error: HTML tags detected in {key}. Please enter valid data without HTML tags.")
            
            # Kiểm tra NoSQL injection
            if nosqli_pattern.search(cleaned_value):
                raise HTTPException(status_code=400, detail=f"Error: NoSQL injection detected in {key}. Please enter valid data without special characters.")
            
            # Cập nhật lại dữ liệu đã được làm sạch
            data[key] = cleaned_value
    return data


def compare_and_validate(user_data: dict):
    # Sao chép dữ liệu gốc để so sánh sau khi làm sạch
    original_data = user_data.copy()

    # Làm sạch dữ liệu
    cleaned_data = validate_and_sanitize_input(user_data)

    # So sánh dữ liệu gốc và dữ liệu sau khi làm sạch
    if original_data != cleaned_data:
        raise HTTPException(status_code=400, detail="Error: Injection detected. Please enter valid data without malicious content.")
    else: return cleaned_data
