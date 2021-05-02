from rest_framework import serializers

from .models import Artist, Album, Song

BASE_URL = 'https://t2-tvillalobos.herokuapp.com/'

# class NewSerializer(serializers.ModelSerializer):

#     newspaper = serializers.SerializerMethodField('obtain_newspaper')
#     img_source = serializers.SerializerMethodField('obtain_source')
#     img_url = serializers.SerializerMethodField('add_http')

    
#     def obtain_newspaper(self, new): 
#         if "soychile.cl" in new.link:
#             link = new.link.strip("http://www.soychile.cl/").strip("https://www.soychile.cl/").split("/")[0]
#             name = "soy" + link.replace("-", "").lower()
#             return name
#         return "emol"
#     def obtain_source(self, new): 
#         if "soychile.cl" in new.link:
#             return "soychile"
#         return "emol"

#     def add_http(self, n):
#         if "emol" in n.link:
#             return "https://" + n.img_link
#         return n.img_link


#     class Meta:
#         model = New
#         fields = ('id', 'headline', 'lead', 'body', 'link', 'img_link', 'news_date', 'newspaper', 'img_source', 'img_url')

class ArtistSerializer(serializers.HyperlinkedModelSerializer):
    
    self = serializers.SerializerMethodField('add_self')
    albums = serializers.SerializerMethodField('add_albums')
    tracks = serializers.SerializerMethodField('add_tracks')
    id = serializers.SerializerMethodField('add_id')


    def add_id(self, a):
        return a.cid

    def add_self(self, a):
        return f"{BASE_URL}artists/{a.cid}"

    def add_albums(self, a):
        return f"{BASE_URL}artists/{a.cid}/albums"
        
    def add_tracks(self, a):
        return f"{BASE_URL}artists/{a.cid}/tracks"


    class Meta:
        model = Artist
        fields = ('id', 'name', 'age', 'albums', 'tracks', 'self')


class AlbumSerializer(serializers.HyperlinkedModelSerializer):
    
    self = serializers.SerializerMethodField('add_self')
    artist = serializers.SerializerMethodField('add_artists')
    tracks = serializers.SerializerMethodField('add_tracks')
    id = serializers.SerializerMethodField('add_id')


    def add_id(self, a):
        return a.cid

    def add_self(self, a):
        return f"{BASE_URL}albums/{a.cid}"

    def add_artists(self, a):
        return f"{BASE_URL}artists/{a.artist_id.cid}"
        
    def add_tracks(self, a):
        return f"{BASE_URL}albums/{a.cid}/tracks"

    class Meta:
        model = Album
        fields = ('name', 'genre', 'tracks', 'artist', 'self')

class SongSerializer(serializers.HyperlinkedModelSerializer):
    

    id = serializers.SerializerMethodField('add_id')
    album_id = serializers.SerializerMethodField('add_album_id')
    artist = serializers.SerializerMethodField('add_artist')
    album = serializers.SerializerMethodField('add_album')
    self = serializers.SerializerMethodField('add_self')


    def add_id(self, a):
        return a.cid

    def add_self(self, a):
        return f"{BASE_URL}tracks/{a.cid}"

    def add_album(self, a):
        return f"{BASE_URL}albums/{a.album_id.cid}"

    def add_album_id(self, a):
        return a.album_id.cid

    def add_artist(self, a):
        return f"{BASE_URL}artists/{a.album_id.artist_id.cid}"
    

        
    # def add_tracks(self, a):
    #     return f"{BASE_URL}albums/{a.cid}/tracks"

    class Meta:
        model = Song
        fields = ('id', 'name', 'times_played', 'self', 'album_id', 'artist', 'album', 'duration')