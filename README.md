# Adventure Game and Engine

[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL%203.0-blue.svg)](LICENSE)

This project features a novel adventure game that is really easy to customize using a custom programming language called ActionScript.

The game comes with a prebuilt example, which is under the [gamedata](gamedata) folder, but you may customize the game as you wish - there are no hardcoded values, hence the adventure game 'engine'.

## ActionScript

ActionScript is a small domain-specific language for our adventure game with an instruction set that is designed to program puzzles (called Actions). ActionScript code is written in the file actions.txt under gamedata, and it looks like the following:

```
-print("You notice there's a T-Card scanner next to you.")
$has_item("T-Card")
#print("You need to have your T-Card with you!")
#print("A security guard approaches you...")
$unlock_direction_at_point(14, "WEST")
$print("You have unlocked the west entrance.")
+print("You have already unlocked the west entrance.")
```

and many more instructions to add/take points, items, and even to win the game.

ActionScript is composed of 4 different execution modes, indicated by $, +, -, and #. $ execution mode indicates that the instruction will be executed once, and if the instruction fails it will be caught by the following # operators (you can think of # as a try-except block).
\+ and - execution modes are 'shallow,' meaning that they will be executed automatically even if the user doesn't invoke the action, allowing us to indicate the existence of the action to the user. + is executed if the user has already completed the action, and - is executed if the user has not completed the action yet. Each action has a name and location (as described in actions.txt), and each action can be executed by typing the name into the console at the correct location. If the location of an action is -1, it means it's a `Background Action' that is invisible to the player, which may be used to create certain effects, such as curses, multipliers, bonuses, etc.

## Customizing the Game

You may also customize the game map by editing map.txt under gamedata. Similarly, you can change the starting point under defaults; add new items at items.txt, and locations under locations.txt. 

# License

AGPL-3.0-only - See [LICENSE](LICENSE) for details.
