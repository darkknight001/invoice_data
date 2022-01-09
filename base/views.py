from functools import partial
import re
from django.http import response
from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from rest_framework.response import Response

from .models import Invoice
from .serializer import InvoiceSerializer
from base import serializer
# Create your views here.

@api_view(['GET'])
def getRoutes(request):
    routes = [
        {
           'endpoint': '/api/load_invoice',  
           'methods': ['POST'],
           'description': 'Client-side API, takes pdf file as request data, and returns the status',
        },
        {
           'endpoint': '/api/get_invoice_status',  
           'methods': ['GET'],
           'description': 'Client-side API, takes invoice_number as request data, and returns the status of digitization',
        },
        {
           'endpoint': '/api/process_invoice',  
           'methods': ['PUT'],
           'description': 'Internal API, to be used manualy or by other microservices to update the invoice data to database',
        },
        
    ]
    return Response(routes)

@api_view(['POST'])
def loadInvoice(request):
    parser_classes = [FileUploadParser]

    # Get invoice Number from pdf name
    data = request.data

    invoiceNumber = str(data.get('file')).split('.', 1)[0]
    data.setdefault('invoiceNumber', invoiceNumber)
    serializer = InvoiceSerializer(data=data)
    response = {}
    http_status = ''
    if serializer.is_valid():
        serializer.save()
        response['details'] = "File uploaded successfully"
        # response['data'] = serializer.data
        http_status=status.HTTP_201_CREATED
    else:
        response['details'] = "File upload failed."
        response['data'] = serializer.errors
        http_status=status.HTTP_400_BAD_REQUEST
        
    return Response(response, status=http_status)


@api_view(['GET'])
def getInvoiceStatus(request, invoiceNumber):
    response = {}
    status_code= ''

    try:
        invoiceObject = Invoice.objects.get(invoiceNumber=invoiceNumber)
        serializer = InvoiceSerializer(invoiceObject)

        if invoiceObject.isDigitized:
            response['status'] = 'success'
            status_code = status.HTTP_200_OK
            response['details'] = {
                'Status' : 'The document is processed.',
                'data': serializer.data
            }
        else:
            response['status'] = 'processing'
            status_code = status.HTTP_200_OK
            response['details'] = {
                'Status' : 'The document is still under processing.',
                'invoiceNumber': invoiceObject.invoiceNumber,
                'file': serializer.data.get('file')
            }
    
    except Invoice.DoesNotExist:
        response['status'] = "failed"
        status_code = status.HTTP_404_NOT_FOUND
        response['details'] = "Given invoice not found in database."
    return Response(response, status=status_code)


# Internal API
@api_view(['PUT'])
def updateInvoice(request, invoiceNumber):

    response = {}
    status_code= ''

    try:
        invoiceObject = Invoice.objects.get(invoiceNumber=invoiceNumber)
        
        # data = request.data

        # invoiceObject.vendor = data['vendor']
        # invoiceObject.buyer = data['buyer']
        # invoiceObject.billedAmt = data['billedAmt']
        # invoiceObject.billedDate = data['billedDate']
        # invoiceObject.items = data['items']
        # invoiceObject.isDigitized = data['isDigitized']

        # invoiceObject.save()

        serializer = InvoiceSerializer(instance=invoiceObject, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            response['details'] = "Details updated successfully"
            response['data'] = serializer.data
            status_code=status.HTTP_200_OK
        else:
            response['details'] = "Details update failed."
            response['errors'] = serializer.errors
            status_code=status.HTTP_400_BAD_REQUEST
    
    except Invoice.DoesNotExist:
        response['status'] = "failed"
        status_code = status.HTTP_404_NOT_FOUND
        response['details'] = "Given invoice not found in database."
    return Response(response, status=status_code)
