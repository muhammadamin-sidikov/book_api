import django_filters
from .models import Books

class BookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    category = django_filters.CharFilter(field_name='book_category__category', lookup_expr='icontains')

    price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')
    price__gte = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price__lte = django_filters.NumberFilter(field_name='price', lookup_expr='lte')

    pages__gt = django_filters.NumberFilter(field_name='pages', lookup_expr='gt')
    pages__lt = django_filters.NumberFilter(field_name='pages', lookup_expr='lt')
    pages__gte = django_filters.NumberFilter(field_name='pages', lookup_expr='gte')
    pages__lte = django_filters.NumberFilter(field_name='pages', lookup_expr='lte')

    publication_date__gt = django_filters.DateFilter(field_name='publication_date', lookup_expr='gt')
    publication_date__lt = django_filters.DateFilter(field_name='publication_date', lookup_expr='lt')

    class Meta:
        model = Books
        fields = '__all__'