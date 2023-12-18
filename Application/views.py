from .models import CustomerManager, Customer, DryCleaningMachine, NormalMachine, Booking, BookingManager
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect
import re
import random
import json


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
                        'phone_number': phone, 'email': email, 'status': "OUT"}
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



def customer_list(request):
    return render(request, 'view_customer.html')


def update_customer_details(request, customer_id):
    customer_manager = CustomerManager()

    selected_customer = customer_manager.get_customer(customer_id)
    print(selected_customer)
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


# views.py


def generate_booking_id(customer_id):
    # Extract the first two digits of the customer_id
    first_two_digits = str(customer_id)[:2]

    # Generate a random 4-digit number
    random_digits = str(random.randint(1000, 9999))

    # Concatenate the first two digits and random digits
    booking_id = f"{first_two_digits}{random_digits}"

    return booking_id


def is_valid_customer_id(customer_id):
    # Regex pattern for validating customer_id (3 letters + 6 digits)
    pattern = re.compile(r'^[a-zA-Z]{3}\d{6}$')
    return re.match(pattern, customer_id)


# views.py


def free_machines():
    with open(r'Application\static\freemachines.json', 'r') as free_machines:
        free_machines_data = json.load(free_machines)

    with open(r'Application\static\machine.json', 'r') as machine_list:
        machine_list_data = json.load(machine_list)

    dry_free = normal_free = 0

    for data in machine_list_data:
        if data['type'] == "dry_cleaning" and data['is_free'] == True:
            dry_free += 1
        if data['type'] == "normal" and data['is_free'] == True:
            normal_free += 1
    
    free_machines_data = {
        "dry_free": dry_free,
        "normal_free": normal_free
    }
    with open(r'Application\static\freemachines.json', 'w') as free_machines:   
        json.dump(free_machines_data, free_machines)

    with open(r'Application\static\freemachines.json', 'r') as free_machines:
        free_machines_data = json.load(free_machines)

    return free_machines_data

def price_list_return():
    with open(r'Application\static\pricelist.json', 'r') as price_file:
        price_data = json.load(price_file)
        print(price_data)
    return price_data



def create_booking(request):
    price_data = price_list_return()
    free_machine = free_machines()
    context = {'price_data': price_data, 'free_machines' : free_machine}
    
    if request.method == 'POST':
        # Extract data from form submission
        customer_id = request.POST.get('customer_id')
        dry_quantity = request.POST.get('dry_quantity')
        clothes_quantity = request.POST.get('clothes_quantity')
        shoes_quantity = request.POST.get('shoes_quantity')
        bags_quantity = request.POST.get('bags_quantity')

        # Validate customer_id
        if not is_valid_customer_id(customer_id):
            return JsonResponse({'success': False, 'message': 'Invalid customer ID'})

        # Convert quantities to integers (if not None)
        dry_quantity = int(dry_quantity) if dry_quantity is not None else 0
        clothes_quantity = int(clothes_quantity) if clothes_quantity is not None else 0
        shoes_quantity = int(shoes_quantity) if shoes_quantity is not None else 0
        bags_quantity = int(bags_quantity) if bags_quantity is not None else 0
        # Generate booking ID
        booking_id = generate_booking_id(customer_id)

        # Create Booking instance
        booking = Booking(booking_id, customer_id, dry_quantity, clothes_quantity, shoes_quantity, bags_quantity, total_cost = 0, payment_status = False)
        # Add booking to BookingManager
        booking_manager = BookingManager()
        total_cost = booking_manager.calculate_total_cost(booking, price_data.get('price_rates'))
        booking.total_cost = total_cost

        print(booking.total_cost)

        booking_manager.add_booking(booking)
        with open(r'Application\static\bookings.json', 'r') as booking_json:
            bookings_json_data = json.load(booking_json)
        
        for booking in booking_manager:
            dict_temp = {}
            dict_temp['booking_id'] = booking.booking_id
            dict_temp['customer_id'] = booking.customer_id
            dict_temp['dry_quantity'] = booking.dry_quantity
            dict_temp['clothes_quantity'] = booking.clothes_quantity
            dict_temp['shoes_quantity'] = booking.shoes_quantity
            dict_temp['bags_quantity'] = booking.bags_quantity
            dict_temp['total_cost'] = booking.total_cost
            dict_temp['payment_status'] = booking.payment_status
            bookings_json_data.append(dict_temp)
        
        BookingManager.bookings= []

        with open(r'Application\static\bookings.json', 'w') as booking_json:
            json.dump(bookings_json_data, booking_json, indent=4)
        
        return JsonResponse({'success': True, 'message': 'Booking created successfully'})
    else:
        return render(request, 'create_booking.html', context)


def view_bookings(request):
    with open(r'Application\static\bookings.json', 'r') as booking_json:
        bookings_json_data = json.load(booking_json)

    return render(request, 'view_bookings.html', {'bookings': bookings_json_data})

def update_booking(request, booking_id):
    with open(r'Application\static\bookings.json', 'r') as booking_json:
        bookings_json_data = json.load(booking_json)
    
    for booking in bookings_json_data:
        if booking['booking_id'] == booking_id:
            booking_final = booking
            booking_idx = bookings_json_data.index(booking)
    booking = booking_final

    if request.method == 'POST':
        # Extract updated data from the form submission
        updated_payment_status = request.POST.get('confirm_payment')
        if updated_payment_status == 'on':
            booking['payment_status'] = True
        bookings_json_data[booking_idx] = booking

        with open(r'Application\static\bookings.json', 'w') as booking_json:
            json.dump(bookings_json_data, booking_json, indent=4)

        return redirect('view_bookings')

    return render(request, 'update_booking.html', {'booking': booking})



def machine_details(request, machine_name):
    # Load machine data from the JSON file
    with open(r'Application\static\machine.json', 'r') as file:
        machines_data = json.load(file)

    # Find the machine with the specified name
    machine = next((m for m in machines_data if m['name'] == machine_name), None)

    if machine is not None:
        return render(request, 'machine_details.html', {'machine': machine})
    else:
        # If machine with the specified name is not found, return a 404 response
        return JsonResponse({'success': False, 'message': 'no machine details found'})
