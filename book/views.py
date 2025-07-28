from rest_framework import permissions, viewsets, mixins, status, filters
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from permissions import IsStaffOrReadeOnly
from .filters import BookFilter
from .models import Books, BookImage, Star, Like, Comment
from .serializers import (
    BooksSerializer, BookImageSerializer, StarSerializer,
    CommentSerializer, LikeDetailSerializer, BooksLikeSerializer,
    StarAvgSerializer,
)

class BooksViewSet(viewsets.ModelViewSet):
    queryset = Books.objects.all()
    serializer_class = BooksSerializer
    permission_classes = [IsStaffOrReadeOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BookImageViewSet(viewsets.ModelViewSet):
    queryset = BookImage.objects.all()
    serializer_class = BookImageSerializer
    permission_classes = [IsStaffOrReadeOnly]

class StarViewSet(viewsets.ModelViewSet):
    queryset = Star.objects.all()
    serializer_class = StarSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        book_id = self.request.data.get('book_id')
        book = get_object_or_404(Books, id=book_id)
        serializer.save(user=self.request.user, book=book)

class BookStarAvgAPIView(APIView):
    def get(self, request):
        books = Books.objects.all()
        serializer = StarAvgSerializer(books, many=True)
        return Response(serializer.data)

class LikeAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        books = Books.objects.all()
        serializer = BooksLikeSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        book_id = request.data.get('book_id')
        book = get_object_or_404(Books, id=book_id)
        like, created = Like.objects.get_or_create(user=request.user, book=book)

        if created:
            return Response({"message": "Liked successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Already liked"}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        book_id = request.data.get('book_id')
        book = get_object_or_404(Books, id=book_id)
        like = Like.objects.filter(user=request.user, book=book).first()

        if like:
            like.delete()
            return Response({"message": "Unliked successfully"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "Like not found"}, status=status.HTTP_404_NOT_FOUND)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        book_id = self.request.data.get('book')
        serializer.save(user=self.request.user, book_id=book_id)

class BookFilterViewSet(viewsets.ModelViewSet):
    queryset = Books.objects.all()
    serializer_class = BooksSerializer
    permission_classes = [permissions.AllowAny]

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = BookFilter
    search_fields = ['title', 'description', 'author__name']
    ordering_fields = ['price', 'pages', 'publication_date']

