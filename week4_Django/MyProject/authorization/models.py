from django.db import models

class Authorization(models.Model):
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200, default = "")
    done = models.BooleanField(default=False)
    joined_date = models.DateField(null=True)
    phone = models.CharField(max_length=20, default = "")

    def __str__(self):
        return f"{self.firstname} {self.lastname}"