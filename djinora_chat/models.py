from django.db import models


class TempPublicUser(models.Model):
    username = models.CharField(max_length=36)
    permanent = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class TempMessage(models.Model):
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(TempPublicUser, on_delete=models.CASCADE, related_name='user')
    bot = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username + ": " + self.message


class SlackUser(models.Model):
    uid = models.CharField(max_length=9, primary_key=True)
    name = models.CharField(max_length=30)
    username = models.CharField(max_length=30)
    email = models.EmailField()

    def __str__(self):
        return self.uid

    def first_name(self):
        return self.name.split()[0]
