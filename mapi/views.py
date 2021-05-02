from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from  django.db import IntegrityError
from django.http import Http404



from .serializers import ArtistSerializer, AlbumSerializer, SongSerializer
from .models import Artist, Album, Song


class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all().order_by('name')
    serializer_class = ArtistSerializer
    lookup_field = "cid"
    lookup_value_regex = "[^/]+"  

    def create(self, request, *args, **kwargs):
        try:
            return super(ArtistViewSet, self).create(request, *args, **kwargs)
        except IntegrityError:
            artist = Artist.objects.get(name=request.data["name"])
            data = ArtistSerializer(artist).data
            return Response(data=data, status=status.HTTP_409_CONFLICT)



class ArtistAlbumsViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.filter()
    serializer_class = AlbumSerializer

    def partial_update(self, request, *args, **kwargs):
            instance = self.get_object()
            for a in instance.album_set.all():
                for t in a.song_set.all():
                    serializer = SongSerializer(t, data=request.data, partial=True)
                    t.times_played += t.times_played + 1
                    serializer.save()


            return Response(serializer.data)

    def get_queryset(self):
        try:
            artist = Artist.objects.get(cid=self.kwargs.get('cid'))
        except Artist.DoesNotExist:
            raise Http404

        artist_cid = self.kwargs.get('cid')
        return self.queryset.filter(artist_id__cid=artist_cid)

    def perform_create(self, serializer):
        
        artist = Artist.objects.get(cid=self.kwargs.get('cid'))
        print("ARTISTAAAAAAAADSJSAJDJASJDASJADSJDSAJADSJA:",artist)
        serializer.save(artist_id=artist)

    def create(self, request, *args, **kwargs):
        try:
            artist = Artist.objects.get(cid=self.kwargs.get('cid'))
        except Artist.DoesNotExist:
            return Response(data={"error": "El artista no existe"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        try:
            return super(ArtistAlbumsViewSet, self).create(request, *args, **kwargs)

        except IntegrityError:
            album = Album.objects.get(name=request.data["name"], artist_id__cid=self.kwargs.get('cid'))
            data = AlbumSerializer(album).data
            return Response(data=data, status=status.HTTP_409_CONFLICT)


class ArtistTracksViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.filter()
    serializer_class = SongSerializer

    # def partial_update(self, request, *args, **kwargs):
    #         instance = self.get_object()
    #         for a in instance.album_set.all():
    #             for t in a.song_set.all():
    #                 serializer = SongSerializer(t, data=request.data, partial=True)
    #                 t.times_played += t.times_played + 1
    #                 serializer.save()


    #         return Response(serializer.data)

    def get_queryset(self):
        try:
            artist = Artist.objects.get(cid=self.kwargs.get('cid'))
        except Artist.DoesNotExist:
            raise Http404
        artist_id = self.kwargs.get('cid')
        artist = Artist.objects.get(cid=artist_id)
        data = []
        for a in artist.albums.all():
            for s in a.songs.all():
                data.append(s)
        return data










class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all().order_by('name')
    serializer_class = AlbumSerializer
    lookup_field = "cid"
    lookup_value_regex = "[^/]+" 

    def create(self, request, *args, **kwargs):
        try:
            return super(AlbumViewSet, self).create(request, *args, **kwargs)
        except IntegrityError:
            album = Album.objects.get(name=request.data["name"])
            data = ArtistSerializer(artist).data
            return Response(data=data, status=status.HTTP_409_CONFLICT)





class AlbumTracksViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.filter()
    serializer_class = SongSerializer

    # def partial_update(self, request, *args, **kwargs):
    #         instance = self.get_object()
    #         for a in instance.album_set.all():
    #             for t in a.song_set.all():
    #                 serializer = SongSerializer(t, data=request.data, partial=True)
    #                 t.times_played += t.times_played + 1
    #                 serializer.save()


    #         return Response(serializer.data)

    def get_queryset(self):

        try:
            album = Album.objects.get(cid=self.kwargs.get('cid'))
        except Album.DoesNotExist:
            print("ENTRE ACAaAAAAAAAAAAAAAAA!")
            raise Http404

        album_cid = self.kwargs.get('cid')
        return self.queryset.filter(album_id__cid=album_cid)

    def perform_create(self, serializer):

        
        try:
            album = Album.objects.get(cid=self.kwargs.get('cid'))
        except Album.DoesNotExist:
            raise Http404
        serializer.save(album_id=album)

    def create(self, request, *args, **kwargs):

        try:
            album = Album.objects.get(cid=self.kwargs.get('cid'))
        except Album.DoesNotExist:
            return Response(data={"error": "El album no existe"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            
        try:
            album = Album.objects.get(cid=self.kwargs.get('cid'))
        except Album.DoesNotExist:
            raise Http404

        try:

            return super(AlbumTracksViewSet, self).create(request, *args, **kwargs)

        except IntegrityError:
            song = Song.objects.get(name=request.data["name"], album_id__cid=self.kwargs.get('cid'))
            data = SongSerializer(song).data
            return Response(data=data, status=status.HTTP_409_CONFLICT)



class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all().order_by('name')
    serializer_class = SongSerializer
    lookup_field = "cid"
    lookup_value_regex = "[^/]+" 


class UpdateSong(APIView):


    def put(self, request, cid, format=None):

        obj = Song.objects.get(cid=cid)
        aux = obj.times_played
        obj.times_played = aux + 1
        obj.save()
        data = SongSerializer(obj).data
        return Response(data=data, status=status.HTTP_200_OK)



class UpdateArtist(APIView):


    def put(self, request, cid, format=None):

        try:
            artist = Artist.objects.get(cid=cid)
        except Artist.DoesNotExist:
            raise Http404
        songs = []
        for a in artist.albums.all():
            for s in a.songs.all():
                songs.append(s)
                aux = s.times_played
                s.times_played = aux + 1
                s.save()
        data = [SongSerializer(s).data for s in songs]
        return Response(data=data, status=status.HTTP_200_OK)


class UpdateAlbum(APIView):


    def put(self, request, cid, format=None):

        try:
            album = Album.objects.get(cid=cid)
        except Album.DoesNotExist:
            raise Http404
        songs = []
        for s in album.songs.all():
            songs.append(s)
            aux = s.times_played
            s.times_played = aux + 1
            s.save()
        data = [SongSerializer(s).data for s in songs]
        return Response(data=data, status=status.HTTP_200_OK)