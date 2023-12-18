import json
from typing import Any
import os
from abc import ABC, abstractmethod 
from datetime import datetime

class Customer:
    def __init__(self, name, phone, email, status, id):
        self.name = name
        self.phone = phone
        self.email = email
        self.status = status
        self.id = id

class CustomerManager:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(CustomerManager, cls).__new__(cls)
            cls._instance.customers = []
            cls._instance.load_data()
        return cls._instance

    def load_data(self):
        # Load customer data from JSON file
        with open('Application\static\customers.json') as json_file:
            self.customers = json.load(json_file)

    def save_data(self):
        # Save customer data to JSON file
        with open('Application\static\customers.json', 'w') as json_file:
            json.dump(self.customers, json_file, indent=2)

    def get_customer(self, customer_id):
        # Get customer by ID
        return next((customer for customer in self.customers if customer['id'] == customer_id), None)

    def update_customer(self, customer_id, data):
        # Update customer details
        customer = self.get_customer(customer_id)
        if customer:
            customer.update(data)
            self.save_data()
            return True
        return False


class Machine(ABC):
    def __init__(self, name, capacity, is_free):
        self.name = name
        self.capacity = capacity
        self.is_free = is_free

    @abstractmethod
    def get_type(self):
        pass


class DryCleaningMachine(Machine):
    def get_type(self):
        return 'dry_cleaning'


class NormalMachine(Machine):
    def get_type(self):
        return 'normal'


class TotalCostStrategy:
    def calculate_total_cost(self, booking, price_data):
        raise NotImplementedError("Subclasses must implement this method")


class BasicTotalCostStrategy(TotalCostStrategy):
    def calculate_total_cost(self, booking, price_data):
        total_cost = 0
        total_cost += price_data.get('dry_cleaning', 0) * booking.dry_quantity
        total_cost += price_data.get('clothes', 0) * booking.clothes_quantity
        total_cost += price_data.get('shoes', 0) * booking.shoes_quantity
        total_cost += price_data.get('bags', 0) * booking.bags_quantity
        return total_cost


class SpecialOfferTotalCostStrategy(TotalCostStrategy):
    def calculate_total_cost(self, booking, price_data):
        # Implement special offer pricing logic here
        pass

class Booking:
    def __init__(self, booking_id, customer_id, dry_quantity=0, clothes_quantity=0, shoes_quantity=0, bags_quantity=0, total_cost=0,payment_status=False):
        self.booking_id = booking_id
        self.customer_id = customer_id
        self.dry_quantity = dry_quantity
        self.clothes_quantity = clothes_quantity
        self.shoes_quantity = shoes_quantity
        self.bags_quantity = bags_quantity
        self.total_cost = total_cost
        self.payment_status = payment_status


class BookingManager:
    _instance = None
    bookings = []

    def __init__(self, total_cost_strategy=None):
        self.total_cost_strategy = total_cost_strategy or BasicTotalCostStrategy()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BookingManager, cls).__new__(cls)
        return cls._instance

    def add_booking(self, booking):
        self.bookings.append(booking)

    def get_bookings(self):
        return self.bookings

    def get_booking_by_id(self, booking_id):
        for booking in self.bookings:
            if booking.booking_id == booking_id:
                return booking
        return None

    def update_booking(self, booking_id, new_booking):
        for i, booking in enumerate(self.bookings):
            if booking.booking_id == booking_id:
                self.bookings[i] = new_booking
                break

    # Implementing the iterator pattern
    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        if self._index < len(self.bookings):
            result = self.bookings[self._index]
            self._index += 1
            return result
        else:
            raise StopIteration

    def set_total_cost_strategy(self, total_cost_strategy):
        self.total_cost_strategy = total_cost_strategy

    def calculate_total_cost(self, booking, price_data):
        return self.total_cost_strategy.calculate_total_cost(booking, price_data)
