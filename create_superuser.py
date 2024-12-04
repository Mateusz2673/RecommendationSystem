import os
from django.contrib.auth import get_user_model

User = get_user_model()

username = os.getenv("ADMIN_USERNAME", "admin")
email = os.getenv("ADMIN_EMAIL", "admin@example.com")
password = os.getenv("ADMIN_PASSWORD", "password")

if not User.objects.filter(login=username).exists():
    User.objects.create_superuser(login=username, email=email, password=password)
    print(f"Superuser {username} created successfully.")
else:
    print(f"Superuser {username} already exists.")