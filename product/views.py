from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.views import APIView
from django.db.models import Avg

from .filters import ProductsFilter

from .serializers import ProductSerializer, ProductImagesSerializer

from .models import Product, ProductImages


# Create your views here.

class GetProduct(APIView) :
    def get(self,request,id):
        product = Product.objects.get(pk=id)
        serializer = ProductSerializer(product, many = False)
        return Response({"product":serializer.data})


class GetProducts(APIView):
    def get(self,request) :

        product = Product.objects.all()
        serializer = ProductSerializer(product, many = True)
        return Response({"product" : serializer.data})


class NewProduct(APIView):
    def post(self,request):
        data = request.data

        serializer = ProductSerializer(data = data)

        if serializer.is_valid() :

            product = Product.objects.create(**data)

            res = ProductSerializer(product, many = False)

            return Response({"product" : res.data})

        else :
            return Response(serializer.errors)


@api_view(['POST'])
def upload_product_images(request) :
    data = request.data
    files = request.FILES.getlist('images')

    images = []
    for f in files :
        image = ProductImages.objects.create(product = Product(data['product']), image = f)
        images.append(image)

    serializer = ProductImagesSerializer(images, many = True)

    return Response(serializer.data)


@api_view(['PUT'])
def update_product(request, pk) :
    product = get_object_or_404(Product, id = pk)

    # Check if the user is same - todo

    product.name = request.data['name']
    product.description = request.data['description']
    product.price = request.data['price']
    product.category = request.data['category']
    product.brand = request.data['brand']
    product.ratings = request.data['ratings']
    product.stock = request.data['stock']

    product.save()

    serializer = ProductSerializer(product, many = False)

    return Response({"product" : serializer.data})


@api_view(['DELETE'])
def delete_product(request, pk) :
    product = get_object_or_404(Product, id = pk)

    # Check if the user is same - todo

    args = {"product" : pk}
    images = ProductImages.objects.filter(**args)
    for i in images :
        i.delete()

    product.delete()

    return Response({'details' : 'Product is deleted'}, status = status.HTTP_200_OK)

class NewRiview(APIView):
    def post(self,request,id):
        user = request.user
        product = get_object_or_404(Product, id = pk)
        data = request.data

        review = product.reviews.filter(user = user)

        if data['rating'] <= 0 or data['rating'] > 5 :
            return Response({'error' : 'Please select rating between 1-5'}, status = status.HTTP_400_BAD_REQUEST)

        elif review.exists() :

            new_review = {'rating' : data['rating'], 'comment' : data['comment']}
            review.update(**new_review)

            rating = product.reviews.aggregate(avg_ratings = Avg('rating'))

            product.ratings = rating['avg_ratings']
            product.save()

            return Response({'detail' : 'Review Updated'})

        else :
            Review.objects.create(
                user = user,
                product = product,
                rating = data['rating'],
                comment = data['comment']
            )

            rating = product.reviews.aggregate(avg_ratings = Avg('rating'))

            product.ratings = rating['avg_ratings']
            product.save()

            return Response({'detail' : 'Review Posted'})
