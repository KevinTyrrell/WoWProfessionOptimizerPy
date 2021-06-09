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


from Recipe import Recipe

from random import random


class Crafter:
    def __init__(self, level: int, target: int):
        self.__level = level
        self.__target = target
        self.__inventory = {}

    """
    Crafts an item, awarding a possible skill-up based on random chance.
    
    @:param recipe: Recipe to be crafted.
    @:return bool: True if the crafter is now at his target skill level.
    """
    def craft(self, recipe: Recipe) -> bool:
        self.__inventory[recipe.name] = self.__inventory.get(recipe.name, 0) + recipe.supply
        if random() < recipe.skill_chance(self.__level):
            self.__level += 1
            # Indicate if we need to keep crafting.
            if self.__level >= self.__target:
                return True
        return False
