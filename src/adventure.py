"""CSC111 Project 1: Text Adventure Game

Instructions (READ THIS FIRST!)
===============================

This Python module contains the code for Project 1. Please consult
the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2024 CSC111 Teaching Team
"""
from __future__ import annotations

import sys
from typing import Optional

from src.actions.context import Context
from src.direction import Direction
from src.game_data import World, Player, Location

DEFAULT_MENU = ['go <direction>', 'look', 'inventory', 'score', 'steps', 'quit', 'inspect', 'grab', 'drop']


# Note: You may add helper functions, classes, etc. here as needed
def prepare_world() -> tuple[World, Player, Location]:
    """
    Returns an instance of World, Player and starting Location by
    loading files from the assets folder.

    defaults.txt is a file containing only one single line, in the format:
        <initial starting location id> <maximum permitted steps>
    """
    with open("../gamedata/map.txt", "r") as world_map, \
            open("../gamedata/locations.txt", "r") as locations, \
            open("../gamedata/items.txt", "r") as items, \
            open("../gamedata/actions.txt", "r") as actions, \
            open("../gamedata/defaults.txt", "r") as defaults:
        starting_location_id_str, max_steps_str = defaults.readline().split(' ')

        wrld = World(world_map, locations, items, actions)
        x, y = wrld.get_location_position(
            location_id=int(starting_location_id_str),
            world_map=wrld.map
        )
        plyr = Player(x=x, y=y, max_steps=int(max_steps_str))
        loc = wrld.get_location(x, y)

        return wrld, plyr, loc


def handle_menu(loc: Location) -> None:
    """Helper function to handle the menu call in the main loop.
    """
    print("Menu Options:")
    for option in DEFAULT_MENU + [str(act) for act in loc.actions if not act.completed]:
        print('\t-', option)


def handle_inspect(loc: Location) -> None:
    """Helper function to handle the inspect call in the main loop.
    """
    if len(loc.items) == 0:
        print("You couldn't find any items here.")
    else:
        items_and_counts = {itm: loc.items.count(itm) for itm in loc.items}
        print("You have seen the following items:")
        for item, count in items_and_counts.items():
            print(f"×{count} {item}")


def handle_grab(choice: str, p: Player, loc: Location) -> None:
    """Helper function to handle the grab call in the main loop.
    """
    item_string = choice[5:].lower()
    item = next((itm for itm in loc.items if repr(itm) == item_string), None)
    if item is not None:  # or just not None, but this is more readable
        print(f"You have picked up {item}.")
        loc.items.remove(item)
        p.inventory.append(item)
        p.steps += 1
    else:
        print("You couldn't find that item.")


def handle_drop(choice: str, p: Player, loc: Location) -> None:
    """Helper function to handle the drop call in the main loop.
    """
    item_string = choice[5:].lower()
    item = next((itm for itm in p.inventory if repr(itm) == item_string), None)
    if item is not None:
        print(f"You dropped your {item}.")
        p.inventory.remove(item)
        loc.items.append(item)
        p.steps += 1
    else:
        print("You couldn't find that item in your inventory.")


def handle_go(direction: Direction, p: Player, wrld: World, loc: Location) -> Optional[Location]:
    """Helper function to handle the go call in the mail loop.
    """
    if direction in loc.allowed_movements:
        x_offset, y_offset = direction.offset()
        p.x, p.y = p.x + x_offset, p.y + y_offset
        p.steps += 1
        return wrld.get_location(p.x, p.y)
    else:
        print('That direction is blocked.')
        return None


def handle_inventory(p: Player) -> None:
    """Helper function to handle inventory call in the main loop.
    """
    inventory_string = [str(itm) for itm in p.inventory]
    items_and_counts = {itm: inventory_string.count(itm) for itm in inventory_string}
    if len(p.inventory) == 0:
        print('You have no items in your inventory.')
    else:
        print('You have the following items in your inventory:')
        for item, count in items_and_counts.items():
            print(f'×{count} {item}')


def handle_simple_commands(choice: str, p: Player, loc: Location) -> None:
    """A wrapped handler to reduce function complexity that computes
    various actions.
    """
    if choice == 'look':
        print(loc.descriptor.long_description)

    elif choice == 'inventory':
        handle_inventory(p)

    elif choice == 'score':
        print(f'Your score is {p.points}!')

    elif choice == 'steps':
        print(f'You have {p.steps}/{p.max_steps} steps')

    elif choice == 'quit':
        print("Bye!")
        sys.exit(0)


def main_loop(loc: Location, p: Player) -> Optional[Location]:
    """The main function that runs the adventure game, asking for choices.
    Return the new location if the location has changed, None otherwise.
    This function should be called inside a while loop.
    """
    choice = input("\nEnter action: ").strip().lower()

    if choice in {'menu', '[menu]', 'help'}:
        handle_menu(loc)

    elif choice == 'inspect':
        handle_inspect(loc)

    elif choice.startswith('grab'):
        handle_grab(choice, p, loc)

    elif choice.startswith('drop'):
        handle_drop(choice, p, loc)

    elif choice.startswith('go'):
        direction_string = choice[3:]

        if direction_string.lower() not in {'east', 'west', 'north', 'south'}:
            print(f"'{direction_string}' doesn't seem like a valid direction.")
            return None

        direction = Direction.from_str(direction_string)
        return handle_go(direction, p, world, loc)

    elif choice in {'look', 'inventory', 'score', 'quit', 'steps'}:
        handle_simple_commands(choice, p, loc)
    else:
        act = loc.get_action_by_string(choice)

        if act is None:
            print('Unknown command!')
            return None

        _ = act.execute(context=Context(world=world, player=p, location=loc), shallow=False)
        p.steps += 1

        if p.victory:
            return loc
    return None


if __name__ == "__main__":
    world, player, location = prepare_world()

    while not player.victory and player.steps < player.max_steps:
        location.visit(player)

        for action in world.background_actions:
            success = action.execute(context=Context(world=world, player=player, location=location), _shallow=True)

        for action in location.actions:
            action.execute(context=Context(world=world, player=player, location=location), shallow=True)

        while True:
            new_location = main_loop(location, player)
            if player.steps >= player.max_steps:
                break
            if new_location is not None:
                location = new_location
                break

    if player.victory:
        print(f'You won in {player.steps} moves! Your score was a whopping {player.points}!')
    else:
        print('You have missed your exam!')
