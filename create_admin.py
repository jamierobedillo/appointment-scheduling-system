
from werkzeug.security import generate_password_hash

from repositories.user_repository import UserRepository


user_repository = UserRepository()

full_name = "System Administrator"
email = "admin.python@example.com"
phone = "09123456789"
password = "AdminPython123"

existing_admin = user_repository.get_user_by_email(email)

if existing_admin:
    print("Admin account already exists.")
else:
    hashed_password = generate_password_hash(password)

    user_repository.create_admin(
        full_name,
        email,
        hashed_password,
        phone
    )

    print("Admin account created successfully!")
