from rest_framework.pagination import CursorPagination
from .constants import DEFAULT_SORT_PROPERTY

class CustomCursorPagination(CursorPagination):
    page_size = 3
    ordering = DEFAULT_SORT_PROPERTY