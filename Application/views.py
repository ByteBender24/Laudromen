from .models import DryCleaningMachine, NormalMachine
from .models import CustomerManager, Customer
from django.shortcuts import render
from django.http import Http404
from django.shortcuts import render, redirect
from .models import Customer
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

        # Load existing customer data from JSON file
        try:
            with open('Application\static\customers.json', 'r') as file:
                customers = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            # Handle the case when the file is not found or contains invalid JSON
            customers = []

        # Add new customer data
        new_customer = {'id': id, 'name': name,
                        'phone_number': phone, 'email': email, 'status':"IN"}
        customers.append(new_customer)

        # Save updated customer data back to JSON file
        with open('Application\static\customers.json', 'w') as file:
            json.dump(customers, file, indent=2)

        # Optionally, you can return a JsonResponse with a success message
        return JsonResponse({'message': 'Customer created successfully', 'customer_id': id})



def machine_list(request):
    return render(request, 'machine_list.html')


def reports(request):
    pass


def booking(request):
    pass


def customer_list(request):
    return render(request, 'view_customer.html')

def update_customer_details(request, customer_id):
    customer_manager = CustomerManager()

    selected_customer = customer_manager.get_customer(customer_id)
    print (selected_customer)
    if selected_customer:
        if request.method == 'POST':
            # Update customer details based on the form submission
            update_data = {
                'name': request.POST.get('name'),
                'phone_number': request.POST.get('phone_number'),
                'email': request.POST.get('email'),
                'status': request.POST.get('status'),
            }

            if customer_manager.update_customer(customer_id, update_data):
                # Redirect or perform additional actions after successful update
                # For example, you might want to redirect to the customer details page
                return JsonResponse({'message': 'Customer details updated successfully'})
            else:
                return JsonResponse({'error': 'Failed to update customer details'}, status=500)
        else:
            # Render the update_customer_details.html template with preloaded data
            return render(request, 'update_customer_details.html', {'customer': selected_customer})
    else:
        # Handle the case where the customer with the given ID is not found
        return JsonResponse({'error': 'Customer not found'}, status=404)


def read_machines_from_json():
    try:
        with open('Application\static\machine.json', 'r') as file:
            machines_data = json.load(file)
    except FileNotFoundError:
        machines_data = []

    machines = []

    for machine_data in machines_data:
        if machine_data['type'] == 'dry_cleaning':
            machine = DryCleaningMachine(
                name=machine_data['name'], capacity=machine_data['capacity'], is_free=machine_data['is_free'])
        elif machine_data['type'] == 'normal':
            machine = NormalMachine(
                name=machine_data['name'], capacity=machine_data['capacity'], is_free=machine_data['is_free'])
        else:
            continue

        machines.append(machine)

    return machines


def write_machine_to_json(machine):
    try:
        with open('Application\static\machine.json', 'r') as file:
            machines_data = json.load(file)
    except FileNotFoundError:
        machines_data = []

    machine_data = {
        'name': machine.name,
        'capacity': machine.capacity,
        'is_free': machine.is_free,
        'type': machine.get_type(),
    }

    machines_data.append(machine_data)

    with open('Application\static\machine.json', 'w') as file:
        json.dump(machines_data, file, indent=2)


def machine_list(request):
    machines = read_machines_from_json()

    return render(request, 'machine_list.html', {'machines': machines})


def create_machine(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        capacity = int(request.POST.get('capacity'))
        is_free = bool(request.POST.get('is_free'))

        machine_type = request.POST.get('type')
        if machine_type == 'dry_cleaning':
            machine = DryCleaningMachine(
                name=name, capacity=capacity, is_free=is_free)
        elif machine_type == 'normal':
            machine = NormalMachine(
                name=name, capacity=capacity, is_free=is_free)
        else:
            return redirect('machine_list')

        # Add the new machine to the machines list and save to JSON file
        machines = read_machines_from_json()
        machines.append(machine)
        write_machine_to_json(machine)

    return render(request, 'add_machine.html')
