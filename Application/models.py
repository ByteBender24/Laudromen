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

