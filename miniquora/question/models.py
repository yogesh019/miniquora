from django.db import models
from account.models import MyUser

class Question(models.Model):
    title=models.CharField(max_length=100,default='')
    text=models.TextField(max_length=1024,default='')
    created_on=models.DateTimeField(auto_now_add=True)
    created_by=models.ForeignKey(MyUser,related_name='questions_created')
    upvoted_by=models.ManyToManyField(MyUser,related_name="questions_upvoted",blank=True)

# Create your models here.
