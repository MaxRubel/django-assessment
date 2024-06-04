from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Song, Artist, Genre, SongGenre

class SongSerializer(serializers.ModelSerializer):
    """JSON serializer for Songs"""

    class Meta:
        model = Song
        fields = ('id', 'title', 'artist', 'artist_id', 'album', 'length', 'genres')
        depth = 1 

class SongView(ViewSet):
    """Level up Song view"""

    def retrieve(self, request, pk):
        try:
            song = Song.objects.get(pk=pk)
            serializer = SongSerializer(song)

            return Response(serializer.data)
        except Song.DoesNotExist as ex:
                return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
    def list(self, request):
         songs = Song.objects.all()
         serializer = SongSerializer(songs, many=True)
         return Response(serializer.data)
    
    def create(self, request):
         song = Song.objects.create(
            title = request.data["title"],
            artist_id = request.data["artist_id"],
            album = request.data["album"],
            length = request.data["length"]
         )
         
         genre_ids = request.data.get("genre_ids", [])
         
         for genre_id in genre_ids:
            try:
                genre = Genre.objects.get(id=genre_id)
                SongGenre.objects.create(song=song, genre=genre)
            except Genre.DoesNotExist:
                pass

         serializer = SongSerializer(song)
         return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        song = Song.objects.get(pk=pk)
        song.title = request.data["title"]
        song.album = request.data["album"]
        song.length = request.data["length"]

        artist = Artist.objects.get(pk=request.data["artist_id"])
        song.artist = artist
        song.save()
        serializer = SongSerializer(song)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
         song = Song.objects.get(pk=pk)
         song.delete()
         return Response(None, status=status.HTTP_204_NO_CONTENT)