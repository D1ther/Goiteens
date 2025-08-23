from models import (
    User,
    Subscription,
    Content,
    UserSubscribers
)
from django.shortcuts import get_object_or_404

def get_content_from_subscription(user_email: str, content_id: int, subscription_id: int):
    try:
        user = get_object_or_404(User, email=user_email)

        if not user.subscribes.filter(id=subscription_id).exists():
            return "User is not subscribed to this subscription."
        
        subscription = get_object_or_404(Subscription, id=subscription_id)
        content = get_object_or_404(Content, id=content_id)

        user_subscriptions = get_object_or_404(UserSubscribers, user=user, subscribe=subscription)

        if not user_subscriptions.active:
            return "User subscription is not active."

        if content not in subscription.content:
            return "Content is not available in this subscription."
        
        return content
    except Exception as e:
        print(f"Error retrieving content: {e}")
        return None
        
