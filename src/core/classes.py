from aiogram.filters.callback_data import CallbackData
from aiogram.filters import Filter
from aiogram.types import Message
from dataclasses import dataclass


class UserCallback(CallbackData, prefix='user'):
    foo: str
    bar: int
    option : str


class AdminCallback(CallbackData, prefix='admin'):
    foo: str
    bar: int


class FlagStorage:
    def __init__(self):
        self.flags = []

    def push(self, message: str) -> None:
        self.flags.append(message)
    
    def get(self, id: int) -> str:
        try:
            return self.flags[id]
        except IndexError:
            return 'None'

    def clear(self) -> None:
        self.flags.clear()
    

@dataclass(frozen=False)
class Order:
    def __init__(self):
        self.id : int
        self.user : int
        self.category : str
        self.url : str
        self.price : float
        self.delivery_type : str
        self.address : str
        self.size : str
        self.label : str
        self.style : str
        self.status : str
        self.color : str
        self.date : str


class Admin:
    def __init__(self) -> None:
        self.id : int


category_dict = {
    'category_sneak' : 'Кроссовки',
    'category_shoes' : 'Ботинки',
    'category_sweater' : 'Толстовки, кофты, легкие куртки',
    'category_shirt' : 'Футболки, шорты',
    'category_pants' : 'Штаны, джинсы',
    'category_outwear' : 'Зимние куртки, пальто',
    'category_underwear' : 'Носки, майки, нижнее белье',
    'category_glasses' : 'Очки, парфюм, украшения, часы',
    'category_head' : 'Головные уборы',
    'category_small_bag' : 'Маленькие сумки',
    'category_big_bag' : 'Большие сумки',
    'category_another' : 'Другое'
}