from django.shortcuts import render
from template.models import Product
from paypal.standard.forms import PayPalPaymentsForm
from django.views import View
from django.views.generic import TemplateView
import stripe
from  django.conf  import settings
import json
from django.shortcuts import get_object_or_404

from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse

stripe.api_key= settings.STRIPE_SECRET_KEY


def index(request):
    return render(request, 'checkout.html')



class SuccessView(TemplateView):
    template_name = "success.html"

class CancelView(TemplateView):
    template_name = "cancel.html"


class ProductLandingPageView(TemplateView):
    template_name = "landing.html"

    def get_context_data(self, **kwargs):
        product = Product.objects.get(name="Pant")
        context = super(ProductLandingPageView, self).get_context_data(**kwargs)
        context.update({
            "product": product,
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
        })
        return context


class CreateCheckoutSessionView(View):
    def post(self, request,product_id, *args, **kwargs):
        product_id = self.kwargs["pk"]
        user_email = request.user.email 
        product = Product.objects.get(id=product_id)
        YOUR_DOMAIN = "http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': int(product.price * 100),
                        'product_data': {
                            'name': product.name,
                            # 'images': ['https://i.imgur.com/EHyR2nP.png'],
                        },
                    },
                    'quantity': 1,
                },
            ],
           
          
            mode='payment',
            customer_email=user_email,  # Store user's email
              metadata={  
                'user_email': user_email,
                'product_id': str(product.id),
                
    },
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )
        return JsonResponse({
            'id': checkout_session.id
        })


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None

    try:
        # Construct the event from Stripe webhook payload
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle different event types
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        user_email = session.get("metadata", {}).get("user_email")  # Get logged-in user's email
        product_id = session.get("metadata", {}).get("product_id")

        if not product_id or not user_email:
            return HttpResponse("Missing product ID or email", status=400)

        product = get_object_or_404(Product, id=product_id)
        # Send an email to the customer with the product URL or file link
        email = send_mail(
            subject="Here is your product",
            body=f"Thanks for your purchase. Here is the product you ordered. The URL is {product.url}",
            from_email= user_email,  # Send email from logged-in user
            to=[user_email],  # Send to user
            headers={"Reply-To": user_email},  # Allow replies to the user
        )
        email.send()

    elif event["type"] == "payment_intent.succeeded":
        intent = event['data']['object']
        stripe_customer_id = intent["customer"]
        stripe_customer = stripe.Customer.retrieve(stripe_customer_id)
        customer_email = stripe_customer['email']
        product_id = intent["metadata"]["product_id"]
        product = Product.objects.get(id=product_id)

        # Send email with product URL or file link to the customer
        send_mail(
            subject="Here is your product",
            message=f"Thanks for your purchase. Here is the product you ordered. The URL is {product.url}",
            recipient_list=[customer_email],
            from_email=settings.EMAIL_HOST_USER
        )

    return HttpResponse(status=200)



class StripeIntentView(View):
    def post(self, request, *args, **kwargs):
        try:
           
            req_json = json.loads(request.body)
            
            customer = stripe.Customer.create(email=req_json['email'])

            
            product_id = self.kwargs["pk"]
            product = Product.objects.get(id=product_id)

            # Convert price from dollars to cents (Stripe requires amount in cents)
            amount_in_cents = int(product.price * 100)

          
            intent = stripe.PaymentIntent.create(
                amount=amount_in_cents,
                currency='usd',
                customer=customer['id'],
                metadata={
                    "product_id": product.id
                }
            )
            # Return the client secret which the frontend needs to complete payment
            return JsonResponse({
                'clientSecret': intent['client_secret'] 
            })
        
        except stripe.error.StripeError as e:
            # Handle Stripe errors (e.g., invalid API keys, rate limits)
            return JsonResponse({'error': 'Stripe error: ' + str(e)}, status=400)
        
        except Product.DoesNotExist:
            # Handle case where product with given ID does not exist
            return JsonResponse({'error': 'Product not found'}, status=404)
        
        except Exception as e:
            # General error handling for unexpected issues
            return JsonResponse({'error': 'An unexpected error occurred: ' + str(e)}, status=500)
