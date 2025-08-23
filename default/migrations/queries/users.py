from models import (
    User,
    Subscription,
    UserSubscribers
)

from django.shortcuts import get_object_or_404


def subscribe_user_to_subscription(user_email: str, subscription: Subscription):
    try:
        user = get_object_or_404(User, email=user_email)

        if subscription in user.subscribes.all():
            return "User already subscribed to this subscription."
        
        user_subcriptions = get_object_or_404(UserSubscribers, user=user, subscribe=subscription)

        if user_subcriptions:
            user_subcriptions.active = True
            user_subcriptions.save()
        
        user.subscribes.add(subscription)
        user.save()

        return user
    except Exception as e:
        print(f"Error subscribing user: {e}")
        return None

def unsubscribe_user_from_subscription(user_email: str, subscription: Subscription):
    try:
        user = get_object_or_404(User, email=user_email)

        if subscription not in user.subscribes.all():
            return "User is not subscribed to this subscription."
        
        user_subcriptions = get_object_or_404(UserSubscribers, user=user, subscribe=subscription)

        if user_subcriptions:
            user_subcriptions.delete()
            user_subcriptions.save()
        
        user.subscribes.remove(subscription)
        user.save()

        return user
    except Exception as e:
        print(f"Error unsubscribing user: {e}")
        return None
        
     
