from user.models import User


def create_user(phone_number):
    user = User(phone_number=phone_number, username=f"user_{phone_number}")
    user.set_unusable_password()
    user.save()