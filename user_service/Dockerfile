FROM python:3.9-slim

WORKDIR /app

# Cài đặt các gói phụ thuộc cần thiết cho mysqlclient
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    gcc \
    pkg-config \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# COPY entrypoint.sh ./entrypoint.sh
# Cấp quyền thực thi cho entrypoint.sh
# RUN chmod +x entrypoint.sh

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]