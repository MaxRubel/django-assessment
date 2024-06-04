from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from tunaapi.models import Artist, Song
from rest_framework import serializers
from tunaapi.models import Artist, Song


class ArtistSerializer(serializers.ModelSerializer):
    """JSON serializer for Artists"""
    
    song_count = serializers.SerializerMethodField()

    class Meta:
        model = Artist
        fields = ('id', 'name', 'age', 'bio', 'song_count', 'songs')
        depth =1 

    def get_song_count(self, obj):
        return obj.song_count


class ArtistView(ViewSet):
    """Level up Artist view"""

    def retrieve(self, request, pk):
        try:
            artist = Artist.objects.get(pk=pk)
            serializer = ArtistSerializer(artist)
            return Response(serializer.data)
        except Artist.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
    def list(self, request):
        artists = Artist.objects.all()
        serializer = ArtistSerializer(artists, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        artist = Artist.objects.create(
            name=request.data["name"],
            age=request.data["age"],
            bio=request.data["bio"]
        )
        serializer = ArtistSerializer(artist)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        artist = Artist.objects.get(pk=pk)
        artist.name = request.data["name"]
        artist.age = request.data["age"]
        artist.bio = request.data["bio"]
        
        artist.save()
        serializer = ArtistSerializer(artist)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        artist = Artist.objects.get(pk=pk)
        artist.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
