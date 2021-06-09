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

from json import load


class JSONLoader:
    __DEFAULT_RESOURCE_PATH = "res/"
    __JSON_FILE_EXTENSION = ".json"

    def __init__(self):
        self.__registers = {}

    """
    Loads a JSON file from the storage medium, registering it with a name.
    Once registered, JSON files can be retrieved using said name.
    
    @:param name: Name to register the JSON file with.
    @:param path: Path to the JSON file. If unspecified, differs to `__DEFAULT_RESOURCE_PATH` + name.
    @:return JSON object:
    """
    def register(self, name: str = None, path: str = None) -> any([list, dict]):
        if path is None:
            path = self.__DEFAULT_RESOURCE_PATH + name + self.__JSON_FILE_EXTENSION
        file = open(path)
        jso = load(file)
        self.__registers[name] = jso
        return jso

    """
    Retrieves a registered JSON object by name.
    
    :param register: Registered name of the JSON object.
    :return JSON object:
    :raises ValueError: if no such register exists.
    """
    def get(self, register: str):
        if register not in self.__registers:
            raise ValueError("Register '{0}' does not exist.".format(register))
        return self.__registers[register]
