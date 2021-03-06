from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY
# Create your views here.
@login_required
def checkout(request):
    customer_id = request.user.userstripe.stripe_id 
    publishkey = settings.STRIPE_PUBLISHABLE_KEY
    if request.method == 'POST':
        # Get the credit card details submitted by the form        
        token=request.POST['stripeToken']   
        
        # Create the charge on Stripe's servers 
        #this will charge the user's card
        try:
            customer = stripe.Customer.retrieve(customer_id)
            customer.sources.create(card=token)
            charge = stripe.Charge.create(
                    amount=1000, # amount in cents, again
                    currency="usd",
                    customer=customer,
                    description="Example charge"
                    )
        except stripe.error.CardError, e:
            # The card has been declined
                pass
    context = {'publishkey':publishkey} 
    template = 'checkout.html'
    return render(request, template, context)

