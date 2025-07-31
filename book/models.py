from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import  gettext_lazy as _
from django.contrib.auth import get_user_model
from django.utils import timezone
from user.models import Author, Translator

User = get_user_model()

class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)

class Books(BaseModel):
    class LanguageChoices(models.TextChoices):
        UZBEK = 'uz', 'Uzbek'
        ENGLISH = 'en', 'English'
        RUSSIAN = 'ru', 'Russian'
        ARABIC = 'ar', 'Arabic'
        TURKISH = 'tr', 'Turkish'
        FRENCH = 'fr', 'French'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')
    title = models.CharField(max_length=50)
    info = models.TextField()
    isbn = models.CharField(max_length=20, unique=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    book_language = models.CharField(
        max_length=10,
        choices=LanguageChoices.choices,
        default=LanguageChoices.UZBEK
    )
    writing = models.CharField(max_length=50, verbose_name=_('Yozuv'))                             # Yozuv
    translator = models.ForeignKey(Translator, on_delete=models.CASCADE, null=True, blank=True)    # Tarjimon
    pages = models.IntegerField(validators=[MinValueValidator(0)] )
    publisher = models.CharField(max_length=50)                                                    # Nashriyot
    cover = models.CharField(max_length=50)                                                        # Muqovasi
    publication_date = models.DateField()                                                          # Chop etilgan yili
    page_surface = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.title} - {self.author}"

class BookStock(BaseModel):
    book = models.ForeignKey(Books, on_delete=models.CASCADE, related_name='stocks')
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.book}: {self.created_at} - {self.price}"


class BookImage(BaseModel):
    book = models.ForeignKey(Books, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='book_images/')

    def __str__(self):
        return f"Image of {self.book.title}"

class Star(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE, related_name='star')
    rating = models.PositiveSmallIntegerField(validators=[MaxValueValidator(5)])

    class Meta:
        unique_together = ['book', 'user']

    def __str__(self):
        return f"{self.user} ⭐ {self.rating} - {self.book.title}"

class Comment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE, related_name='comment')
    text = models.TextField()


    def __str__(self):
        return f"Comment by {self.user} on {self.book.title}"

class Like(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE, related_name='like')

    class Meta:
        unique_together = ['book', 'user']

class BookCategory(BaseModel):
    CATEGORIES = (
        ('fiction', 'Fiction'),                                                             # Badiiy adabiyotlar
        ('psychology_and_personal_development', 'Psychology and personal development'),     # Psixologiya va shaxsiy rivojlanish
        ('business', 'Business'),                                                           # Biznes kitoblar
        ('Children_literature', "Children's literature"),                                   # Bolalar adabiyoti
        ('religious_literature', 'Religious literature'),                                   # Diniy adabiyotlar
        ('books_in_russian', 'Books in Russian'),                                           # Rus tilidagi kitoblar
        ('sducational_literature', 'Educational literature'),                               # O‘quv adabiyoti
        ('top_100_bestsellers', 'TOP-100 bestsellers'),                                     # TOP-100 ta bestseller
        ('bestseller_sets', 'Bestseller sets'),                                             # Bestseller to‘plamlar
        ('detective', 'Detective'),                                                         # Detektiv
        ('science_fiction', 'Science Fiction'),                                             # Ilmiy fantastika
        ('politics', 'Politics'),                                                           # Siyosat
        ('biography', 'Biography'),                                                         # Biografiya
        ('book_gift_sets', 'Book gift sets'),                                               # Kitobli sovg‘a to‘plamlari
        ('turkish_literature', 'Turkish literature'),                                       # Turk adabiyoti
        ('history', 'History'),                                                             # Tarix
        ('books_in_english', 'Books in English'),                                           # Ingliz tilida kitoblar
        ('books_for_collectors', 'Books for collectors')                                    # Kollektorlar uchun kitoblar
    )

    book = models.ForeignKey(Books, on_delete=models.CASCADE, related_name='book_category')
    category = models.CharField(max_length=50, choices=CATEGORIES)

    class Meta:
        unique_together = ['book', 'category']

    def __str__(self):
        return f"{self.book} - {self.category}"
