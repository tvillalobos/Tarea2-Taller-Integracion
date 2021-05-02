# myapi/urls.py
from django.urls import include, path, re_path
from .views import ArtistViewSet, AlbumViewSet, ArtistAlbumsViewSet, AlbumTracksViewSet, SongViewSet, ArtistTracksViewSet,UpdateSong, UpdateArtist, UpdateAlbum

from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'artists/?', ArtistViewSet)
router.register(r'albums/?', AlbumViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    re_path(r'^tracks/(?P<cid>.+)/play', UpdateSong.as_view(), name='updatesong'),
    re_path(r'^artists/(?P<cid>.+)/albums/play', UpdateArtist.as_view(), name='updateartist'),
    re_path(r'^albums/(?P<cid>.+)/tracks/play', UpdateAlbum.as_view(), name='updatealbum'),
    re_path(r'^artists/(?P<cid>.+)/albums', ArtistAlbumsViewSet.as_view({'get': 'list', 'post': 'create'}), name='albumsbyartist'),
    re_path(r'^albums/(?P<cid>.+)/tracks', AlbumTracksViewSet.as_view({'get': 'list', 'post': 'create'}), name='tracksofalbum'),
    path('tracks', SongViewSet.as_view({'get': 'list'}), name='trackslist'),
    re_path(r'^tracks/(?P<cid>.+)', SongViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'}), name='trackdetail'),
    re_path(r'^artists/(?P<cid>.+)/tracks', ArtistTracksViewSet.as_view({'get': 'list'}), name='tracksofartist'),

]