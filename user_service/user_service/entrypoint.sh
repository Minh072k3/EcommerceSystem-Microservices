#!/bin/bash

# Đợi MySQL khởi động
sleep 15

# Áp dụng migrations
python manage.py migrate

# Tạo tài khoản admin nếu chưa tồn tại
python manage.py shell -c "
from users.models import User
if not User.objects.filter(email='admin@example.com').exists():
    user = User.objects.create_user(
        username='admin',
        email='admin@example.com',
        password='admin123',
        is_superuser=True,
        is_staff=True
    )
    user.user_type = 'ADMIN'
    user.save()
    print('Admin user created successfully')
else:
    print('Admin user already exists')
"

# Khởi động server
python manage.py runserver 0.0.0.0:8000