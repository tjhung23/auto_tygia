import gspread
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

# Kết nối Google Sheets bằng file tạo từ Secret
gc = gspread.service_account(filename='credentials.json')
sh = gc.open("update ty gia") # Tên file Google Sheets bạn đã tạo
worksheet = sh.sheet1

url = "https://portal.vietcombank.com.vn/UserControls/TVPortal.TyGia/pXML.aspx"
response = requests.get(url)
tree = ET.fromstring(response.content)
now_vn = datetime.utcnow() + timedelta(hours=7)
date_str = now_vn.strftime("%Y-%m-%d %H:%M:%S")

for child in tree.findall('Exrate'):
    worksheet.append_row([
        date_str, 
        child.get('CurrencyCode'), 
        child.get('CurrencyName'), 
        child.get('Buy'), 
        child.get('Transfer'), 
        child.get('Sell')
    ])
print("Đã cập nhật tỷ giá vào Google Sheets!")
