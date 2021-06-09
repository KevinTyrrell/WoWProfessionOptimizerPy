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

from typing import List, Dict


class RecipeManager:
    def __init__(self, recipes, include, exclude, spec):
        recipes = {k: recipes[k] for k in set(recipes) - exclude}  # Filter out exclusions.
        self.__recipes = {k: Recipe(k, v) for k, v in recipes.items()}  # Construct formal recipes.
        """
        self.__recipes = {k: v for k, v in self.__recipes.items()
                          # Ensure recipes have no specialization or match our specialization.
                          if v.specialization is None or v.specialization == spec}
        """
        for recipe in include:
            if recipe not in recipes:
                raise RuntimeError("Unknown recipe name: {}".format(recipe))

    """
    @:param skill: Current skill level.
    @:return list: List of recipes which can grant skill increases.
    """
    def relevant_recipes(self, skill: int) -> List[Recipe]:
        return [e for e in self.__recipes.values() if e.orange <= skill < e.grey]

    """
    @:return recipes: Dictionary of all applicable recipes.
    Recipes which require different specializations are omitted.
    """
    @property
    def recipes(self) -> Dict[str, Recipe]:
        return self.__recipes
