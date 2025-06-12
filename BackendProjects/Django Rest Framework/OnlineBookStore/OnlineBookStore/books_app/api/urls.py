from rest_framework.urls import path
from .views import (AuthorDetailView, AuthorView, BookDetailView, BookView, ReviewDetailView, ReviewView)

urlpatterns = [
    path('list/', BookView.as_view(), name='book_list'),
    path('<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('author/list/', AuthorView.as_view(), name='author_list'),
    path('author/<int:pk>/', AuthorDetailView.as_view(), name='author_detail'),
    path('review/list/', ReviewView.as_view(), name='review_list'),
    path('review/<int:pk>/', ReviewDetailView.as_view(), name='review_detail')
]
