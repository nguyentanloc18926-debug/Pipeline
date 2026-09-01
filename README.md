# E-Commerce Data Cleaning Pipeline

## Giới thiệu
Pipeline tự động kết nối CSDL SQL Server, trích xuất dữ liệu thô, làm sạch đơn rác/lỗi và xuất tập Feature sẵn sàng cho huấn luyện ML.

## Luồng xử lý (Data Flow)
SQL Server (Raw Data) -> Pandas Cleaning (Drop NaNs, Duplicates) -> Aggregation (CustomerID) -> CSV Export

## Công nghệ sử dụng
- Python 3.12
- Pandas, SQLAlchemy, pyodbc
- SQL Server