# Game name TBD
This is a simple Pygame platfomer that I am making and will probably continue to develop for a while until I get bored.

If you are reading this feel free to pull my repo and work on it yourself!

# CONTROLS

| MECHANIC | CONTROL |
| ------ | ------ |
| *RIGHT* | Right arrow |
| *LEFT* | Left arrow |
| *JUMP* | Up arrow |
| *DASH* | Space |
| *PUSH* | Down arrow |
| *RESET* | R |

Show hitboxes **(WIP)** C

# MECHANICS BREAKDOWN
## Horizontal Movement :
While on ground, the player has basically complete control over their x velocity, by holding **LEFT** or **RIGHT**. 

However, when the player is in the air, the horizontal movement will be a lot more gradual and will have actual velocity, an interesting air strafe mechanic that works well with walljumping and wallsliding.

## Jumping :
When the player presses **JUMP** the players y velocity will be set to `JUMP_STRENGTH` (determined in settings.py). Simple!

## Wall sliding :
Hold **LEFT** or **RIGHT** against a wall to start a wall slide, slowing the players fall to a speed determined by SLIDE_SPEED in settings.py. Not possible to perform while on ground.

## Walljumping :
Originally, the walljumping was designed to be chainable on a single wall, but to make gameplay more challenging, I decided you have to chain walljumps between separate walls. To achieve a walljump, hold <RIGHT> or <LEFT> against a wall to begin a wall slide, then press <JUMP> to jump backwards off the wall with opposite momentum.

## Double jump :
While in the air, either that be because the player jumped or has fallen off a ledge, the player will be granted an additional jump provided the player has not already used up the double jump opportunity. This double jump flag will be reset once the player contacts the ground again.

## Dash :
<DASH> while holding **RIGHT** or <LEFT> to launch the player with high vertical velocity in the corresponding direction. Upon contact with a wall, the dash will be stopped immediately. If the player dashes just before pressing <JUMP>, the player will be rewarded with additional upwards momentum. This is an advanced mechanic.

## Pushing :
When holding <RIGHT> or <LEFT> while walking against a box and on the ground, if the player holds <PUSH>, the box can be displaced by the player.

## Buttons :
If a button is pressed, the door with the corresponding id will disable, allowing the player through. 

Buttons can be activated 2 ways as of now. Either by the player colliding with them, or by a box colliding with them.

There are 2 types of buttons; hold and press. Holdbuttons are required to be held down constantly in order to disable the door, however, when a pressbutton is held down for any instance of time, it will stay held down until the level resets (player dies or level reset is called).

---

# FILE EXPLANATIONS
- `main.py`
The main file that imports all other files and runs them either through it, or the files it imports.
- `level.py`
The file that runs code for interpreting the level layout, drawing the objects with screen shake, and some game logic such as spike collisions and button / door logic. Called through `main.py`.
- `player.py`
The file that handles player logic such as controls, collisions, movement and other methods. Called through `level.py`, `buttons.py`.
- `tile.py`
The file that contains the `Tile` class, which is the base block for the level. Represented by **X**. Called through `level.py`.
- `spikes.py`
The file that contains the `Spike` class, main danger for the player. Represented by either **A** or **V**. Called through `level.py`.
- `box.py`
The file that contains the `Box` class. Contains a majority of box logic in the game. Represented by **B**. Called through `level.py`.
- `buttons.py`
The file that contains the `PressButton` and `HoldButton` classes. Contains logic and ids for the buttons. Represented by **T** for pressbuttons and **H** for holdbuttons. Called by `level.py`, `doors.py`.
- `doors.py`
The file that contains the `Door`, `PressDoor` and `HoldDoor` classes. Handles logic for doors. Represented by **O** for pressdoors and **D** for holddoors. Called through `level.py`.
- `settings.py`
The file that contains a majority of constant variables that can be accessed throughout the whole directory. Called through `main.py`, `level.py`, `player.py`, `buttons.py`.
- `map.py`
Contains level layouts in list form. Uses different symbols to show different objects *(See table below)*. Called through `settings.py`, `buttons.py`, `level.py`.

## Map legend
| Symbol | Object |
| -------- | -------- |
| X | Tile |
| P | Player start |
| A | Spike (up) |
| V | Spike (down) |
| B | Box |
| T | PressButton |
| H | HoldButton |
| O | PressDoor |
| D | HoldDoor |