from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from account.models import User

# Create your models here.

class Post(models.Model):
    Title =models.CharField(max_length= 50)
    Content = models.TextField(max_length=1000)
    Date = models.DateTimeField(default= timezone.now)
    user = models.ForeignKey(User, on_delete= models.CASCADE)

    class Meta:
        ordering= ['-Date']