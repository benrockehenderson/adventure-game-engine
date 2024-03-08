"""CSC111 Project 1: Text Adventure Game Classes

Instructions (READ THIS FIRST!)
===============================

This Python module contains the main classes for Project 1, to be imported and used by
 the `adventure` module.
 Please consult the project handout for instructions and details.

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
from typing import Optional, TextIO
from dataclasses import dataclass

# from python_ta.contracts import check_contracts

from src.errors import LocationError, MapSyntaxError
from src.actions.action import Action, SingleAction, BackgroundAction
from src.actions.parser import ActionScriptParser
from src.direction import Direction


class Item:
    """An item in our text adventure game world.

    Instance Attributes:
        - name: The name of the item, which must be unique.
        - location_id: The location of the item. If the item is awarded via an action, this is None.

    Representation Invariants:
        - self.name != ''
        - self.location_id >= 0
    """
    name: str
    location_id: Optional[int]

    # The only thing you must NOT change is the name of this class: Item.
    # All item objects in your game MUST be represented as an instance of this class.
    def __init__(self, name: str, location_id: Optional[int]) -> None:
        """Initialize a new item.
        """
        self.name = name
        self.location_id = location_id

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        # The lowercase name of an item is the official representation (the id) of the item.
        return self.name.lower()


@dataclass
class LocationDescriptor:
    """A dataclass describing the position and description of a location.

    Instance Attributes:
        - position: The position tuple of this location on the world map.
        - location_id: The unique number of the location.
        - short_description: The short description of this location.
        - long_description: The long description of this location.

    Representation Invariants:
        - self.position[0] >= 0 and self.position[1] >= 0
        - self.location_id >= 0
        - self.short_description != ''
        - self.long_description != ''
    """
    position: tuple[int, int]
    location_id: int
    short_description: str
    long_description: str


# The only thing you must NOT change is the name of this class: Location.
# All locations in your game MUST be represented as an instance of this class.
@dataclass
class Location:
    """A location in our text adventure game world.

    Instance Attributes:
        - descriptor: The LocationDescriptor for this location, including location information.
        - allowed_movements: The list of allowed movements, either north/east/west/south. See `Direction`.
        - actions: The list of available actions in this location.
        - points: The number of points received from visiting this location.
        - items: The list of available items for pickup in this location.
        - already_visited: Whether this location was visited before.

    Representation Invariants:
        - self.position[0] >= 0 and self.position[1] >= 0
    """
    descriptor: LocationDescriptor
    allowed_movements: set[Direction]
    actions: list[SingleAction]
    points: int
    items: list[Item]
    already_visited: bool

    def available_actions(self) -> list[Action]:
        """
        Return the available actions in this location.
        The actions should depend on the items available in the location
        and the x,y position of this location on the world map.
        """
        return self.actions

    def visit(self, player: Player) -> None:
        """Increment player's points and add points for visiting the location.
        """
        if self.already_visited:
            print(self.descriptor.short_description)
        else:
            print(self.descriptor.long_description)
            player.points += self.points
            self.already_visited = True

    def get_action_by_string(self, action_string: str) -> Optional[Action]:
        """Return the
        """
        for action in self.available_actions():
            if repr(action) == f"{action_string.lower()}:{self.descriptor.location_id}":
                return action
        return None


class Player:
    """
    A Player in the text adventure game.

    Instance Attributes:
        - x: The x position of the player.
        - y: The y position of the player.
        - max_steps: The maximum steps the player can take.
        - inventory: The list of items the player is currently holding.
        - victory: Whether the player has won the game.
        - steps: Total steps the player has taken. This excludes "view" actions, such as inventory or inspect.
        - points: The total number of points the player has currently got.

    Representation Invariants:
        - self.x >= 0 and self.y >= 0
        - self.steps >= 0
        - self.max_steps >= 0
    """
    x: int
    y: int
    max_steps: int
    inventory: list[Item]
    victory: bool
    steps: int
    points: int

    def __init__(self, x: int, y: int, max_steps: int) -> None:
        """
        Initializes a new Player at position (x, y).
        """
        self.x = x
        self.y = y
        self.max_steps = max_steps
        self.inventory = []
        self.victory = False
        self.steps = 0
        self.points = 0

    def create_add_item(self, name: str, location_id: Optional[int]) -> None:
        """Create and add an item to the inventory of the player.
        """
        item = Item(name=name, location_id=location_id)
        self.inventory.append(item)


class World:
    """A text adventure game world storing all location, item and map data.

    Instance Attributes:
        - locations: A mapping from the unique location number to the location class.
        - map: A nested list representation of this world's map.
        - background_actions: A list of background actions that are executed when the player moves.

    Representation Invariants:
        - all(i >= 0 for i in self.locations)
    """
    locations: dict[int, Location]
    map: list[list[int]]
    background_actions: list[BackgroundAction]

    def __init__(
            self,
            map_data: TextIO,
            location_data: TextIO,
            items_data: TextIO,
            actions_data: TextIO
    ) -> None:
        """
        Initialize a new World for a text adventure game, based on the data in the given open files.

        - location_data: name of text file containing location data (format left up to you)
        - items_data: name of text file containing item data (format left up to you)
        """
        world_map = self.load_map(map_data)
        items = self.load_items(items_data)
        actions = self.load_actions(actions_data)
        self.locations = self.load_locations(location_data, items, actions, world_map)
        self.map = world_map
        self.background_actions = [action for action in actions if isinstance(action, BackgroundAction)]

    # NOTE: The method below is REQUIRED. Complete it exactly as specified.
    # noinspection PyMethodMayBeStatic
    def load_map(self, map_data: TextIO) -> list[list[int]]:
        """
        Store map from open file map_data as the map attribute of this object, as a nested list of integers like so:

        If map_data is a file containing the following text:
            1 2 5
            3 -1 4
        then load_map should assign this World object's map to be [[1, 2, 5], [3, -1, 4]].

        Return this list representation of the map.
        """
        map_grid = []
        lines = map_data.readlines()
        for line in lines:
            line = line.strip()
            if line != '':
                split = [int(i) for i in line.split(' ')]
                map_grid.append(split)
        return map_grid

    def get_location(self, x: int, y: int) -> Optional[Location]:
        """Return Location object associated with the coordinates (x, y) in the world map, if a valid location exists at
         that position. Otherwise, return None. (Remember, locations represented by the number -1 on the map should
         return None.)
        """
        if y >= len(self.map):
            return None
        if x >= len(self.map[y]):
            return None
        if self.map[y][x] == -1:
            return None
        return self.locations[self.map[y][x]]

    # =============================
    # ======== Item Parser ========
    # =============================

    @staticmethod
    def load_items(item_data: TextIO) -> list[Item]:
        """Load items from item_data into a list of items.
        The item data is in the format:

            <location id> <item name>

        where <item name> may include spaces. If <location id> is -1, then this item cannot be
        picked up from any location, and must be given to the user via an action result.
        """
        items = []
        for line in item_data.readlines():
            line = line.strip()
            if line != '':
                split = line.split(' ')
                location_id = int(split[0])
                name = ' '.join(split[1:])
                if location_id != -1:
                    items.append(Item(name=name, location_id=location_id))
                else:
                    items.append(Item(name=name, location_id=None))
        return items

    # ==================================
    # ======== Action Parsers ==========
    # ==================================

    @staticmethod
    def load_actions(actions_data: TextIO) -> list[Action]:
        """Parse the actions_data file, returning a list of actions.
        """
        actions = []
        lines = actions_data.readlines()
        current_segment = []
        for line in lines:
            line = line.strip()
            if line == "END":
                actions.append(World._parse_action_segment(current_segment))
                current_segment = []
            elif line != '':
                current_segment.append(line)
        return actions

    @staticmethod
    def _parse_action_segment(segment: list[str]) -> Action:
        """Parse an action segment and return it as an instance of Action.

        An action segment is any segment of actions.txt, from which the action can be constructed.
        Action segments are in the following format:

        <Action Name> <Action Location ID>
        <ActionScript Code>

        where <ActionScript Code> may span across multiple lines, until END. If <Action Location ID> is
        -1, it means that the action is a background action. Note that END is not included in the action segment.
        """
        split = segment[0].split(' ')
        action_location_id = int(split[-1])
        name = ' '.join(split[:-1])
        instructions = ActionScriptParser(segment[1:]).compile()

        if action_location_id == -1:
            return BackgroundAction(name=name, instructions=instructions)
        return SingleAction(name=name, action_location_id=action_location_id, instructions=instructions)

    # ==================================
    # ======== Location Parsers ========
    # ==================================

    # noinspection PyMethodMayBeStatic
    def load_locations(
            self,
            location_data: TextIO,
            items: list[Item],
            actions: list[Action],
            world_map: list[list[int]]
    ) -> dict[int, Location]:
        """Return a mapping from location id to the location instance while reading and
         building locations from the location data file.
        """
        locations = {}
        lines = location_data.readlines()
        current_segment = []
        for line in lines:
            line = line.strip()
            if line == "END":
                location = World._parse_location_segment(current_segment, items, actions, world_map)
                # if location.descriptor.location_id != -1:
                locations[location.descriptor.location_id] = location
                current_segment = []
            elif line != '':
                current_segment.append(line)
        return locations

    @staticmethod
    def _parse_location_segment(
            segment: list[str],
            items: list[Item],
            actions: list[Action],
            world_map: list[list[int]],
    ) -> Location:
        """Parse any location segment into a Location instance.

        A location segment is in the form:

        LOCATION <location id>
        <points>
        LOCK_DEFAULT <direction 1> <direction 2> (if any ...)
        <short description>
        <long description>

        where the third line starting with LOCK_DEFAULT is optional. LOCK_DEFAULT allows for the direction to
        be locked by default, even if it is physically accessible according to the map. The direction must then
        be unlocked by actions, or could remain locked. If the third line is omitted, no directions are locked.

        Implementation note: Although we could have easily opted into locking a specific place from all four
        directions, locking from one direction gives us more flexibility. Maps could be enhanced with certain
        blocks in which players are forced to move to a specific direction. To lock an entire room, one must either
        set it to -1 on the map, or lock other rooms leading there.
        """
        must_be_location, location_id = segment[0].split(' ')
        if must_be_location != "LOCATION":
            raise MapSyntaxError("Location declarations must start with LOCATION")

        location_id = int(location_id)
        position = World.get_location_position(location_id, world_map)
        allowed_movements = World._get_free_directions(position, world_map)

        points_received = int(segment[1])
        short_description, long_description = World._parse_middle_segment(segment[2:], allowed_movements)

        descriptor = LocationDescriptor(
            position=position,
            location_id=location_id,
            short_description=short_description,
            long_description=long_description
        )

        return Location(
            descriptor=descriptor,
            allowed_movements=allowed_movements,
            actions=[
                action for action in actions if isinstance(
                    action,
                    SingleAction
                ) and action.action_location_id == location_id
            ],
            points=points_received,
            items=[item for item in items if item.location_id == location_id],
            already_visited=False
        )

    @staticmethod
    def _parse_middle_segment(segment: list[str], allowed_movements: set[Direction]) -> tuple[str, str]:
        """Parse the middle part of the location segment, returning the short and long descriptions, in order.
        The set of allowed movements must be passed onto this function as there's a possibility of a LOCK
        occurring in the middle segment.
        """
        short_description_or_lock = segment[0]
        offset = 0
        if short_description_or_lock.startswith("LOCK_DEFAULT"):
            locked_directions_str = short_description_or_lock.split()[1:]
            for locked_direction in locked_directions_str:
                locked_direction = Direction.from_str(locked_direction)
                allowed_movements.remove(locked_direction)
            offset = 1

        short_description = segment[0 + offset]
        long_description = '\n'.join(segment[1 + offset:])
        return short_description, long_description

    @staticmethod
    def get_location_position(location_id: int, world_map: list[list[int]]) -> tuple[int, int]:
        """Search and return for the location_id on the world_map, based on map.txt file.
        """
        i = 0
        column_count = len(world_map[0])
        while i < len(world_map) * column_count:
            y = i // column_count
            x = i % column_count
            if world_map[y][x] == location_id:
                return x, y
            i += 1
        raise LocationError("Unable to find location in map")

    @staticmethod
    def _get_free_directions(position: tuple[int, int], world_map: list[list[int]]) -> set[Direction]:
        """Return the free directions according to the world map. This does not account for the locked
        directions, which must be removed later.
        """
        x, y = position
        top_free = y > 0 and world_map[y - 1][x] != -1
        bottom_free = (y < (len(world_map) - 1)) and world_map[y + 1][x] != -1
        left_free = x > 0 and world_map[y][x - 1] != -1
        right_free = (x < (len(world_map[0]) - 1)) and world_map[y][x + 1] != -1

        free_directions = set()
        if top_free:
            free_directions.add(Direction.NORTH)
        if bottom_free:
            free_directions.add(Direction.SOUTH)
        if left_free:
            free_directions.add(Direction.WEST)
        if right_free:
            free_directions.add(Direction.EAST)
        return free_directions


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['src.errors', 'src.actions.action', 'src.actions.parser', 'src.direction', 'src.actions'],
        'allowed-io': ['Location.visit']
    })
