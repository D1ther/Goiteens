from models import Subscription
from django.shortcuts import get_object_or_404

def get_subscriptions():
    return Subscription.objects.all()

def get_subscription_by_id(subscription_id: int):
    return get_object_or_404(Subscription, id=subscription_id)

    
