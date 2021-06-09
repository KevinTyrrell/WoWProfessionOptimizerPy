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


class Recipe:
    def __init__(self, name: str, details: dict):
        self.__name = name
        self.__skills = tuple(details["skills"])
        self.__supply = details["supply"]
        self.__spec = None if "specialization" not in details else details["specialization"]
        self.__reagents = details["reagents"]

    """
    Calculates the chance for a skill up to occur at a specific skill level.
    Skill Up Formula: chance = (greySkill - yourSkill) / (greySkill - yellowSkill)
    
    @:param skill: Current skill level.
    @:return chance: Chance for a skill up to occur (between [0.0, 1.0])
    """
    def skill_chance(self, skill: int) -> float:
        if skill < self.orange:
            raise ValueError("Insufficient skill to calculate skill chance: {0} (Req. {1})".format(skill, self.orange))
        if skill <= self.yellow:
            return 1  # Guaranteed chance for a skill up under these circumstances.
        if skill >= self.grey:
            return 0  # Guaranteed chance for no skill ups under these circumstances.
        return (self.grey - skill) / (self.grey - self.yellow)

    """
    @:return name: Name of the recipe.
    """
    @property
    def name(self) -> str:
        return self.__name

    """
    @:return supply: Number of items supplied from the recipe.
    """
    @property
    def supply(self) -> int:
        return self.__supply

    """
    @:return skill: Skill in which the recipe becomes orange.
    """
    @property
    def orange(self) -> int:
        return self.__skills[0]

    """
    @:return skill: Skill in which the recipe becomes yellow.
    """
    @property
    def yellow(self) -> int:
        return self.__skills[1]

    """
    @:return skill: Skill in which the recipe becomes grey.
    """
    @property
    def grey(self) -> int:
        return self.__skills[2]

    """
    @:return reagents: Reagents used to craft the recipe.
    """
    @property
    def reagents(self) -> dict:
        return self.__reagents

    """
    @:return specialization: Specialization required to craft the recipe.
    """
    @property
    def specialization(self) -> str:
        return self.__spec

    """
    @:return string: String representation of the recipe.
    """
    def __str__(self) -> str:
        return "{}[{},{},{},{}]{}".format(
            self.name, self.orange, self.yellow, self.yellow + (self.grey - self.yellow) // 2, self.grey,
            "" if self.__spec is None else "(" + self.__spec + ")")

    """
    @:return string: String representation of the recipe.
    """
    def __repr__(self) -> str:
        return self.__str__()
