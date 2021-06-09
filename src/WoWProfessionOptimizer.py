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

from JSONLoader import JSONLoader
from RecipeManager import RecipeManager
from ItemCache import ItemCache

import argparse
from random import seed


""" Minimum and maximum skill levels for World of Warcraft professions. """
__MIN_SKILL_LEVEL, __MAX_SKILL_LEVEL = 1, 375
""" Set seed for deterministic skill increases. """
__SET_SEED = 37 * 11 * 93


def main() -> None:
    parser = argparse.ArgumentParser(description="Tool used to find the cheapest possible crafting route"
                                                 "through a World of Warcraft profession.",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("profession", type=lambda e: e.upper().capitalize(),
                        help="Profession to be leveled.")

    def argparse_skill_range(arg: str) -> int:
        arg = int(arg)
        # Argument exception handler for skill parameters.
        if arg < __MIN_SKILL_LEVEL or arg > __MAX_SKILL_LEVEL:
            raise argparse.ArgumentTypeError("Skill level must be within bounds [{0},{1}]"
                                             .format(__MIN_SKILL_LEVEL, __MAX_SKILL_LEVEL))
        return arg

    parser.add_argument("start", default=1, type=argparse_skill_range,
                        help="Current profession skill level.")
    parser.add_argument("target", default=375, type=argparse_skill_range,
                        help="Target profession skill level.")
    parser.add_argument("prices", type=str,
                        help="Path to auction house pricing JSON file.")
    parser.add_argument("-s", "--spec", dest="spec", default=None, type=str,
                        help="Enables use of specialization-only recipes (e.g. 'Goblin', 'Gnomish').")
    parser.add_argument("-x", "--exclude", dest="exclude", default=[], nargs="*",
                        help="List of recipes to exclude from the crafting process.")

    include = {}

    # Parser for optional 'include' parameter: recipes may be proceeded by quantities.
    def argparse_include_parse():
        prev_str = None
        next_funct = None

        def await_str(arg: str):
            nonlocal prev_str, next_funct
            if arg in include:
                raise RuntimeError("Optional 'include' parameter found duplicate recipe '{0}'.".format(arg))
            include[arg] = 1
            prev_str = arg
            next_funct = await_num

        def await_num(arg: str):
            nonlocal prev_str, next_funct
            include[prev_str] = int(arg)
            next_funct = await_str

        def controller(arg: str):
            nonlocal next_funct
            if arg.isnumeric():
                if next_funct == await_str:
                    raise RuntimeError("Optional 'include' parameter found quantity "
                                       "'{0}' without a preceding recipe.".format(arg))
            elif next_funct == await_num:
                next_funct = await_str
            next_funct(arg)
            return arg
        next_funct = await_str
        return controller
    argparse_include_parse = argparse_include_parse()

    parser.add_argument("-i", "--include", dest="include", type=argparse_include_parse, nargs="*",
                        help="List of recipes (with quantities) to include in the crafting process."
                             " e.g. \"Fel Iron Bar\" 2 \"Adamantite Bar\"")

    args = parser.parse_args()
    exclude = set(args.exclude)
    seed(__SET_SEED)

    loader = JSONLoader()
    manager = RecipeManager(loader.register(args.profession), include, exclude, args.spec)
    item_cache = ItemCache(manager, loader, args.prices)

    print(item_cache.eval_item("Turbo-Charged Flying Machine"))

if __name__ == "__main__":
    main()
