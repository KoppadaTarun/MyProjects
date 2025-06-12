from django.db import models

class AuthorModel(models.Model):
    Name = models.CharField(max_length=20)
    age = models.IntegerField()
    bio = models.TextField(max_length = 300)

    def __str__(self):
        return self.Name


class BookModel(models.Model):

    title = models.CharField(max_length= 50)
    author = models.ForeignKey(AuthorModel, on_delete=models.CASCADE)
    description = models.TextField(max_length=300)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.IntegerField()

    def __str__(self):
        return self.title

class ReviewsModel(models.Model):
    book = models.ForeignKey(BookModel, on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField()
    comment = models.CharField(max_length=225)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment
