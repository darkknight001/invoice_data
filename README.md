# Invoice Handler API Assignment - OneImpression

## Context 
Customers send in their invoices (PDF files) and the your system converts the (unstructured) data from the invoice into a structured format and saves it in an SQL database. At the minimum, this includes the vendor/seller, the purchaser/buyer, the invoice number and date, and each line item mentioned in the invoice.

These documents are then processed by our background processing engine using OCR and machine learning (or sometimes manually), structured information is generated and validated, after which the document is marked “digitized” and the structured information is accessible to our customers.

This is a sample web service to handle above given problem statement

## Structure
Here, I've used SQLITE as relational DB

DB structure used:

```
TABLE Invoice
  - _id (Primary key, auto-incremented)
  - invoiceNumber(String, unique) 
  - file(file path)
  - vendor(supplier/vendor details)
  - buyer(Buyer details)
  - billedAmt(Amount on invoice)
  - billedDate(Date on which invoice is generated)
  - items (Particulares)
  - isDigitized(Tells if document is digitized or not, Boolean, default value: False)
  - created_timestamp(datetime, shows what time the invoice was uploaded)
```

## How to use this repository
- Clone the repository from github.
- move to repository folder
- Create a virtualenv and install required packages
  ```bash
  $ python3 -m venv virtualenv
  $ source virtualenv/bin/activate
  $ pip3 install -r requirements.txt
  ```
- start django server:
  ```bash
  $ python manage.py makemigrations #To cheate database schema
  $ python manage.py migrate #Implement migrations
  $ python manage.py runserver #start webserver
  ```
-Optional: Django-admin
```bash
$ python manage.py createsuperuser #Create superuser to access Django Admin
```


## APIs 

1. ### Load Invoice
   ```
   Method: POST
   Path: "/api/load_invoice"
   Desciption: Client-side API, takes pdf file as request data, and returns the status
   ```


   - Request Payload:
   ```python
   {
     "file": "<file object>"   #Used postman to test
   }
   ```


   - Response Data:
   ```JSON
   {
      "status": "File uploaded successfully",
      "details": {
          "invoiceNumber": "<InvoiceNumber>",
          "file": "<InvoiceNumber>.pdf",
          "isDigitized": false,
          "created_timestamp": "datetime.datetime"
      }
   }
   ```


2. ### Get Invoice Status
    ```
    Method: GET
    Path: "/api/get_invoice_status/<invoiceNumber>"
    Desciption: Client-side API, takes invoice_number as request data, and returns the status of digitization
    ```
    - Request Payload:
    ```python
    None
    ```
    - Response Data:
    ```JSON
    {
        "status": "success",
        "details": {
            "Status": "The document is processed.",
            "data": {
                "invoiceNumber": "<invoiceNumber>",
                "file": "/media/<invoiceNumber>.pdf",
                "vendor": "Vendor Details",
                "buyer": "Buyer Details",
                "billedAmt": "Amt",
                "billedDate": "datetime.datetime",
                "items": "<Particaulars>",
                "isDigitized": true,
                "created_timestamp": "datetime.datetime"
            }
        }
    }
    ```


3. ### Update Invoice Data
    ```
    Method: PUT
    Path: "/api/update_invoice/<invoiceNumber>"
    Desciption: Internal API, to be used manualy or by other microservices to update the invoice data to database
    
    ```
    - Request Payload:
    ```python
    {
        "vendor": "Vendor Details",
        "buyer": "Buyer Details",
        "billedAmt": "Amt",
        "billedDate": "datetime.datetime",
        "items": "<Particaulars>",
        "isDigitized": true
    }
    ```
    - Response Data:
    ```JSON
    {
        "details": "Details updated successfully",
        "details": {
            "Status": "The document is processed.",
            "data": {
                "invoiceNumber": "<invoiceNumber>",
                "file": "/media/<invoiceNumber>.pdf",
                "vendor": "Vendor Details",
                "buyer": "Buyer Details",
                "billedAmt": "Amt",
                "billedDate": "datetime.datetime",
                "items": "<Particaulars>",
                "isDigitized": true,
                "created_timestamp": "datetime.datetime"
            }
        }
    }
    ```


    
## Testing the API 
   We can use Postman to test the API. Use endpoint as 'http://localhost:8000/api/...'
   

## Scope of Improvements
- Using Authentication
- Adding User interface for both client-end and internal use

