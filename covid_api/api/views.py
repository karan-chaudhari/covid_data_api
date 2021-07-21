from django.shortcuts import render, redirect
from rest_framework import generics, permissions
from rest_framework.response import Response
from django.contrib import messages
from django.contrib.auth import authenticate,login
from .serializers import UserSerializer, SignupSerializer
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import UserProfile
import plotly.graph_objects as go
import requests, json
import smtplib, imghdr
from email.message import EmailMessage

# Signup API
class SignupAPI(generics.GenericAPIView):
    serializer_class = SignupSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # return Response({
        # "user": UserSerializer(user, context=self.get_serializer_context()).data
        # })
        messages.info(request, f'account created successfully.')
        return redirect('/')

def index(request):
    if 'email' in request.session:
        return redirect('/fetch/')
    return render(request, 'user/index.html')

def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = UserProfile.objects.filter(email=email, password=password)
        if user:
            request.session['email'] = user[0].email
            user = user[0].email
            return redirect('/fetch/')
        if not user:
            messages.info(request, f'account does not exist plz Sign Up.')
            return render(request, "login.html")
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('/')

def fetch_data(request):
    if request.method == "POST":
        country = request.POST.get("country_dropdown")
        # daterange = request.POST.get("date_dropdown")  
        try:
            url = "https://corona-api.com/countries/"+str(country)
            data = requests.get(url)
            data = data.json()
            fetchedData = []
            dayCount = 0
            for x in data.get('data')['timeline']:
                fetchedData.append(x)
                dayCount += 1
                if dayCount == 15:
                    break

            userData = UserProfile.objects.all()
            countryData = [i.country for i in userData]
            countryData = set(countryData)

            fig = go.Figure(data=[
                go.Bar(name='Confirmed', x=[i['date'] for i in fetchedData], y=[i['confirmed'] for i in fetchedData]),
                go.Bar(name='Recovered', x=[i['date'] for i in fetchedData], y=[i['recovered'] for i in fetchedData]),
            ])

            fig.update_layout(barmode='group', width=1200,height=1200)
            fig.write_image("api/static/graph/fig1.png")

            fig = go.Figure(data=[
                go.Bar(name='Deaths', x=[i['date'] for i in fetchedData], y=[i['deaths'] for i in fetchedData]),
                go.Bar(name='New Confirmed', x=[i['date'] for i in fetchedData], y=[i['new_confirmed'] for i in fetchedData]),
                go.Bar(name='New Recovered', x=[i['date'] for i in fetchedData], y=[i['new_recovered'] for i in fetchedData]),
                go.Bar(name='New Deaths', x=[i['date'] for i in fetchedData], y=[i['new_deaths'] for i in fetchedData]),
                go.Bar(name='Active', x=[i['date'] for i in fetchedData], y=[i['active'] for i in fetchedData])
            ])

            fig.update_layout(barmode='group', width=1200,height=1200)
            fig.write_image("api/static/graph/fig2.png")

            context = {'countryData' : countryData, 'jsonData':fetchedData, 'graph' : True, 'dataTable' : True}
            return render(request, 'fetch-data.html', context)
        except TypeError:
            messages.info(request, f'Select country & daterange option.')
            return redirect('/fetch/')
    userData = UserProfile.objects.all()
    countryData = [i.country for i in userData]
    countryData = set(countryData)
    context = {'countryData' : countryData, 'graph' : False, 'dataTable' : False}
    return render(request, 'fetch-data.html', context)

def send_mail(request):
    if request.method == "POST":
        receiver_mail = request.POST.get("receiver_mail")
        Sender_Email = "testnayara2@gmail.com"
        Reciever_Email = str(receiver_mail)
        Password = "hakpzckvjzrbivrh"

        newMessage = EmailMessage()                         
        newMessage['Subject'] = "COVID DATA API CHART" 
        newMessage['From'] = Sender_Email                   
        newMessage['To'] = Reciever_Email                   
        newMessage.set_content('Covid data chart Image attached!') 

        with open('api/static/graph/fig1.png', 'rb') as f:
            image_data = f.read()
            image_type = imghdr.what(f.name)
            image_name = f.name

        newMessage.add_attachment(image_data, maintype='image', subtype=image_type, filename=image_name)

        with open('api/static/graph/fig2.png', 'rb') as f:
            image_data = f.read()
            image_type = imghdr.what(f.name)
            image_name = f.name

        newMessage.add_attachment(image_data, maintype='image', subtype=image_type, filename=image_name)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            
            smtp.login(Sender_Email, Password)              
            smtp.send_message(newMessage)
        messages.info(request, f'Mail Sent.')
        return redirect('/fetch/')