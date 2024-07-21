from django.contrib.auth.backends import ModelBackend
from .models import MyUser

class UserIDAuthBackend(ModelBackend):
    def authenticate(self, request, UserID=None, password=None, **kwargs):
        try:
            user = MyUser.objects.get(UserID=UserID)
            if user.check_password(password):
                return user
        except MyUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return MyUser.objects.get(pk=user_id)
        except MyUser.DoesNotExist:
            return None