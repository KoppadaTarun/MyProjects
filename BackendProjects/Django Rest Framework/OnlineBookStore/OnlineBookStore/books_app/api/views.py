from rest_framework.views import APIView
from rest_framework import status
from .serializer import BookSerializer, AuthorSerializer, ReviewSerializer
from books_app.models import AuthorModel, BookModel, ReviewsModel
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


class BookView(APIView):
    def get(self, request):
        books = BookModel.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BookSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)

class BookDetailView(APIView):

    def get(self, request, pk):
        book = get_object_or_404(BookModel, pk=pk)

        serializer = BookSerializer(book)
        return Response(serializer.data, status= status.HTTP_200_OK)

    def put(self, request, pk):
        book = get_object_or_404(BookModel, pk=pk)
        serializer = BookSerializer(book , request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        book = get_object_or_404(BookModel, pk=pk)
        book.delete()

        return Response({"message":"Deleted Successfully"}, status=status.HTTP_204_NO_CONTENT)



class AuthorView(APIView):
    def get(self, request):
        authors = AuthorModel.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AuthorSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)

class AuthorDetailView(APIView):

    def get(self, request, pk):
        author = get_object_or_404(AuthorModel, pk=pk)

        serializer = AuthorSerializer(author)
        return Response(serializer.data, status= status.HTTP_200_OK)

    def put(self, request, pk):
        author = get_object_or_404(AuthorModel, pk=pk)
        serializer = AuthorSerializer(author , request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        book = get_object_or_404(AuthorModel, pk=pk)
        book.delete()

        return Response({"message":"Deleted Successfully"}, status=status.HTTP_204_NO_CONTENT)



class ReviewView(APIView):
    def get(self, request):
        reviews = ReviewsModel.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ReviewSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)

class ReviewDetailView(APIView):

    def get(self, request, pk):
        book = get_object_or_404(ReviewsModel, pk=pk)

        serializer = ReviewSerializer(book)
        return Response(serializer.data, status= status.HTTP_200_OK)

    def put(self, request, pk):
        review = get_object_or_404(ReviewsModel, pk=pk)
        serializer = ReviewSerializer(review , request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        book = get_object_or_404(ReviewsModel, pk=pk)
        book.delete()

        return Response({"message":"Deleted Successfully"}, status=status.HTTP_204_NO_CONTENT)





