from django.db import models
# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    emailid = models.CharField(max_length=200, primary_key=True)


class Question(models.Model):
    id = models.IntegerField(primary_key=True)
    question = models.CharField(max_length=20000)
    caption = models.CharField(max_length=200)


class Submission(models.Model):
    s_id = models.IntegerField(primary_key=True)
    q_id = models.ForeignKey(Question)
    status = models.IntegerField()
    u_id = models.ForeignKey(User)
    lang = models.CharField(max_length=200)