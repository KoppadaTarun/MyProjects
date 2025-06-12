from books_app.models import AuthorModel, BookModel, ReviewsModel
from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework import serializers


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = AuthorModel
        fields = '__all__'





class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReviewsModel
        exclude = ['book',]
        # extra_kwargs = {
        #     'book':{
        #         'write_only':True
        #     }
        # }


class BookSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    # reviews = serializers.StringRelatedField(many=True, read_only=True)
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = BookModel
        fields = '__all__'