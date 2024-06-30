from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User

class HardCodedAuthBackend(BaseBackend):
    def authenticate(self, request, username = None, password = None):
        if username == 'anosh' and password == '123':
            try:
                user = User.objects.get(username = username)
            except User.DoesNotExist:
                user = User(username = username)
                user.set_password(password)
                user.save()
            return user     
        else:
            return None
    
    def get_user(self,user_id):
        try:
            return User.objects.get(pk = user_id)
        except User.DoesNotExist:
            return None