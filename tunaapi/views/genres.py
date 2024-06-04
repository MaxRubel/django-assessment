from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Genre, Artist

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ('id', 'name', 'age', 'bio')

class GenreSerializer(serializers.ModelSerializer):
    """JSON serializer for Songs"""

    songs = serializers.SerializerMethodField()

    class Meta:
        model = Genre
        fields = ('id', 'description', 'songs')
        depth = 2 
    
    def get_songs(self, obj):
        songs = obj.songs.all()
        song_data = []

        for song in songs:
            artist = Artist.objects.get(id=song.artist_id)
            artist_serializer = ArtistSerializer(artist)
            song_data.append({
                'id': song.id,
                'title': song.title,
                'album': song.album,
                'length': song.length,
                'artist_id': song.artist_id,
                'artist': artist_serializer.data
            })
            
        return song_data

class GenreView(ViewSet):
    """Genre view"""

    def retrieve(self, request, pk):
        try:
            genre = Genre.objects.get(pk=pk)
            serializer = GenreSerializer(genre)

            return Response(serializer.data)
        except Genre.DoesNotExist as ex:
                return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
    def list(self, request):
         """function to get all Genres"""
         genre = Genre.objects.all()
         serializer = GenreSerializer(genre, many=True)
         return Response(serializer.data)
    
    def create(self, request):
         """function to create a Genre"""
         genre = Genre.objects.create(
            description = request.data["description"],
         )
         serializer = GenreSerializer(genre)
         return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        """function to update a Genre"""
        genre = Genre.objects.get(pk=pk)
        genre.description = request.data["description"]
        
        genre.save()
        serializer = GenreSerializer(genre)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
         """function to delete a Genre"""
         genre = Genre.objects.get(pk=pk)
         genre.delete()
         return Response(None, status=status.HTTP_204_NO_CONTENT)