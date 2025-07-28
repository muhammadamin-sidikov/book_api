from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (BooksViewSet, BookImageViewSet,
                    StarViewSet, CommentViewSet,
                    LikeAPIView, BookStarAvgAPIView,
                    BookFilterViewSet)

router = DefaultRouter()
router.register(r'filter', BookFilterViewSet, basename='books')
router.register('images', BookImageViewSet)
router.register('stars', StarViewSet)
router.register('comments', CommentViewSet)
router.register('book', BooksViewSet, basename='all-books')

urlpatterns = [
    path('likes/', LikeAPIView.as_view()),
    path('likes/<int:book_id>/', LikeAPIView.as_view()),

    path('stars-avg/', BookStarAvgAPIView.as_view()),
]

urlpatterns += router.urls