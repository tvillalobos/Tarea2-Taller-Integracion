# models.py
from django.db import models
from base64 import b64encode





class Artist(models.Model):
    cid = models.TextField(unique=True)
    name = models.TextField(default='Artista')
    age = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        name_split = self.name
        encoded = b64encode(name_split.encode()).decode('utf-8')
        self.cid = encoded[:22]
        super(Artist, self).save()

    def __str__(self):
        return self.name

class Album(models.Model):
    artist_id = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='albums')
    cid = models.TextField(unique=True)
    name = models.TextField()
    genre = models.TextField()
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        name_split = f"{self.name}:{self.artist_id.cid}"
        encoded = b64encode(name_split.encode()).decode('utf-8')
        self.cid = encoded[:22]
        super(Album, self).save()

class Song(models.Model):
    album_id = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='songs')
    cid = models.TextField(unique=True)
    name = models.TextField()
    duration = models.FloatField()
    times_played = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        name_split = f"{self.name}:{self.album_id.cid}"
        encoded = b64encode(name_split.encode()).decode('utf-8')
        self.cid = encoded[:22]
        super(Song, self).save()

    def __str__(self):
        return self.name