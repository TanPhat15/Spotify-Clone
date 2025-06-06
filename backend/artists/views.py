from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Artist
from .serializers import ArtistSerializer

class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

    # Tìm kiếm nghệ sĩ theo tên
    def get_queryset(self):
        queryset = Artist.objects.all()
        name = self.request.query_params.get('name', None)
        
        if name:
            queryset = queryset.filter(name__icontains=name)
        
        return queryset

    # Tạo một nghệ sĩ mới
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Cập nhật thông tin nghệ sĩ
    def update(self, request, *args, **kwargs):
        artist = self.get_object()
        serializer = self.get_serializer(artist, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Xóa một nghệ sĩ
    def destroy(self, request, *args, **kwargs):
        artist = self.get_object()
        artist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_artist_name_by_id(artist_id):
        try:
            return Artist.objects.get(id=artist_id).name
        except Artist.DoesNotExist:
            return "Unknown Artist"
