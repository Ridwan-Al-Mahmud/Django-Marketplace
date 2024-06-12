from django.shortcuts import render, redirect
from .models import Product, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib import messages
from .forms import SignUpForm

# Create your views here.
def index(request):
  products = Product.objects.all()
  return render(request, 'store/index.html', {
    'products': products
  })

def about(request):
  return render(request, 'store/about.html')

def login_user(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
      login(request, user)
      messages.success(request, 'You have been logged in successfully!...')
      return redirect('index')
    else:
      messages.success(request, 'There was an error logging in! Please, try again...')
      return render(request, 'login')
  else:
    return render(request, 'store/login.html')

def logout_user(request):
  logout(request)
  messages.success(request, 'You have been logged out successfully!...')
  return redirect('index')

def register_user(request):
  form = SignUpForm()
  if request.method == 'POST':
    form = SignUpForm(request.POST)
    if form.is_valid():
      form.save()
      username = form.cleaned_data['username']
      password = form.cleaned_data['password1']
      user = authenticate(username=username, password=password)
      login(request, user)
      messages.success(request, 'You have been registered successfully!...')
      return redirect('index')
    else:
      messages.success(request, 'Oops, an error occurred! Please try again...')
      return redirect('register')
  else:
      return render(request, 'store/register.html',{
        'form': form
      })

def product(request, pk):
  product = Product.objects.get(id=pk)
  return render(request, 'store/product.html', {
    'product': product
  })

def category(request, foo):
  foo = foo.replace('-', ' ')
  try:
    category = Category.objects.get(name=foo)
    products = Product.objects.filter(category=category)
    return render(request, 'store/category.html', {
      'products': products,
      'category': category
    })
  except:
    messages.success(request, "That category doesn't exist...")
    return redirect('index')