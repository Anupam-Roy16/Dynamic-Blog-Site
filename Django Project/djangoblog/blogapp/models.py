from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class author(models.Model):
    name=models.ForeignKey(User,on_delete=models.CASCADE)
    details=models.TextField()
    profile_picture=models.FileField()
    def __str__(self):
        return self.name.username

class category(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name


class article(models.Model):
    article_author=models.ForeignKey(author,on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    posted_on=models.DateTimeField(auto_now=False,auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True,auto_now_add=False)

    body=models.TextField()
    image=models.FileField() 
    category=models.ForeignKey(category,on_delete=models.CASCADE)

    def __str__(self):
        return self.title

