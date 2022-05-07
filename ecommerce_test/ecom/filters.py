from unicodedata import name
import django_filters
from django_filters import CharFilter, NumberFilter

from .models import *

class CakeFilter(django_filters.FilterSet):
	name = CharFilter(field_name="name")
	expriration = NumberFilter(field_name="expiry")

class DrinkFilter(django_filters.FilterSet):
	name = CharFilter(field_name="name")
	expriration = NumberFilter(field_name="expiry")

class ShippmentFilter(django_filters.FilterSet):
	name = CharFilter(field_name="name")