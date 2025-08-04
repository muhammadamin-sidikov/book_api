from rest_framework import permissions, viewsets, mixins, status, filters
from rest_framework.generics import get_object_or_404
from django.core.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from permissions import IsStaffOrReadeOnly
from .filters import BookFilter
from .models import Books, BookImage, Star, Like, Comment, BookStock, BookCategory, Category
from .serializers import (
    BooksSerializer, BookImageSerializer, StarSerializer,
    CommentSerializer, LikeDetailSerializer, BooksLikeSerializer,
    StarAvgSerializer, BookStockSerializer, BookCategorySerializer,
    CategorySerializer,
)

class BooksViewSet(viewsets.ModelViewSet):
    queryset = Books.objects.all()
    serializer_class = BooksSerializer
    permission_classes = [IsStaffOrReadeOnly]

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = BookFilter
    search_fields = ['title', 'description', 'author__name']
    ordering_fields = ['price', 'pages', 'publication_date']

    def get_queryset(self):
        if self.request.user.is_staff:
            return Books.objects.all()
        return Books.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.user != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("Siz faqat o'zingizning kitoblaringizni tahrirlashingiz mumkin.")
        serializer.save()

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
        serializer = BooksLikeSerializer(books, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        book_id = request.data.get('book_id')
        book = get_object_or_404(Books, id=book_id)
        like, created = Like.objects.get_or_create(user=request.user, book=book)

        if created:
            return Response({"message": "Liked successfully"}, status=status.HTTP_201_CREATED)
        return Response({"message": "Already liked"}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        book_id = request.data.get('book_id')
        book = get_object_or_404(Books, id=book_id)
        like = Like.objects.filter(user=request.user, book=book).first()

        if like:
            like.delete()
            return Response({"message": "Unliked successfully"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Like not found"}, status=status.HTTP_404_NOT_FOUND)

class BookStockViewSet(viewsets.ModelViewSet):
    queryset = BookStock.objects.all()
    serializer_class = BookStockSerializer
    permission_classes = [permissions.IsAdminUser]

class BookCategoryViewSet(viewsets.ModelViewSet):
    queryset = BookCategory.objects.all()
    serializer_class = BookCategorySerializer
    permission_classes = [IsStaffOrReadeOnly]

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsStaffOrReadeOnly]

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Comment.objects.all()
        return Comment.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        book_id = self.request.data.get('book')
        serializer.save(user=self.request.user, book_id=book_id)

    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.user != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("Faqat o'zingizning izohlaringizni tahrirlashingiz mumkin.")
        serializer.save()

