from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from contacts.models import Contact


def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

        #check if user has already done an enquiry
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(listing_id=listing_id, user_id=user_id)
            if has_contacted:
                messages.error(request, 'You Have Already Made An Inquiry For This Listing ')
                return redirect('/listings/' + listing_id)

        contact = Contact(listing=listing, listing_id=listing_id, name=name, email=email, phone=phone, message=message, user_id=user_id)

        contact.save()

        #send mail
        send_mail(
            'Shops Listing Inquiry',
            'there has been an inquiry for '+listing+' contact no: '+phone+' name: '+name+' . sign into the admin pannel for more info',
            'bt.realestate.co@gmail.com',
            [realtor_email, 'ahthakkar02@gmail.com'],
            fail_silently=False

        )
        messages.success(request, 'Your Request Has Been Submitted, A Realtor Will Get Back To You Soon')

        return redirect('/listings/'+listing_id)