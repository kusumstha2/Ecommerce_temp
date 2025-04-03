# Ecommerce templates

### Install Dependencies
- pip install -r requirements.txt

### Apply migrations
- py manage.py makemigrations
- py manage.py migrate

### Create superuser
- py manage.py createsuperuser

### To run server
- py manage.py runserver

### Set up a virtual environment:
- python -m venv env.

## API Endpoints

### Get All Categories
- Endpoint: GET /templates/product_category/
- Response Status: 200 OK
- Headers:
    Allow: GET, POST, HEAD, OPTIONS
    Content-Type: application/json
    Vary: Accept

### Create a product
- Endpoint: POST/templates/products/
- Response Status: 201 Created
- Headers:
    Allow: GET, POST, HEAD, OPTIONS
    Content-Type: application/json
    Location: True
    Vary: Accept

## Inventory Management
- When a new product is added, its initial stock quantity is stored (e.g., 500 pieces).
- When a customer adds a product to the cart (e.g., 50 pieces), the stock remains unchanged until the purchase is completed.
- After a successful purchase, the stock is decreased by the purchased quantity (e.g., 500 - 50 = 450 pieces).
- If the same product is added again, it will be added to the existing stock, ensuring accurate tracking.