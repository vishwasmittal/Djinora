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
    # first_name = models.CharField(max_length=15)
    username = models.CharField(max_length=30)
    email = models.EmailField()

    def first_name(self):
        return self.name.split()[0]

    # def __str__(self):
    #     return str(self.eno) + '    ' + self.uid + '    ' + self.name

    # def save(self, force_insert=False, force_update=False, using=None,
    #          update_fields=None):
    #     if self.email == self.email2:
    #         self.email2 = None
    #
    #     super(SlackUser, self).save(force_insert=force_insert, force_update=force_insert, using=using,
    #                                 update_fields=update_fields)
