# Tho Vu
# thv7pas
# CS1110

import uvage
import random

"""
Game Description:
This game is called ship vs ship, where the goal is to destroy the other person's
space ship. Each player will have the ability to shoot bullets.
There will also be some power ups the player can get, like
shields or an extra life. Whoever has no lives left first will lose.

Basic Features:

User input: each player will have an up, down, left, right movement, and the ability to shoot bullets
Game Over: Whoever runs out of lifes first loses.
Graphics: Basic images of ship, exploding ship, and powerups

Additional Features:

Restart from game over: either player presses Enter/Return to restart the game if someone loses
Collectibles: Basic powerups that each player can get, like shield or an extra life
Two players: This is a two player game where each person tries to destory each other's ship and
Sprite animations: Things like ship explosion, or powerup animations
"""

##############################################################################################################################################################################
#                                                                                   Instructions                                                                             #
#  Controls:                                                                                                                                                                 #
#           Player 1: arrows keys for movemnet and numpad 0 for shooting                                                                                                     #
#           Player 2: wasd keys for movemnet and space for shooting                                                                                                          #
#                                                                                                                                                                            #
#  Powerups:                                                                                                                                                                 #
#           Heart:  add an extra life to the player who grabs it. The maximum amount of lives a player can have is 5.                                                        #                                                      #
#           Shield: add an extra layer of shield that blocks a bullet shot. The maximum amount of shields the player can have is 3.                                          #
#                   NOTE: Shields do not prevent player to player collision (i.e. ship colliding with each other), so both player will lose a life.                          #
#                                                                                                                                                                            #
#  To start the game, press enter/return. Each player will only be able to shoot one bullet at a time. Once the bullet reaches out of bounds, the player can shoot again.    #
#  Whoever runs out of lives first loses. The screen will display the winner, and is able to restart the game if either player presses enter/return                          #
#                                                                                                                                                                            #
##############################################################################################################################################################################

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800


def setup():
    """
    Sets up everything in its right position including ships, lives, shield, walls, etc.
    """
    global camera, p1rocket, p2rocket, p1facingRight, p2facingRight, wall1, wall2, wall3, wall4, p1life, p2life,  p1bullet, p2bullet, game_on, game_over, game_off
    global p1Shield, p2Shield, powerup, life, shield, explode, shipFrame, p2died, p1died, shieldSprite, shieldFrame, heartFrame, background
    game_on = False  # Game is starting
    game_off = False  # Game is paused since a player died
    game_over = True   # Game is done since a player has lost the game
    camera = uvage.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
    background = uvage.from_image(800, 600, 'background.jpg')
    p1life = 3  # Player 1 lives
    p2life = 3  # Player 2 lives
    p1Shield = 0  # Player 1 shield
    p2Shield = 0  # Player 2 shield
    heartFrame = 0  # Sprite animation for heart powerup
    shipFrame = 0   # Sprite animation for ship exploding
    shieldFrame = 0  # Sprite animation for shield powerup

    # Checks who died in the round
    p2died = False
    p1died = False

    # Checks if the rocket is facing right
    p1facingRight = True
    p2facingRight = True

    # Setup rocket image
    p1rocket = uvage.from_image(100, 300, 'p1.png')
    p1rocket.scale_by(.1)
    p1rocket.rotate(270)
    p2rocket = uvage.from_image(700, 300, 'p2.png')
    p2rocket.scale_by(.1)
    p2rocket.rotate(90)

    # Draw walls
    wall1 = uvage.from_color(0, 300, "blue", 1, 1000)
    wall2 = uvage.from_color(800, 300, "blue", 1, 1000)
    wall3 = uvage.from_color(400, 600, "black", 1000, 1)
    wall4 = uvage.from_color(400, 0, "blue", 1000, 1)

    # Each ship's bullet
    p1bullet = uvage.from_image(-100, 700, "missle.png")
    p1bullet.scale_by(.01)
    p2bullet = uvage.from_image(-100, 700, "missle.png")
    p2bullet.scale_by(.01)

    # Loading in the sprites
    explode = uvage.load_sprite_sheet("explode.png", rows=4, columns=8)
    shieldSprite = uvage.load_sprite_sheet("shield.png", rows=3, columns=3)

    # Random number generator for powerup location
    random_x1 = random.randint(50, int(.9*SCREEN_WIDTH))
    random_x2 = random.randint(50, int(.9*SCREEN_WIDTH))
    random_y1 = random.randint(50, int(.9*SCREEN_HEIGHT))
    random_y2 = random.randint(50, int(.9*SCREEN_HEIGHT))
    life = uvage.from_image(random_x1, random_y1, "red 32px1.png")
    shield = uvage.from_image(random_x2, random_y2, shieldSprite[2])
    shield.scale_by(.1)


