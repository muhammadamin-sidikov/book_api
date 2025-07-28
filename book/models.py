from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import  gettext_lazy as _
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Books(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')
    title = models.CharField(max_length=50)
    info = models.TextField()
    isbn = models.CharField(max_length=20, unique=True)
    author = models.CharField(max_length=50)
    book_language = models.CharField(max_length=50)
    writing = models.CharField(max_length=50, verbose_name=_('Yozuv'))     # Yozuv
    translator = models.CharField(max_length=50, null=True, blank=True)                           # Tarjimon
    pages = models.IntegerField(validators=[MinValueValidator(0)] )
    publisher = models.CharField(max_length=50)                            # Nashriyot
    cover = models.CharField(max_length=50)                                # Muqovasi
    publication_date = models.DateField()                                  # Chop etilgan yili
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
    page_surface = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.title} - {self.author}"


class BookImage(models.Model):
    book = models.ForeignKey(Books, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='book_images/')

    def __str__(self):
        return f"Image of {self.book.title}"

class Star(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE, related_name='star')
    rating = models.PositiveSmallIntegerField(validators=[MaxValueValidator(5)])

    class Meta:
        unique_together = ['book', 'user']

    def __str__(self):
        return f"{self.user} ⭐ {self.rating} - {self.book.title}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE, related_name='comment')
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return f"Comment by {self.user} on {self.book.title}"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE, related_name='like')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ['book', 'user']

