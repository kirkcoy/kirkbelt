from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *

import bcrypt

def index(request):
    return render(request, 'quotes/index.html')

def register(request):
    if request.method == 'POST':
        errors = User.objects.register_validator(request.POST)
        print(errors)
        if len(errors):
            for key, val in errors.items():
                messages.error(request, val, extra_tags='register')
                
            # systematicall insert to session correct values 
            for key, val in request.POST.items():
                if key not in errors:
                    request.session[key] = request.POST[key]
        else:
            try: 
                user = User()
                user.first_name = request.POST['first_name']
                user.last_name = request.POST['last_name']
                user.email = request.POST['email']
                user.password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode('utf-8')
                user.save()
                request.session['user_id'] = user.id
                request.session['user_first_name'] = user.first_name
                request.session['logged_in'] = True
                request.session['user_level'] = user.role.level
                request.session['user_hash'] = create_user_hash(user.created_at)
                del request.session['first_name']
                del request.session['last_name']
                del request.session['email']
                messages.success(request, 'Successfully registered!')
            except Exception as e:
                print(str(e))
            return redirect('/quotes')
        return redirect('/')
            #  return redirect('/wishes')

def signin(request):
    if request.method == 'POST':
        try:
            user = User.objects.get(email = request.POST['email'])
        except Exception as e:
            print(str(e))
            messages.error(request, 'Unable to login', extra_tags="login")
            return redirect('/signin')
        
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            request.session['user_id'] = user.id
            request.session['user_first_name'] = user.first_name
            request.session['logged_in'] = True
            return redirect('/quotes')
        else:
            messages.error(request, 'Unable to login')
            return redirect('/')
        
    elif request.method == 'GET':
        if 'logged_in' in request.session and request.session['logged_in']:
            return redirect('/')
        else:
            return render(request, 'quotes/index.html')

def quotes(request):
    if 'user_id' in request.session:
        quotes = Quote.objects.all().order_by('-created_at')
        return render(request, 'quotes/dash.html', { 'quotes': quotes } )
    else:
        messages.error(request, 'You must logged in to enter this websit', extra_tags="login")
        return redirect('/')


def add_new_quotes(request):
    # for retention
    request.session['author']=request.POST['author']
    request.session['quote']=request.POST['quote']

    print(request.session['user_id'], '-'*100)

    if request.method == 'POST':
        errors = Quote.objects.quotes_validator(request.POST)
        if len(errors):
            for key, val in errors.items():
                messages.error(request, val, extra_tags='quotes')
                
            for key, val in request.POST.items():
                if key not in errors:
                    request.session[key] = request.POST[key]
        else:
            try: 
                quote = Quote()
                quote.message = request.POST['quote']
                quote.author = request.POST['author']
                quote.user = User.objects.get(id = request.session['user_id'])
                quote.save()
            except Exception as e:
                print(str(e))
        return redirect('/quotes')

def add_likes(request, id):

    quote = Quote.objects.get(id = id)
    try:
        likers = quote.likers.get(id = request.session['user_id'])
        messages.error(request, 'Already liked this quote', extra_tags='likes')
    except:
        pass

    try:
        user = User.objects.get(id = request.session['user_id'])
        quote.likers.add(user)
    except:
        pass

    return redirect('/quotes') 


def remove_quote(request, id):
    try:
        quote = Quote.objects.get(id = id)
        quote.delete()
        return redirect('/quotes')
    except:
        messages.error(request, 'Error on delete', extra_tags='likes')
        return redirect('/quotes')

def myaccount_id(request, id):
    if 'user_id' in request.session:
        user = User.objects.get(id = request.session['user_id'])
        return render(request, 'quotes/edit.html', { 'user': user} )

    else:
        messages.error(request, 'You must logged in to enter this websit', extra_tags="login")
        return redirect('/')

def edit(request):
    # for retention
    request.session['efirst_name']=request.POST['first_name']
    request.session['elast_name']=request.POST['last_name']
    request.session['eemail']=request.POST['email']

    if request.method == 'POST':
        errors = User.objects.edit_validator(request.POST)
        print(errors)
        if len(errors):
            for key, val in errors.items():
                messages.error(request, val, extra_tags='register')
                
            # systematicall insert to session correct values 
            for key, val in request.POST.items():
                if key not in errors:
                    request.session[key] = request.POST[key]
        else:
            try: 
                user = User.objects.get(id = request.session['user_id'])
                user.first_name = request.POST['first_name']
                user.last_name = request.POST['last_name']
                user.email = request.POST['email']
                user.save()
                messages.success(request, 'Successfully edited!')
            except Exception as e:
                print(str(e))
        return redirect('/myaccount/' + str(request.session['user_id']))

def user_id(request, id):
    if 'user_id' in request.session:
        user = User.objects.get(id = request.session['user_id'])
        quotes = user.quotes.all().order_by('-created_at')
        return render(request, 'quotes/user.html', { 'quotes': quotes, 'user': user} )

    else:
        messages.error(request, 'You must logged in to enter this websit', extra_tags="login")
        return redirect('/')

def logout(request):
    keys = []
    
    for key in request.session.keys():
        keys.append(key)

    for idx in range(len(keys)):
        del request.session[keys[idx]]

    messages.success(request, 'You\'ve been logged out successfully!')
    return redirect('/signin')