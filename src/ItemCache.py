"""
Tool used to find the cheapest possible crafting route through a World of Warcraft profession.
    Copyright (C) 2021  Kevin Tyrrell

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from RecipeManager import RecipeManager
from Recipe import Recipe
from JSONLoader import JSONLoader

from typing import Callable, Iterable


class ItemCache:
    def __init__(self, manager: RecipeManager, loader: JSONLoader, prices_path: str):
        self.__recipes = manager.recipes
        self.__vendor = loader.register("Vendor")
        self.__conversions = loader.register("Conversions")
        self.__prices = loader.register("Prices", prices_path)
        self.__cache = {}

    """
    Evaluates and appraises a specified item.
    Items purchasable from vendors are defaulted to vendor price.
    Items crafted from the profession are defaulted to their crafting cost.
    If the item can be converted from another items, that price is taken into account.
    Otherwise, the user-provided prices JSON file is used.
    
    Items which cannot have their price evaluated will throw a runtime error.
    
    @:param item: Name of the item to be evaluated.
    @:return value: Appraised value of the item.
    """
    def eval_item(self, item: str):
        if item in self.__cache:  # Memoization.
            print("Already Seen Item: '{}'".format(item))
            return self.__cache[item]
        if item in self.__vendor:
            return self.__memo(item, self.__vendor[item])
        if item in self.__recipes:
            return self.__memo(item, self.__eval_recipe(self.__recipes[item]))
        if item in self.__conversions:
            price = ItemCache.__accumulator(self.__conversions[item].items(),
                                            lambda k, v: self.eval_item(k) * v)
            if item not in self.__prices:
                return self.__memo(item, price)
            # Determine if conversion reduces the cost for the item.
            return self.__memo(item, min(self.__prices[item], price))
        if item not in self.__prices:
            raise RuntimeError("Item '{}' pricing data was undefined.".format(item))
        return self.__memo(item, self.__prices[item])

    def __eval_recipe(self, recipe: Recipe) -> int:
        return ItemCache.__accumulator(recipe.reagents.items(),
                                       lambda k, v: self.eval_item(k) * v) // recipe.supply

    def __memo(self, item: str, cost: int) -> int:
        self.__cache[item] = cost
        return cost

    @staticmethod
    def __accumulator(itr: Iterable, accumulator: Callable[[str, int], int]) -> int:
        adder = 0
        for k, v in itr:
            adder += accumulator(k, v)
        return adder
