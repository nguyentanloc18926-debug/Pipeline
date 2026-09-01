import pandas as pd
from sqlalchemy import create_engine

# 1. KẾT NỐI VÀ TRÍCH XUẤT DỮ LIỆU TỪ SQL SERVER
# Nếu dùng Windows Authentication (như bên dưới):
connection_string = (
    "mssql+pyodbc://MSI\\MSSQLSERVER01/ECommerceDB?"
    "driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
)

print("--- Đang kết nối CSDL và đọc dữ liệu ---")
engine = create_engine(connection_string)

# Đọc dữ liệu bằng SQL query (chỉ lấy các đơn thành công)
query = "SELECT * FROM RawTransactions WHERE Status = 'Completed'"
df_raw = pd.read_sql(query, engine)
print(f"Dữ liệu thô đọc về ({len(df_raw)} dòng):")
print(df_raw)

# 2. XỬ LÝ VÀ LÀM SẠCH DỮ LIỆU BẰNG PANDAS
print("\n--- Đang làm sạch dữ liệu ---")

# Loại bỏ dòng bị trùng lặp
df_clean = df_raw.drop_duplicates(subset=['TransactionID'])

# Loại bỏ dòng bị thiếu tiền (NaN/NULL)
df_clean = df_clean.dropna(subset=['Amount'])

# Chuyển đổi Ngày về chuẩn Datetime, bỏ qua các ô lỗi ngày
df_clean['TransactionDate'] = pd.to_datetime(df_clean['TransactionDate'], errors='coerce')
df_clean = df_clean.dropna(subset=['TransactionDate'])

# 3. GOM NHÓM DỮ LIỆU (AGGREGATION) CON SỐ SẠCH
# Tính tổng chi tiêu và tổng số đơn hàng của từng CustomerID
df_customer_summary = df_clean.groupby('CustomerID').agg(
    TotalSpent=('Amount', 'sum'),
    TotalOrders=('TransactionID', 'count'),
    LastPurchase=('TransactionDate', 'max')
).reset_index()

print("\n--- Dữ liệu sau khi làm sạch & gom nhóm ---")
print(df_customer_summary)

# 4. XUẤT KẾT QUẢ SẠCH DÀNH CHO ML TRAIN
df_customer_summary.to_csv("clean_customer_features.csv", index=False)
print("\n=> Đã xuất file clean_customer_features.csv thành công!")