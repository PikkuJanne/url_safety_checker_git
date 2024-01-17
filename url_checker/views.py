from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import URL
from .safe_browsing import check_url_with_google_safe_browsing
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.response import Response
from .serializers import URLSerializer
from .safe_browsing import check_url_with_google_safe_browsing


@api_view(['POST'])
def api_register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.create_user(username=username, password=password)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def api_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def submit_url(request):
    serializer = URLSerializer(data=request.data)
    if serializer.is_valid():
        url_instance = serializer.save(user=request.user)
        is_malicious = check_url_with_google_safe_browsing(url_instance.url)
        url_instance.is_malicious = is_malicious if is_malicious is not None else False
        url_instance.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('submit_url')  
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def submit_url(request):
    context = {}  # rendering templates

    if request.method == 'POST':
        submitted_url = request.POST.get('url')  
        print("Form submitted with URL:", submitted_url)  

        if submitted_url:  
            url_instance = URL(url=submitted_url, user=request.user)
            url_instance.save()  
            print("URL instance saved:", url_instance.url)  

            # Check if the URL is maliciousness ugly
            is_malicious = check_url_with_google_safe_browsing(submitted_url)
            if is_malicious is not None:  
                url_instance.is_malicious = is_malicious
                url_instance.checked_date = timezone.now()
                url_instance.save()
                return redirect('display_result', url_instance.id)
            else:
                context['error'] = "Error checking URL. Please try again."

    # Render the URL sub formia
    return render(request, 'url_checker/submit_url.html', context)


@login_required
def display_result(request, url_id):
    try:
        # Retrieve the URL instance by ID
        url_instance = URL.objects.get(id=url_id)
        print("Displaying result for URL ID:", url_id) 
        return render(request, 'url_checker/display_result.html', {'url': url_instance})
    except URL.DoesNotExist:
        # If the URL instance doesn't exist, return an error fukaa
        print("URL not found for ID:", url_id)  
        return render(request, 'url_checker/display_result.html', {'error': "URL not found."})
    
@login_required
def history(request):
    # Fetching URLs checked by the logged-in user
    user_urls = URL.objects.filter(user=request.user).order_by('-checked_date')
    
    # Passing the URLs to the template
    return render(request, 'url_checker/history.html', {'user_urls': user_urls})




