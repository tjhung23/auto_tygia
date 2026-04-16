import requests
import pandas as pd
import xml.etree.ElementTree as ET
from datetime import datetime
import os

# Lấy dữ liệu từ VCB
url = "https://portal.vietcombank.com.vn/UserControls/TVPortal.TyGia/pXML.aspx"
try:
    response = requests.get(url, timeout=30)
    tree = ET.fromstring(response.content)

    data = []
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for child in tree.findall('Exrate'):
        data.append({
            'Ngày': date_str,
            'Mã ngoại tệ': child.get('CurrencyCode'),
            'Tên ngoại tệ': child.get('CurrencyName'),
            'Mua tiền mặt': child.get('Buy'),
            'Mua chuyển khoản': child.get('Transfer'),
            'Bán': child.get('Sell')
        })

    df_new = pd.DataFrame(data)
    file_name = "ty_gia_vcb.xlsx"

    # Lưu hoặc nối thêm dữ liệu vào Excel
    if os.path.exists(file_name):
        df_old = pd.read_excel(file_name)
        df_final = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df_final = df_new

    df_final.to_excel(file_name, index=False)
    print(f"Thành công: Cập nhật tỷ giá lúc {date_str}")
except Exception as e:
    print(f"Lỗi rồi: {e}")
