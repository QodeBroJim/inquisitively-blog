from django.db import models

class Signup(models.Model):
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class AccessTutorialSignup(models.Model):
    email = models.EmailField()
    first_name = models.TextField(max_length=100)
    last_name = models.TextField(max_length=100)
    hobby = models.TextField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    