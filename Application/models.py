import json
from typing import Any
import pickle
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


class Laundry(ABC):
    def __init__(self, cust_id, name, phone, date = None):
        self.cust_id = cust_id
        self.name = name
        self.phone = phone
        self.date = date
        if self.date is None:
            self.date = datetime.now.date


class ClothingLaundry(Laundry):
    def __init__(self, cust_id, name, phone, clothes, date):
        super().__init__(cust_id, name, phone, date)
        self.clothes = clothes


class DryCleaning(Laundry):
    def __init__(self, cust_id, name, phone, clothes, date):
        super().__init__(cust_id, name, phone, date)
        self.clothes = clothes


class BagLaundry(Laundry):
    def __init__(self, cust_id, name, phone, bags, date):
        super().__init__(cust_id, name, phone, date)
        self.bags = bags


class ShoeLaundry(Laundry):
    def __init__(self, cust_id, name, phone, shoes, date):
        super().__init__(cust_id, name, phone, date)
        self.shoes = shoes


class LaundryStrategy(ABC):
    def process(self, cust_id, name, phone, item, date, file_name):
        laundry = self.create_instance(cust_id, name, phone, item, date)
        self.save_to_file(laundry, file_name)

    @abstractmethod
    def create_instance(self, cust_id, name, phone, item, date):
        pass
    
    @abstractmethod
    def save_to_file(self, laundry, file_name):
        pass


class ClothingStrategy(LaundryStrategy):
    def create_instance(self, cust_id, name, phone, item, date):
        return ClothingLaundry(cust_id, name, phone, item, date)

    def save_to_file(self, laundry, file_name):
        with open(file_name, 'wb') as file:
            pickle.dump([laundry], file)


class DryCleaningStrategy(LaundryStrategy):
    def create_instance(self, cust_id, name, phone, item, date):
        return DryCleaning(cust_id, name, phone, item, date)

    def save_to_file(self, laundry, file_name):
        with open(file_name, 'wb') as file:
            pickle.dump([laundry], file)


class BagStrategy(LaundryStrategy):
    def create_instance(self, cust_id, name, phone, item, date):
        return BagLaundry(cust_id, name, phone, item, date)

    def save_to_file(self, laundry, file_name):
        with open(file_name, 'wb') as file:
            pickle.dump([laundry], file)


class ShoeStrategy(LaundryStrategy):
    def create_instance(self, cust_id, name, phone, item, date):
        return ShoeLaundry(cust_id, name, phone, item, date)

    def save_to_file(self, laundry, file_name):
        with open(file_name, 'wb') as file:
            pickle.dump([laundry], file)


def load_data(file_path, target_list):
    if os.path.getsize(file_path) > 0:
        with open(file_path, 'rb') as file:
            target_list.extend(pickle.load(file))


strategies = {
    'clothing': ClothingStrategy(),
    'dry': DryCleaningStrategy(),
    'bag': BagStrategy(),
    'shoe': ShoeStrategy(),
}


def load_data_read(file_path):
    try:
        with open(file_path, 'rb') as file:
            data = pickle.load(file)
    except FileNotFoundError:
        data = []
    return data
