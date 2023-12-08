from django.shortcuts import render
import re
import random
import json
from django.http import JsonResponse


# Methods
def generate_customer_code(name, phone_number):
    # Extract the first three letters from the customer's name
    name_prefix = re.sub(r'[^a-zA-Z]', '', name)[:3].upper()

    # Generate a random three-digit number
    random_three_digits = str(random.randint(100, 999))

    # Extract the last three digits from the phone number
    last_three_digits = re.sub(r'[^0-9]', '', phone_number)[-3:]

    # Combine the name prefix, random three digits, and last three digits to create the customer code
    customer_code = f"{name_prefix}{random_three_digits}{last_three_digits}"

    return customer_code

# Create your views here.


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def dashboard(request):
    return render(request, 'dashboard.html')


def create_customer(request):
    if request.method == "GET":
        return render(request, 'create_customer.html')
    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone_number')
        email = request.POST.get('email')
        id = generate_customer_code(name, phone)

        print(name, phone, email, id)
        # Load existing customer data from JSON file
        try:
            with open('Application\static\customers.json', 'r') as file:
                customers = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            # Handle the case when the file is not found or contains invalid JSON
            customers = []

        # Add new customer data
        new_customer = {'id': id, 'name': name,
                        'phone_number': phone, 'email': email}
        customers.append(new_customer)

        # Save updated customer data back to JSON file
        with open('Application\static\customers.json', 'w') as file:
            json.dump(customers, file, indent=2)

        # Optionally, you can return a JsonResponse with a success message
        return JsonResponse({'message': 'Customer created successfully', 'customer_id': id})



def machine_list(request):
    pass


def reports(request):
    pass


def booking(request):
    pass


def customer_list(request):
    return render(request, 'view_customer.html')