def start_game():
    """
    This function sets all of the values to the correct starting values
    """
    global game_on, game_over, p1life, p2life, p1Shield, p2Shield
    camera.draw(background)
    if game_over:
        camera.draw(uvage.from_text(
            400, 250, "Press Enter to start game", 50, "Green", bold=False))
        if uvage.is_pressing("return"):
            game_on = True
            game_over = False
            p1life = 3
            p2life = 3
            p1Shield = 0
            p2Shield = 0
            camera.clear('white')


def draw_environment():
    """
    This function draws all of the walls, lives, scores, and background
    """
    camera.draw(wall1)
    camera.draw(wall2)
    camera.draw(wall3)
    camera.draw(uvage.from_text(75, 20, "P1 Lives: " + str(p1life), 30, "Red", bold=True))
    camera.draw(uvage.from_text(711, 20, "P2 Lives: " + str(p2life), 30, "Red", bold=True))
    camera.draw(uvage.from_text(82, 40, "P1 Shield: " + str(p1Shield), 30, "Red", bold=True))
    camera.draw(uvage.from_text(718, 40, "P2 Shield: " + str(p2Shield), 30, "Red", bold=True))


def handle_xmovement():
    """
    This function handles the movement of the player
    """
    global camera, p1rocket, p2rocket, heartFrame, p1facingRight, p2facingRight, p1bullet, p2bullet
    is_moving = False
    if game_on:

        # Player 1 movement
        if uvage.is_pressing("right arrow"):
            if not p1facingRight:
                p1facingRight = True
                p1rocket.rotate(180)
            is_moving = True
            p1rocket.x += 8
        if uvage.is_pressing("left arrow"):
            if p1facingRight:
                p1facingRight = False
                p1rocket.rotate(180)
            is_moving = True
            p1rocket.x -= 8
        if uvage.is_pressing("up arrow"):
            p1rocket.y -= 8
        if uvage.is_pressing("down arrow"):
            p1rocket.y += 8
        if not is_moving:
            p1rocket.image = 'p1.png'
        if uvage.is_pressing("keypad 0") and p1facingRight and (800 < p1bullet.x or p1bullet.x < 0):
            xCoor=p1rocket.x + 50
            yCoor=p1rocket.y
            p1bullet=uvage.from_image(xCoor, yCoor, "missle.png")
            p1bullet.scale_by(.05)
            p1bullet.rotate(270)
            p1bullet.xspeed=10
        if uvage.is_pressing("keypad 0") and not p1facingRight and (800 < p1bullet.x or p1bullet.x < 0):
            xCoor=p1rocket.x - 55
            yCoor=p1rocket.y
            p1bullet=uvage.from_image(xCoor, yCoor, "missle.png")
            p1bullet.scale_by(.05)
            p1bullet.rotate(90)
            p1bullet.xspeed=-10

        # Player 2 movement
        if uvage.is_pressing("d"):
            if p2facingRight:
                p2facingRight=False
                p2rocket.rotate(180)
            is_moving=True
            p2rocket.x += 8
        if uvage.is_pressing("a"):
            if not p2facingRight:
                p2facingRight=True
                p2rocket.rotate(180)
            is_moving=True
            p2rocket.x -= 8
        if uvage.is_pressing("w"):
            p2rocket.y -= 8
        if uvage.is_pressing("s"):
            p2rocket.y += 8
        if not is_moving:
            p2rocket.image='p2.png'
        if uvage.is_pressing("space") and not p2facingRight and (800 < p2bullet.x or p2bullet.x < 0):
            xCoor=p2rocket.x + 50
            yCoor=p2rocket.y
            p2bullet=uvage.from_image(xCoor, yCoor, "missle.png")
            p2bullet.scale_by(.05)
            p2bullet.rotate(270)
            p2bullet.xspeed=10
        if uvage.is_pressing("space") and p2facingRight and (800 < p2bullet.x or p2bullet.x < 0):
            xCoor=p2rocket.x - 50
            yCoor=p2rocket.y
            p2bullet=uvage.from_image(xCoor, yCoor, "missle.png")
            p2bullet.scale_by(.05)
            p2bullet.rotate(90)
            p2bullet.xspeed=-10

        # Makes sure the player doesn't go out of bounds
        p1rocket.move_to_stop_overlapping(wall1)
        p1rocket.move_to_stop_overlapping(wall2)
        p1rocket.move_to_stop_overlapping(wall3)
        p1rocket.move_to_stop_overlapping(wall4)
        p2rocket.move_to_stop_overlapping(wall1)
        p2rocket.move_to_stop_overlapping(wall2)
        p2rocket.move_to_stop_overlapping(wall3)
        p2rocket.move_to_stop_overlapping(wall4)

        # moves the bullet if the player shoots
        p1bullet.move_speed()
        p2bullet.move_speed()

        # draw bullet
        camera.draw(p1bullet)
        camera.draw(p2bullet)

    # draw ship
    camera.draw(p1rocket)
    camera.draw(p2rocket)


