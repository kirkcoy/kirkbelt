from django.db import models
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
LETTER_REGEX = re.compile(r'^[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*\d)(?=.*[A-Z]).*$')

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}

        if len(postData['first_name']) < 1: 
            errors["first_name"] = "First Name field is required."
        elif len(postData['first_name']) < 2 or not LETTER_REGEX.match(postData['first_name']):
            errors["first_name"] = "First Name must contain at least two letters and contain only letters."
        
        if len(postData['last_name']) < 1: 
            errors["last_name"] = "Last Name field is required."
        elif len(postData['last_name']) < 2 or not LETTER_REGEX.match(postData['last_name']):
            errors["last_name"] = "Last Name must contain at least two letters and contain only letters."

        if len(postData['email']) < 1: 
            errors["email"] = "Email field is required."
        elif not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Invalid Email Address."

        try:
            user = User.objects.get(email = postData['email'])
            errors["email"] = "Email was already taken."
        except:
            pass

        if len(postData['password']) < 1:
            errors["password"] = "Password field is required."
        elif  len(postData['password']) < 8 or len(postData['password']) > 15 or not PASSWORD_REGEX.match(postData['password']):
            errors["password"] = "Password must contain a number, a capital letter, and be between 8-15 characters."

        if len(postData['confirm_password']) < 1:
            errors["confirm_password"] = "Please confirm your password"
        elif postData['password'] != postData['confirm_password']:
            errors["confirm_password"] = "Password must match."

        return errors

    def edit_validator(self, postData):
        errors = {}

        if len(postData['first_name']) < 1: 
            errors["first_name"] = "First Name field is required."
        elif len(postData['first_name']) < 2 or not LETTER_REGEX.match(postData['first_name']):
            errors["first_name"] = "First Name must contain at least two letters and contain only letters."
        
        if len(postData['last_name']) < 1: 
            errors["last_name"] = "Last Name field is required."
        elif len(postData['last_name']) < 2 or not LETTER_REGEX.match(postData['last_name']):
            errors["last_name"] = "Last Name must contain at least two letters and contain only letters."

        if len(postData['email']) < 1: 
            errors["email"] = "Email field is required."
        elif not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Invalid Email Address."

        return errors

class QuotesManager(models.Manager):
    def quotes_validator(self, postData):
        errors = {}

        if len(postData['author']) < 4:
            errors["author"] = "Author must contain more than 3 characters"
        
        if len(postData['quote']) < 11:
            errors["quote"] = "Quote must contain more than 10 characters"

        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

class Quote(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=255)

    user = models.ForeignKey(User, related_name="quotes", on_delete=models.DO_NOTHING)
    likers = models.ManyToManyField(User, related_name="liked_quotes")

    objects = QuotesManager()
