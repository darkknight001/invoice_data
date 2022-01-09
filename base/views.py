from functools import partial
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

# Internal API, for debug purpose
@api_view(['GET'])
def getRoutes(request):
    routes = [
        {
           'endpoint': '/api/load_invoice',  
           'methods': ['POST'],
           'description': 'Client-side API, takes pdf file as request data, and returns the status',
        },
        {
           'endpoint': '/api/get_invoice_status/<invoice_number>',  
           'methods': ['GET'],
           'description': 'Client-side API, takes invoice_number as request data, and returns the status of digitization',
        },
        {
           'endpoint': '/api/update_invoice/<invoice_number>',  
           'methods': ['PUT'],
           'description': 'Internal API, to be used manualy or by other microservices to update the invoice data to database',
        },
        
    ]
    return Response(routes)

# Customer-end API
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
    
    # Check if file type is valid
    if serializer.is_valid():
        serializer.save()
        response['status'] = "File uploaded successfully"
        response['details'] = {
                'invoiceNumber': serializer.data.get('invoiceNumber'),
                'file': serializer.data.get('file'),
                'isDigitized': serializer.data.get('isDigitized'),
                'created_timestamp': serializer.data.get('created_timestamp'),
        }
        http_status=status.HTTP_201_CREATED
    else:
        response['status'] = "File upload failed."
        response['errors'] = serializer.errors
        http_status=status.HTTP_400_BAD_REQUEST
        
    return Response(response, status=http_status)

# Customer-end API; To get the status of the invoice, returns 400 if invoice is not available in DB
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
        status_code = status.HTTP_400_BAD_REQUEST
        response['details'] = "Given invoice not found in database."
    return Response(response, status=status_code)


# Internal API - For data update purpose, to be used by internal user/Microservices
@api_view(['PUT'])
def updateInvoice(request, invoiceNumber):

    response = {}
    status_code= ''

    try:
        invoiceObject = Invoice.objects.get(invoiceNumber=invoiceNumber)
        
        # In case we don't want to go for validation of data
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