def handle_powerup():
    """
    This function deals with powerups and player interaction with it. Also, handles sprite animations of powerups
    """
    global camera, powerup, p1life, p2life, p1Shield, p2Shield, life, shield, heartFrame, shipFrame, shieldFrame

    if game_on:

        # extra life powerup sprite animation
        heartFrame += .1
        if heartFrame >= 3:
            heartFrame=0
        if heartFrame == 0:
            life.image='Red 32px1.png'
        elif heartFrame == 1:
            life.image='Red 32px2.png'
        elif heartFrame == 2:
            life.image='RedGolden32px1.png'
        else:
            life.image='RedGolden32px2.png'

        # Shield powerup sprite animation
        shieldFrame += 1
        if shieldFrame >= 7:
            shieldFrame=0
        shield.image=shieldSprite[int(shieldFrame)]

        # Adds life if player touches heart powerup
        if p1rocket.touches(life):
            if p1life <= 4:
                p1life += 1
            random_x = random.randint(50, int(.9*SCREEN_WIDTH))
            random_y = random.randint(50, int(.9*SCREEN_HEIGHT))
            life.x = random_x
            life.y = random_y
        if p2rocket.touches(life):
            if p2life <= 4:
                p2life += 1
            random_x = random.randint(50, int(.9*SCREEN_WIDTH))
            random_y = random.randint(50, int(.9*SCREEN_HEIGHT))
            life.x = random_x
            life.y = random_y

        # Adds a shield if a player touches shield powerup
        if p1rocket.touches(shield):
            if p1Shield <= 2:
                p1Shield += 1
            random_x = random.randint(50, int(.9*SCREEN_WIDTH))
            random_y = random.randint(50, int(.9*SCREEN_HEIGHT))
            shield.x = random_x
            shield.y = random_y
        if p2rocket.touches(shield):
            if p2Shield <= 2:
                p2Shield += 1
            random_x = random.randint(50, int(.9*SCREEN_WIDTH))
            random_y = random.randint(50, int(.9*SCREEN_HEIGHT))
            shield.x = random_x
            shield.y = random_y

        # draw shield powerup
        camera.draw(life)
        camera.draw(shield)


def explosion():
    """
    This function handles the ship's explosion if some get hit
    """
    global game_on, game_off, p2Shield, p1Shield, shipFrame, p1died, p2died

    # Player 1 explosion
    if p1died and not p2died:
        if shipFrame != 31:
            shipFrame += 1
            p1rocket.image = explode[int(shipFrame)]
            if shipFrame == 31:
                p1rocket.image=explode[0]
                p1died = False

    # Player 2 explosion
    elif p2died and not p1died:
        if shipFrame != 31:
            shipFrame += 1
            p2rocket.image = explode[int(shipFrame)]
            if shipFrame == 31:
                p2rocket.image = explode[0]
                p2died = False

    # Both player die at the same time
    else:
        if shipFrame != 31:
            shipFrame += 1
            p1rocket.image = explode[int(shipFrame)]
            p2rocket.image = explode[int(shipFrame)]
            if shipFrame == 31:
                p1rocket.image = explode[0]
                p2rocket.image = explode[0]
                p1died = False
                p2died = False


