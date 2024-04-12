from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#this is where we create out data bases 


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Rooms(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True) #  mthan blank true kiyl kiynne forms wala description kiyl thibboth fomr sambndwa eka his wa thiyenna puluwan kiyna eki
    # participants = 
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated' , '-created'] #me class ekn krnne aluthin add una rooms aluthin ad una piliwelat web page eka pennana eki, meket '-' lakuna updated and created variable issrahin daala thiynne eki , eke theruma aluthin add una piliwela kiyna eki , e ira nattnm mulin add una piliwelat thami web page eke dis wenne 

 

    #creating a string representation of the room table's records
    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50]

