import requests
import pandas as pd
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import os

# 1. Lấy dữ liệu từ VCB
url = "https://portal.vietcombank.com.vn/UserControls/TVPortal.TyGia/pXML.aspx"
try:
    response = requests.get(url, timeout=30)
    tree = ET.fromstring(response.content)

    # 2. Xử lý thời gian (Chuyển sang giờ Việt Nam UTC+7)
    # Vì GitHub chạy giờ quốc tế (UTC), ta cộng thêm 7 tiếng
    now_vn = datetime.utcnow() + timedelta(hours=7)
    date_str = now_vn.strftime("%Y-%m-%d %H:%M:%S")

    data = []
    for child in tree.findall('Exrate'):
        data.append({
            'Ngày giờ cập nhật': date_str,  # Cột yêu cầu của bạn
            'Mã ngoại tệ': child.get('CurrencyCode'),
            'Tên ngoại tệ': child.get('CurrencyName'),
            'Mua tiền mặt': child.get('Buy'),
            'Mua chuyển khoản': child.get('Transfer'),
            'Bán': child.get('Sell')
        })

    df_new = pd.DataFrame(data)
    file_name = "ty_gia_vcb.xlsx"

    # 3. Lưu hoặc nối thêm dữ liệu vào Excel
    if os.path.exists(file_name):
        # Đọc file cũ, sau đó dán dữ liệu mới vào dưới cùng
        df_old = pd.read_excel(file_name)
        df_final = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df_final = df_new

    # Xuất file Excel
    df_final.to_excel(file_name, index=False)
    print(f"Thành công: Đã lưu dữ liệu lúc {date_str}")

except Exception as e:
    print(f"Lỗi xảy ra: {e}")
