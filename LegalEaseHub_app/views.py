import json

import requests
from django.http import HttpResponse
from django.shortcuts import render, redirect
from requests.auth import HTTPBasicAuth

from LegalEaseHub_app.credentials import MpesaAccessToken, MpesaC2bCredential, LipanaMpesaPpassword
from LegalEaseHub_app.forms import CasesForm, ImageUploadForm
from LegalEaseHub_app.models import Lawyer, Case, ImageModel


# Create your views here.
def register(request):
    if request.method == 'POST':
        lawyer = Lawyer(firstname=request.POST['firstname'], lastname=request.POST['lastname'],
                        email=request.POST['email'], username=request.POST['username'],
                        password=request.POST['password'])
        lawyer.save()
        return redirect('/')
    else:
        return render(request, 'register.html')


def login(request):
    return render(request, 'login.html')


def index(request):
    if request.method == 'POST':
        if Lawyer.objects.filter(username=request.POST['username'], password=request.POST['password']).exists():
            lawyer = Lawyer.objects.get(username=request.POST['username'], password=request.POST['password'])
            return render(request, 'index.html', {'lawyer': lawyer})
        else:
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')


def about(request):
    return render(request, 'about.html')


def services(request):
    return render(request, 'services.html')


def lawyers(request):
    return render(request, 'lawyers.html')

def contact(request):
    return render(request, 'contact.html')


def add(request):
    if request.method == "POST":
        form = CasesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/form")
    else:
        form = CasesForm()
        return render(request, 'addCases.html', {'form': form})


def show(request):
    case = Case.objects.all()
    return render(request, 'showCases.html', {'case': case})


def delete(request, id):
    case = Case.objects.get(id=id)
    case.delete()
    return redirect('/show')


def edit(request, id):
    case = Case.objects.get(id=id)
    return render(request, 'edit.html', {'case': case})


def update(request, id):
    case = Case.objects.get(id=id)
    form = CasesForm(request.POST, instance=case)
    if form.is_valid():
        form.save()
        return redirect('/show')
    else:
        return render(request, 'edit.html', {'case': case})


def pay(request):
    return render(request, 'pay.html')


def token(request):
    consumer_key = 'YQmocEFkcxUIXvERmzQB1zOjOGGqCQFG'
    consumer_secret = 'DlZPxNqY8mNyYXuH'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(
        consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]

    return render(request, 'token.html', {"token": validated_mpesa_access_token})


def stk(request):
    if request.method == "POST":
        phone = request.POST['phone']
        amount = request.POST['amount']
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        request = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": "JJ's Softwares",
            "TransactionDesc": "Web Development Charges"
        }
        response = requests.post(api_url, json=request, headers=headers)
        return HttpResponse("Success")


def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/image')
    else:
        form = ImageUploadForm()
    return render(request, 'upload_image.html', {'form': form})


def show_image(request):
    images = ImageModel.objects.all()
    return render(request, 'show_image.html', {'images': images})


def imagedelete(request, id):
    image = ImageModel.objects.get(id=id)
    image.delete()
    return redirect('/image')
