from user.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from account.models import Account
from order.models import Order




@receiver(post_save, sender=User)
def create_account(sender, instance, created, **kwargs):

    if created:
       account =  Account.objects.create(user=instance)
       # order = Order.objects.create(account=account, status='checkout', mounted=True)
      
    
