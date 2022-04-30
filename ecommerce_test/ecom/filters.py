import django_filters
from django_filters import CharFilter, NumberFilter

from .models import *

class CakeFilter(django_filters.FilterSet):
	name = CharFilter(field_name="name")
	price = NumberFilter(field_name="price", lookup_expr='gte')

	