from django.db import models
import pickle
import os
from abc import ABC, abstractmethod 
# Create your models here.

class Admin:
    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password


class Create_Account:
    def __init__(self, name, password):
        self.name = name
        self.password = password


def create_Account(name, password):
    return Create_Account(name, password)


class Laundry(ABC):
    def __init__(self, cust_id, name, phone, date):
        self.cust_id = cust_id
        self.name = name
        self.phone = phone
        self.date = date


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