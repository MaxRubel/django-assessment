from django.db import models

class Artist(models.Model):
    name = models.CharField(max_length=150)
    age = models.IntegerField()
    bio = models.CharField(max_length=400)

    @property
    def song_count(self):
        return self.songs.count()
    
    @property
    def songs(self):
        return self.songs.all()