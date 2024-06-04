from django.db import models
from .artist import Artist
from .genre import Genre

class Song(models.Model):
    title = models.CharField(max_length=150)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='songs')
    album = models.CharField(max_length=150)
    length = models.IntegerField()
    genres = models.ManyToManyField(Genre, through='SongGenre', related_name='songs')

    @property
    def artist_id(self):
        return self.artist.id