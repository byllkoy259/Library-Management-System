# Chỉ định Image cơ sở
FROM python:3.11-slim

# Thiết lập thư mục làm việc
WORKDIR /app

# Sao chép file requirements.txt vào thư mục làm việc
COPY requirements.txt .

# Cài đặt các gói hệ thống cần thiết
# RUN apt-get update && apt-get install -y \
#     gcc \
#     libffi-dev \
#     python3-dev \
#     build-essential \
#     && rm -rf /var/lib/apt/lists/*

# Cài đặt các gói cần thiết
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn vào thư mục làm việc
COPY . .

# Khởi động Nginx khi container được chạy
CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]