def reset():
    """
    This ship resets the ship back to its original state once a round is over
    """
    global game_on, game_off, p2Shield, p1Shield

    # Text to tell the player how to start game
    camera.draw(uvage.from_text(400, 100, "press enter for next round", 50, 'green', bold=True))

    # Centers the rocket back to the correct position and values
    p1bullet.center = [-100, 0]
    p2bullet.center = [-100, 0]
    p1bullet.xspeed = 0
    p2bullet.xspeed = 0
    p1bullet.move_speed()
    p2bullet.move_speed()
    p1Shield = 0
    p2Shield = 0

    # Start game
    if uvage.is_pressing("return"):
        game_on = True
        game_off = False
        p1rocket.image = 'p1.png'
        p2rocket.image = 'p2.png'
        p1rocket.center = [100, 300]
        p2rocket.center = [700, 300]


def bullet():
    """
    Handles bullet interaction and ship to ship interactions
    """
    global p1life, p2life, p1Shield, p2Shield, game_on, game_off, p1died, p2died, shipFrame

    # Game over if one ship or both ship reaches 0 lives
    if p2life == 0 or p1life == 0:
        gameOver()
        return

    # Lose one stack of shield if a bullet hits the ship with shield or loses one life if the ship has no shield
    if p1bullet.touches(p2rocket) and p2Shield != 0:
        p2Shield -= 1
        p1bullet.x = -100
        p1bullet.xspeed = 0
        p1bullet.move_speed()
    elif p1bullet.touches(p2rocket) and p1Shield == 0:
        p2life -= 1
        game_on = False
        game_off = True
        p2died = True
        shipFrame = 0

    # Lose one stack of shield if a bullet hits the ship with shield or loses one life if the ship has no shield
    if p2bullet.touches(p1rocket) and p1Shield != 0:
        p1Shield -= 1
        p2bullet.x = -100
        p2bullet.xspeed = 0
        p2bullet.move_speed()
    elif p2bullet.touches(p1rocket) and p1Shield == 0:
        p1life -= 1
        game_on = False
        game_off = True
        p1died = True
        shipFrame = 0

    # Both players lose a life if they touch regardless if they have a shield or not
    if p1rocket.touches(p2rocket) or p2rocket.touches(p1rocket):
        p1life -= 1
        p2life -= 1
        if p1rocket.right_touches(p2rocket) or p2rocket.left_touches(p1rocket):
            p1rocket.x = p1rocket.x + 50
            p2rocket.x = p2rocket.x - 50
        if p2rocket.right_touches(p1rocket) or p1rocket.left_touches(p2rocket):
            p1rocket.x = p1rocket.x - 100
            p2rocket.x = p2rocket.x + 100
        if p1rocket.top_touches(p2rocket) or p2rocket.bottom_touches(p1rocket):
            p1rocket.y = p1rocket.y - 100
            p2rocket.y=p2rocket.y + 100
        if p2rocket.top_touches(p1rocket) or p1rocket.bottom_touches(p2rocket):
            p1rocket.y = p1rocket.y + 100
            p2rocket.y = p2rocket.y - 100
        game_on = False
        game_off = True
        p1died = True
        p2died = True
        shipFrame = 0

    # calls helper functions
    if game_off:
        explosion()
        reset()


def gameOver():
    """
    This function determines which player won and allows the player to restart the game
    """
    global p1life, p2life, game_over, game_on

    # Both players won or lost, depends on how you see it
    if p1life == 0 and p2life == 0:
        game_over = True
        game_on = False
        camera.draw(uvage.from_text(400, 100, "Tie!", 50, 'green', bold=True))
        camera.draw(uvage.from_text(400, 250, "Press Enter to start game", 50, "Green", bold=False))
        if uvage.is_pressing("return"):
            start_game()

    # Player 1 lost
    if p1life == 0 and p2life != 0:
        game_over = True
        game_on = False
        camera.draw(uvage.from_text(400, 100, "Player 2 wins!", 50, 'green', bold=True))
        if uvage.is_pressing("return"):
            start_game()

    # Player 2 lost
    if p2life == 0 and p1life != 0:
        game_over = True
        game_on = False
        camera.draw(uvage.from_text(400, 100, "Player 1 wins!", 50, 'green', bold=True))
        if uvage.is_pressing("return"):
            start_game()


def tick():
    """
    Main driver function
    """
    camera.clear('black')
    start_game()
    draw_environment()
    handle_xmovement()
    handle_powerup()
    bullet()
    gameOver()
    camera.display()


setup()
ticks_per_second=120
uvage.timer_loop(ticks_per_second, tick)