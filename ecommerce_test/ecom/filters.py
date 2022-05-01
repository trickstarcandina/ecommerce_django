import django_filters
from django_filters import CharFilter, NumberFilter

from .models import *

class CakeItemFilter(django_filters.FilterSet):
	cake = CharFilter(field_name="cake")
	price = NumberFilter(field_name="price", lookup_expr='gte')

	