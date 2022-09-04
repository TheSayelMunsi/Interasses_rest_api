from itertools import product
from django.shortcuts import render


from django.shortcuts import render
from rest_framework import generics
import io, csv, pandas as pd
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializer
import csv
from django.core.files.storage import FileSystemStorage
from rest_framework import viewsets
from rest_framework.decorators import action
from django.core.files.base import ContentFile
from .models import Product
from rest_framework import filters



# Create your views here.
fs = FileSystemStorage(location='tmp/')

class ProductViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing Product.

    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends=[filters.SearchFilter]
    search_fields=['^category']
    


    @action(detail=False, methods=['POST'])
    def upload_data(self, request):
        """Upload data from CSV"""
        file = request.FILES["file"]

        content = file.read()  # these are bytes
        file_content = ContentFile(content)
        file_name = fs.save(
            "_tmp.csv", file_content
        )
        tmp_file = fs.path(file_name)

        csv_file = open(tmp_file, errors="ignore")
        reader = csv.reader(csv_file)
        next(reader)
        
        product_list = []
        for id_, row in enumerate(reader):
            (
                user,
                category,
                price,
                name,
                description,
                quantity
            ) = row
            product_list.append(
                Product(
                    user_id=user,
                    category=category,
                    price=price,
                    name=name,
                    description=description,
                    quantity=quantity,
                )
            )

        Product.objects.bulk_create(product_list)

        return Response("Successfully upload the data")