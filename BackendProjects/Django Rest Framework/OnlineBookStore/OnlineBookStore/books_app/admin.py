from django.contrib import admin
from books_app.models import AuthorModel, BookModel, ReviewsModel


admin.site.register(AuthorModel)
admin.site.register(BookModel)
admin.site.register(ReviewsModel)

# Register your models here.
