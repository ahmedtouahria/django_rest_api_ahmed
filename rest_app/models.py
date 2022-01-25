from django.db import models

# Create your models here.
class Movies(models.Model):
    sall_num = models.CharField(max_length=10)
    movie    = models.CharField(max_length=100)
    date     = models.DateTimeField()
    def __str__(self):
        return self.movie
class Guest(models.Model):
    name     = models.CharField(max_length=50)
    mobile   = models.CharField(max_length=10)    
    def __str__(self):
        return self.name
class Reservation(models.Model):
    movie = models.ForeignKey(Movies,related_name="reserved", on_delete=models.CASCADE)
    guest = models.ForeignKey(Guest, related_name='reserved', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.movie} reserved by {self.guest}" 

   
    
    