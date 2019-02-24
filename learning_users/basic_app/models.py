from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfileInfo(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # the above is a model class to add additonal information
    # that the default User doesn't have

    # Additional
    portfolio_site = models.URLField(blank=True)
    # blank=True, means that the user doesn't have to fill it out

    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)
    #upload_to='profile_pics' means that 'profile_pics' is a subdirectory
    # in the media folder we created, so create that folder under media
    # so now when people upload their pics, it will be directly saved
    # in profile_pics folder

    def __str__(self):
        return self.user.username
