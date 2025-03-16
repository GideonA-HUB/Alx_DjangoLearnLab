import django_filters
from .models import Book

class BookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains', label='Title')
    author = django_filters.CharFilter(field_name='author', lookup_expr='icontains', label='Author')
    publication_year = django_filters.NumberFilter(field_name='publication_year', lookup_expr='exact', label='Publication Year')

    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']