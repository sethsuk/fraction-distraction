from classes import Player
import pygame
import sys
from fractions import Fraction
import random


"""-----GLOBAL SETUP/VARIABLES/ASSETS-----"""


# initializes the game and pygame fonts
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
pygame.display.set_caption("Fraction Distraction")

# initializes game sound effects
button_sound = pygame.mixer.Sound("Assets/button.mp3")
error_sound = pygame.mixer.Sound("Assets/error.mp3")

# basic global values
screen_width = 1280
screen_height = 720
mouse_click = False

# creates the main screen of the game
main_screen = pygame.display.set_mode((screen_width, screen_height))

# loads in the assets (background, fonts, and assets)
start_background = pygame.image.load("Assets/start_bg.jpg")
big_font = pygame.font.Font("Assets/zx_spectrum.ttf", 50)
medium_font = pygame.font.Font("Assets/zx_spectrum.ttf", 35)
small_font = pygame.font.Font("Assets/zx_spectrum.ttf", 25)

money = pygame.image.load("Assets/money.png")
money = pygame.transform.scale(money, (89, 80))
money_rect = money.get_rect()
money_rect.center = (1250, 675)

heart = pygame.image.load("Assets/heart.png")
heart = pygame.transform.scale(heart, (54, 45))
heart_rect = heart.get_rect()
heart_rect.center = (screen_width // 2 + 300, 680)


"""-----SUPPORTING FUNCTIONS-----"""


def draw_text(text, font, color, surface, x, y):
    """creates a text box

    @param text: string of the text
    @param font: font of the text, should be in the .ttf file format
    @param color: color of the text, can be in r,g,b or string: https://www.discogcodingacademy.com/turtle-colours
    @param surface: the screen that the text will be on
    @param x: x-position of the text - middle of the text box
    @param y: y-position of the text - middle of the text bos
    """

    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)


def draw_text_outline(text, font, color, surface, x, y):
    """utilizes draw_text to create a black outline

    :param text: string of the text
    :param font: font of the text, should be in the .ttf file format
    :param color: color of the text, can be in r,g,b or string: https://www.discogcodingacademy.com/turtle-colours
    :param surface: the screen that the text will be on
    :param x: x-position of the text - middle of the text box
    :param y: y-position of the text - middle of the text bos
    """

    if font == small_font:
        draw_text(text, font, color, surface, x, y)
    else:
        black_color = (0, 0, 0)

        # Draws the black outline
        draw_text(text, font, black_color, surface, x - 2, y - 2)
        draw_text(text, font, black_color, surface, x - 2, y + 2)
        draw_text(text, font, black_color, surface, x + 2, y - 2)
        draw_text(text, font, black_color, surface, x + 2, y + 2)

        # Draws the real text against black background text
        draw_text(text, font, color, surface, x, y)


def universal_UI(home_button, quit_button, mx, my, click):
    """creates the basic home button (top left) and quit button (top right)

    :param quit_button: rect of the quit button
    :param home_button: rect of the home button
    :param mx: x-pos of mouse
    :param my: y-pos of mouse
    :param click: click boolean, True if player is clicking
    """

    if home_button.collidepoint((mx, my)):
        pygame.draw.rect(main_screen, (64, 128, 230), home_button, 0, 5)
        if click:
            button_sound.play()
            menu(mouse_click, "Fraction Distraction")
    else:
        pygame.draw.rect(main_screen, (46, 102, 191), home_button, 0, 5)

    if quit_button.collidepoint((mx, my)):
        pygame.draw.rect(main_screen, (64, 128, 230), quit_button, 0, 5)
        if click:
            button_sound.play()
            sys.exit()
    else:
        pygame.draw.rect(main_screen, (46, 102, 191), quit_button, 0, 5)

    draw_text_outline("Home", small_font, (255, 255, 255), main_screen, 90, 50)
    draw_text_outline("Quit", small_font, (255, 255, 255), main_screen, 1190, 50)


def money_UI():
    """creates the UI for the total money the player has"""

    main_screen.blit(money, money_rect)
    draw_text_outline(f"${player.total_money}", medium_font, (255, 255, 255), main_screen, 1160, 680)


def item_UI():
    """creates the UI for the amount of items the player has"""

    draw_text_outline(f"X2: {player.items['double_bet']}", medium_font, (255, 255, 255), main_screen,
                      screen_width // 2 - 300, 680)
    draw_text_outline(f"X3: {player.items['triple_bet']}", medium_font, (255, 255, 255), main_screen,
                      screen_width // 2, 680)
    main_screen.blit(heart, heart_rect)
    draw_text_outline(f": {player.items['life_line']}", medium_font, (255, 255, 255), main_screen,
                      screen_width // 2 + 360, 680)


def answer_choice_text(correct_option, answer, fake_1, fake_2):
    """generates the random answer choices

    :param correct_option: the correct option, 1 = left, 2 = middle, 3= right
    :param answer: the correct answer fraction
    :param fake_1: fake answer fraction
    :param fake_2: fake answer fraction
    """

    if correct_option == 1:
        draw_text_outline(f"{answer}", medium_font, (255, 255, 255), main_screen, (screen_width // 2) - 400,
                          screen_height // 2 + 240)  # answer 1
        draw_text_outline(f"{fake_1}", medium_font, (255, 255, 255), main_screen, (screen_width // 2),
                          screen_height // 2 + 240)  # answer 2
        draw_text_outline(f"{fake_2}", medium_font, (255, 255, 255), main_screen, (screen_width // 2) + 400,
                          screen_height // 2 + 240)  # answer 3
    elif correct_option == 2:
        draw_text_outline(f"{fake_1}", medium_font, (255, 255, 255), main_screen, (screen_width // 2) - 400,
                          screen_height // 2 + 240)  # answer 1
        draw_text_outline(f"{answer}", medium_font, (255, 255, 255), main_screen, (screen_width // 2),
                          screen_height // 2 + 240)  # answer 2
        draw_text_outline(f"{fake_2}", medium_font, (255, 255, 255), main_screen, (screen_width // 2) + 400,
                          screen_height // 2 + 240)  # answer 3
    else:
        draw_text_outline(f"{fake_1}", medium_font, (255, 255, 255), main_screen, (screen_width // 2) - 400,
                          screen_height // 2 + 240)  # answer 1
        draw_text_outline(f"{fake_2}", medium_font, (255, 255, 255), main_screen, (screen_width // 2),
                          screen_height // 2 + 240)  # answer 2
        draw_text_outline(f"{answer}", medium_font, (255, 255, 255), main_screen, (screen_width // 2) + 400,
                          screen_height // 2 + 240)  # answer 3


def tutorial_steps(mode):
    """provides the steps needed for each tutorial method

    :param mode: the tutorial mode the player is on
    """

    if mode == "Find Y-intercept Form":
        return ['6x + 7y = 9',
                'Isolate 7y: 7y = -6x + 9', 'Divide equation by 1/7: 1/7 × (7y = -6x + 9)',
                '(1/7 × 7y) = (1/7 × -6x) + (1/7 × 9)', '7/7y = -6x/7 + 9/7', 'y = -6x/7 + 9/7', 'DONE']
    elif mode == "Divide":
        return ['(4/7) ÷  (9/5)', 'Multiply 4/7 by reciprocal of 9/5', '4/7 × 5/9', '(4 × 5) / (7 × 9)', '20/63',
                'DONE']
    elif mode == "Multiply":
        return ['7/9 × 2/3', '(7 × 2) / (9 × 3)', '14/27', 'DONE']
    elif mode == "Find LCD":
        return ['Find Least Common Denominator of 2/9 and 7/6', 'Factorize 9 and 6', '9 = 3 × 3  and 6 = 3 × 2',
                'LCD = 3 × 3 × 2', 'LCD = 18', 'DONE']
    elif mode == 'Transform Fraction':
        return ['3 2/3', '3 + 2/3', '3 = 9/3', '9/3 + 2/3', '(9+2)/3', '11/3', 'DONE']
    elif mode == "Add":
        return ['4/9 + 8/3', 'LCD = 9', '(1/1 × 4/9) + (3/3 × 8/3)', '4/9 + 24/9', '(4+24)/9', '28/9', 'DONE']
    elif mode == "Subtract":
        return ['3/7 - 5/14', 'LCD = 14', '(2/2 × 3/7) - (1/1 × 5/14)', '6/14 - 5/14', '(6-5)/14', '1/14', 'DONE']


def nothing_to_see_here():
    #           .-.
    #          o   \     .-.
    #             .----.'   \
    #           .'o)  / `.   o
    #          /         |
    #          \_)       /-.
    #            '_.`    \  \
    #             `.      |  \
    #              |       \ |
    #          .--/`-.     / /
    #        .'.-/`-. `.  .\|
    #       /.' /`._ `-    '-.
    #  ____(|__/`-..`-   '-._ \
    # |`------.'-._ `      ||\ \
    # || #   /-.   `   /   || \|
    # ||   #/   `--'  /  /_::_|)__
    # `|____|-._.-`  /  ||`--------`
    #       \-.___.` | / || #      |
    #        \       | | ||   #  # |
    #        /`.___.'\ |.`|________|
    #        | /`.__.'|'.`
    #      __/ \    __/ \
    #     /__.-.)  /__.-.)
    # A WILD BUG ON ITS WAY TO WORK, MESSING UP YOUR CODE!

    #              _______
    #             / .   . \
    #            I         I
    # --------OOO---|   |---OOO--------
    #               (___)
    # KILROY WAS HERE :)
    pass


"""-----GAME SCREENS-----"""


def menu(click, message):
    """the main menu screen for the game

    :param click: state of the mouse, True if player pressed Mouse 1
    :param message: string for the message at the top of the screen
    """

    """---------------------------------SETUP-------------------------------"""
    pygame.mouse.set_visible(True)  # deals with the visibility of the mouse. allows  user to see and move their mouse

    # Rects for the two buttons
    start_button = pygame.Rect(screen_width // 2 - 420, screen_height // 2 - 80, 370, 80)
    tutorial_button = pygame.Rect(screen_width // 2 - 420, screen_height // 2 + 40, 370, 80)
    quit_button = pygame.Rect(screen_width // 2 + 50, screen_height // 2 + 40, 370, 80)
    shop_button = pygame.Rect(screen_width // 2 + 50, screen_height // 2 - 80, 370, 80)

    """"----------------------------------LOOP-------------------------------"""
    while True:
        main_screen.blit(start_background, (0, 0))  # creates the background image

        mx, my = pygame.mouse.get_pos()  # deals with the mouse positions

        # Check for mouse over and mouse click on the start button, button changes color on mouse over
        if start_button.collidepoint((mx, my)):
            pygame.draw.rect(main_screen, (64, 128, 230), start_button, 0, 5)
            if click:
                button_sound.play()
                betting_screen()
        else:
            pygame.draw.rect(main_screen, (46, 102, 191), start_button, 0, 5)

        # Check for mouse over and mouse click on the quit button, button changes color on mouse over
        if tutorial_button.collidepoint((mx, my)):
            pygame.draw.rect(main_screen, (240, 20, 20), tutorial_button, 0, 5)
            if click:
                button_sound.play()
                tutorial_select("Select Tutorial")
        else:
            pygame.draw.rect(main_screen, (196, 16, 16), tutorial_button, 0, 5)

        # Check for mouse over and mouse click on the quit button, button changes color on mouse over
        if quit_button.collidepoint((mx, my)):
            pygame.draw.rect(main_screen, (240, 20, 20), quit_button, 0, 5)
            if click:
                button_sound.play()
                sys.exit()
        else:
            pygame.draw.rect(main_screen, (196, 16, 16), quit_button, 0, 5)

        # Check for mouse over and mouse click on the quit button, button changes color on mouse over
        if shop_button.collidepoint((mx, my)):
            pygame.draw.rect(main_screen, (240, 20, 20), shop_button, 0, 5)
            if click:
                button_sound.play()
                shop_screen()
        else:
            pygame.draw.rect(main_screen, (196, 16, 16), shop_button, 0, 5)

        # Draws text on the menu screen
        draw_text_outline(message, big_font, (255, 255, 255), main_screen, screen_width // 2, screen_height // 2 - 170)
        draw_text_outline("Shop/Stats", medium_font, (255, 255, 255), main_screen, screen_width // 2 + 230,
                          screen_height // 2 - 40)
        draw_text_outline("Betting", medium_font, (255, 255, 255), main_screen, screen_width // 2 - 230,
                          screen_height // 2 - 40)
        draw_text_outline("Quit", medium_font, (255, 255, 255), main_screen, screen_width // 2 + 230,
                          screen_height // 2 + 80)
        draw_text_outline("Tutorial", medium_font, (255, 255, 255), main_screen, screen_width // 2 - 230,
                          screen_height // 2 + 80)

        # basic UI elements
        item_UI()
        money_UI()

        click = False  # resets the click event, prevents one click -> two actions

        # Checks for game events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True

        pygame.display.update()
        clock.tick(60)


def betting_screen():
    """the screen for selecting which type of bet the player wants"""

    """---------------------------------SETUP-------------------------------"""

    click = False  # resets the mouse click to avoid a bug where one click would trigger two events

    pygame.mouse.set_visible(True)  # deals with the visibility of the mouse. allows  user to see and move their mouse

    table = pygame.image.load("Assets/table.png")
    table = pygame.transform.scale(table, (765, 464))
    table_rec = table.get_rect()
    table_rec.center = (640, 200)

    smallbet_button = pygame.Rect((screen_width // 2) - 500, (screen_height // 2) + 60, 200, 80)
    medbet_button = pygame.Rect((screen_width // 2) - 100, (screen_height // 2) + 60, 200, 80)
    bigbet_button = pygame.Rect((screen_width // 2) + 300, (screen_height // 2) + 60, 200, 80)
    home_button = pygame.Rect(30, 20, 120, 60)
    quit_button = pygame.Rect(1130, 20, 120, 60)

    """"----------------------------------LOOP-------------------------------"""

    while True:  # screen loop
        main_screen.blit(start_background, (0, 0))  # creates the background image

        mx, my = pygame.mouse.get_pos()  # deals with the mouse positions

        universal_UI(home_button, quit_button, mx, my, click)

        """BET BUTTONS"""

        # Check for mouse over and mouse click on the easy button, button changes color on mouse over
        if smallbet_button.collidepoint((mx, my)):
            pygame.draw.rect(main_screen, (240, 20, 20), smallbet_button, 0, 5)
            if click:
                button_sound.play()
                wager_screen("small")
        else:
            pygame.draw.rect(main_screen, (196, 16, 16), smallbet_button, 0, 5)

        if medbet_button.collidepoint((mx, my)):
            pygame.draw.rect(main_screen, (240, 20, 20), medbet_button, 0, 5)
            if click:
                button_sound.play()
                wager_screen("med")
        else:
            pygame.draw.rect(main_screen, (196, 16, 16), medbet_button, 0, 5)

        if bigbet_button.collidepoint((mx, my)):
            pygame.draw.rect(main_screen, (240, 20, 20), bigbet_button, 0, 5)
            if click:
                button_sound.play()
                wager_screen("big")
        else:
            pygame.draw.rect(main_screen, (196, 16, 16), bigbet_button, 0, 5)

        draw_text_outline("Bet Small", small_font, (255, 255, 255), main_screen, (screen_width // 2) - 400,
                          screen_height // 2 + 100)
        draw_text_outline("Bet Med", small_font, (255, 255, 255), main_screen, (screen_width // 2),
                          screen_height // 2 + 100)
        draw_text_outline("Bet Big", small_font, (255, 255, 255), main_screen, (screen_width // 2) + 400,
                          screen_height // 2 + 100)

        # basic UI elements
        item_UI()
        money_UI()

        click = False  # resets the mouse click

        # Checks for game events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True

        main_screen.blit(table, table_rec)
        draw_text_outline("Bet Difficulty!", big_font, (255, 255, 255), main_screen, 645, 200)
        draw_text_outline("Hard Bets:", medium_font, (255, 255, 255), main_screen, 645, 250)
        draw_text_outline("Greater Rewards", medium_font, (255, 255, 255), main_screen, 645, 285)

        # updates the game and tick
        pygame.display.update()
        clock.tick(60)


def wager_screen(mode):
    """the screen for selecting which wager the player wants

    :param mode: the mode the player chose, string
    """

    """---------------------------------SETUP-------------------------------"""

    click = False  # resets the mouse click to avoid a bug where one click would trigger two events

    pygame.mouse.set_visible(True)  # deals with the visibility of the mouse. allows  user to see and move their mouse

    table = pygame.image.load("Assets/table.png")
    table = pygame.transform.scale(table, (765, 464))
    table_rec = table.get_rect()
    table_rec.center = (640, 200)

    wager1_button = pygame.Rect((screen_width // 2) - 500, (screen_height // 2) + 60, 200, 80)
    wager2_button = pygame.Rect((screen_width // 2) - 100, (screen_height // 2) + 60, 200, 80)
    wager3_button = pygame.Rect((screen_width // 2) + 300, (screen_height // 2) + 60, 200, 80)
    home_button = pygame.Rect(30, 20, 120, 60)
    quit_button = pygame.Rect(1130, 20, 120, 60)

    """"----------------------------------LOOP-------------------------------"""

    while True:  # screen loop
        main_screen.blit(start_background, (0, 0))  # creates the background image

        mx, my = pygame.mouse.get_pos()  # deals with the mouse positions

        universal_UI(home_button, quit_button, mx, my, click)

        """WAGER BUTTONS"""

        # Check for mouse over and mouse click on the button, button changes color on mouse over
        if player.total_money < 15:
            pygame.draw.rect(main_screen, (97, 12, 3), wager1_button, 0, 5)
            if click and wager1_button.collidepoint((mx, my)):
                error_sound.play()
        elif wager1_button.collidepoint((mx, my)):
            pygame.draw.rect(main_screen, (240, 20, 20), wager1_button, 0, 5)
            if click:
                button_sound.play()
                player.bet(15)
                betting_game_screen(mode)
        else:
            pygame.draw.rect(main_screen, (196, 16, 16), wager1_button, 0, 5)

        if player.total_money < 25:
            pygame.draw.rect(main_screen, (97, 12, 3), wager2_button, 0, 5)
            if click and wager2_button.collidepoint((mx, my)):
                error_sound.play()
        elif wager2_button.collidepoint((mx, my)):
            pygame.draw.rect(main_screen, (240, 20, 20), wager2_button, 0, 5)
            if click:
                button_sound.play()
                player.bet(25)
                betting_game_screen(mode)
        else:
            pygame.draw.rect(main_screen, (196, 16, 16), wager2_button, 0, 5)

        if player.total_money < 50:
            pygame.draw.rect(main_screen, (97, 12, 3), wager3_button, 0, 5)
            if click and wager3_button.collidepoint((mx, my)):
                error_sound.play()
        elif wager3_button.collidepoint((mx, my)):
            pygame.draw.rect(main_screen, (240, 20, 20), wager3_button, 0, 5)
            if click:
                button_sound.play()
                player.bet(50)
                betting_game_screen(mode)
        else:
            pygame.draw.rect(main_screen, (196, 16, 16), wager3_button, 0, 5)

        draw_text_outline("$15", small_font, (255, 255, 255), main_screen, (screen_width // 2) - 400,
                          screen_height // 2 + 100)
        draw_text_outline("$25", small_font, (255, 255, 255), main_screen, (screen_width // 2),
                          screen_height // 2 + 100)
        draw_text_outline("$50", small_font, (255, 255, 255), main_screen, (screen_width // 2) + 400,
                          screen_height // 2 + 100)

        # basic UI elements
        item_UI()
        money_UI()

        click = False  # resets the mouse click

        # Checks for game events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True

        main_screen.blit(table, table_rec)

        # draw last, so it's on top of the table
        draw_text_outline("Select Wager!", big_font, (255, 255, 255), main_screen, 640, 200)

        # updates the game and tick
        pygame.display.update()
        clock.tick(60)


def betting_game_screen(mode):
    """the screen for main problem/items/answer choices

    :param mode: the mode the player chose, string
    """

    """---------------------------------SETUP-------------------------------"""

    click = False  # resets the mouse click to avoid a bug where one click would trigger two events

    pygame.mouse.set_visible(True)  # deals with the visibility of the mouse. allows  user to see and move their mouse

    table = pygame.image.load("Assets/table.png")
    table = pygame.transform.scale(table, (765, 464))
    table_rec = table.get_rect()
    table_rec.center = (640, 200)

    # Problem and answer generation with common factors
    if mode == "small":
        operator = random.randint(0, 1)
        common_factor = random.randint(2, 12)

        if operator == 0:
            fraction_1 = Fraction(common_factor * random.randint(1, 4), random.randint(1, 41))
            fraction_2 = Fraction(random.randint(1, 27), common_factor * random.randint(1, 3))
            answer = fraction_1 * fraction_2
            answer_string = f"{fraction_1} × {fraction_2}"
        else:
            fraction_1 = Fraction(common_factor * random.randint(1, 4), random.randint(1, 41))
            fraction_2 = Fraction(common_factor * random.randint(1, 3), random.randint(1, 27))
            answer = fraction_1 / fraction_2
            answer_string = f"{fraction_1} ÷ {fraction_2}"
    elif mode == "med":
        operator = random.randint(0, 3)
        common_factor = random.randint(12, 24)

        if operator == 0:
            fraction_1 = Fraction(common_factor * random.randint(2, 5), random.randint(5, 50))
            fraction_2 = Fraction(random.randint(5, 50), common_factor * random.randint(2, 4))
            answer = fraction_1 * fraction_2
            answer_string = f"{fraction_1} × {fraction_2}"
        elif operator == 1:
            fraction_1 = Fraction(common_factor * random.randint(2, 5), random.randint(5, 50))
            fraction_2 = Fraction(common_factor * random.randint(2, 4), random.randint(5, 50))
            answer = fraction_1 / fraction_2
            answer_string = f"{fraction_1} ÷ {fraction_2}"
        elif operator == 2:
            fraction_1 = Fraction(random.randint(5, 50), common_factor * random.randint(2, 5))
            fraction_2 = Fraction(random.randint(5, 50), common_factor * random.randint(2, 4))
            answer = fraction_1 + fraction_2
            answer_string = f"{fraction_1} + {fraction_2}"
        else:
            fraction_1 = Fraction(random.randint(5, 50), common_factor * random.randint(2, 5))
            fraction_2 = Fraction(random.randint(5, 50), common_factor * random.randint(2, 4))
            answer = fraction_1 - fraction_2
            answer_string = f"{fraction_1} - {fraction_2}"
    else:
        operator = random.randint(0, 9)
        common_factor = random.randint(14, 31)

        if operator == 0:
            fraction_1 = Fraction(common_factor * random.randint(3, 7), random.randint(15, 99))
            fraction_2 = Fraction(random.randint(15, 99), common_factor * random.randint(5, 11))
            answer = fraction_1 * fraction_2
            answer_string = f"{fraction_1} × {fraction_2}"
        elif operator == 1 or operator == 2:
            fraction_1 = Fraction(common_factor * random.randint(3, 7), random.randint(15, 99))
            fraction_2 = Fraction(common_factor * random.randint(5, 11), random.randint(15, 99))
            answer = fraction_1 / fraction_2
            answer_string = f"{fraction_1} ÷ {fraction_2}"
        elif operator == 3 or operator == 4 or operator == 5:
            fraction_1 = Fraction(random.randint(15, 99), common_factor * random.randint(3, 7))
            fraction_2 = Fraction(random.randint(15, 99), common_factor * random.randint(5, 11))
            answer = fraction_1 + fraction_2
            answer_string = f"{fraction_1} + {fraction_2}"
        else:
            fraction_1 = Fraction(random.randint(15, 99), common_factor * random.randint(3, 7))
            fraction_2 = Fraction(random.randint(15, 99), common_factor * random.randint(5, 11))
            answer = fraction_1 - fraction_2
            answer_string = f"{fraction_1} - {fraction_2}"

    fake_answer_1 = answer * Fraction(random.randint(1, 3), random.randint(2, 5))
    fake_answer_2 = answer * Fraction(random.randint(1, 6), random.randint(3, 9))
    while fake_answer_1 == fake_answer_2 or fake_answer_1 == answer or fake_answer_2 == answer:  # Validates the answers
        fake_answer_1 = answer * Fraction(random.randint(1, 3), random.randint(2, 5))
        fake_answer_2 = answer * Fraction(random.randint(1, 6), random.randint(3, 9))

    correct_answer = random.randint(1, 3)  # Between choice 1, 2, and 3

    # Button recs
    item1_button = pygame.Rect((screen_width // 2) - 500, (screen_height // 2) + 60, 200, 80)
    item2_button = pygame.Rect((screen_width // 2) - 100, (screen_height // 2) + 60, 200, 80)
    item3_button = pygame.Rect((screen_width // 2) + 300, (screen_height // 2) + 60, 200, 80)
    ans1 = pygame.Rect((screen_width // 2) - 550, (screen_height // 2) + 200, 300, 80)
    ans2 = pygame.Rect((screen_width // 2) - 150, (screen_height // 2) + 200, 300, 80)
    ans3 = pygame.Rect((screen_width // 2) + 250, (screen_height // 2) + 200, 300, 80)

    # Item booleans toggles
    double_active = False
    triple_active = False

    """"----------------------------------LOOP-------------------------------"""

    while True:  # screen loop
        main_screen.blit(start_background, (0, 0))  # creates the background image

        mx, my = pygame.mouse.get_pos()  # deals with the mouse positions

        """ITEM BUTTONS"""

        # Check for mouse over and mouse click on the easy button, button changes color on mouse over
        if double_active:
            pygame.draw.rect(main_screen, (8, 82, 3), item1_button, 0, 5)
            if click and item1_button.collidepoint((mx, my)):
                error_sound.play()
        elif player.items["double_bet"] == 0:
            pygame.draw.rect(main_screen, (97, 12, 3), item1_button, 0, 5)
            if click and item1_button.collidepoint((mx, my)):
                error_sound.play()
        elif item1_button.collidepoint((mx, my)):
            pygame.draw.rect(main_screen, (240, 20, 20), item1_button, 0, 5)
            if click:
                button_sound.play()
                player.items["double_bet"] -= 1
                player.money_on_table *= 2
                double_active = True
        else:
            pygame.draw.rect(main_screen, (196, 16, 16), item1_button, 0, 5)

        if triple_active:
            pygame.draw.rect(main_screen, (8, 82, 3), item2_button, 0, 5)
            if click and item2_button.collidepoint((mx, my)):
                error_sound.play()
        elif player.items["triple_bet"] == 0:
            pygame.draw.rect(main_screen, (97, 12, 3), item2_button, 0, 5)
            if click and item2_button.collidepoint((mx, my)):
                error_sound.play()
        elif item2_button.collidepoint((mx, my)):
            pygame.draw.rect(main_screen, (240, 20, 20), item2_button, 0, 5)
            if click:
                button_sound.play()
                player.items["triple_bet"] -= 1
                player.money_on_table *= 3
                triple_active = True
        else:
            pygame.draw.rect(main_screen, (196, 16, 16), item2_button, 0, 5)

        if player.items["life_line"] == 0:
            pygame.draw.rect(main_screen, (97, 12, 3), item3_button, 0, 5)
            if click and item3_button.collidepoint((mx, my)):
                error_sound.play()
        elif item3_button.collidepoint((mx, my)):
            pygame.draw.rect(main_screen, (240, 20, 20), item3_button, 0, 5)
            if click:
                button_sound.play()
                player.items["life_line"] -= 1
                player.money_on_table = 0
                betting_screen()
        else:
            pygame.draw.rect(main_screen, (196, 16, 16), item3_button, 0, 5)

        """ANSWER BUTTONS"""

        if ans1.collidepoint((mx, my)):
            pygame.draw.rect(main_screen, (240, 20, 20), ans1, 0, 5)
            if click:
                button_sound.play()
                if correct_answer == 1:
                    results(mode, True, answer, answer_string)
                else:
                    results(mode, False, answer, answer_string)
        else:
            pygame.draw.rect(main_screen, (196, 16, 16), ans1, 0, 5)

        if ans2.collidepoint((mx, my)):
            pygame.draw.rect(main_screen, (240, 20, 20), ans2, 0, 5)
            if click:
                button_sound.play()
                if correct_answer == 2:
                    results(mode, True, answer, answer_string)
                else:
                    results(mode, False, answer, answer_string)
        else:
            pygame.draw.rect(main_screen, (196, 16, 16), ans2, 0, 5)

        if ans3.collidepoint((mx, my)):
            pygame.draw.rect(main_screen, (240, 20, 20), ans3, 0, 5)
            if click:
                button_sound.play()
                if correct_answer == 3:
                    results(mode, True, answer, answer_string)
                else:
                    results(mode, False, answer, answer_string)
        else:
            pygame.draw.rect(main_screen, (196, 16, 16), ans3, 0, 5)

        main_screen.blit(table, table_rec)
        draw_text_outline(answer_string, big_font, (255, 255, 255), main_screen, (screen_width // 2), 200)

        draw_text_outline("X2 Wager", small_font, (255, 255, 255), main_screen, (screen_width // 2) - 400,
                          screen_height // 2 + 100)
        draw_text_outline("X3 Wager", small_font, (255, 255, 255), main_screen, (screen_width // 2),
                          screen_height // 2 + 100)
        draw_text_outline("Life Line", small_font, (255, 255, 255), main_screen, (screen_width // 2) + 400,
                          screen_height // 2 + 100)

        # Assigning answers to the corresponding options
        answer_choice_text(correct_answer, answer, fake_answer_1, fake_answer_2)

        # Basic UI elements
        item_UI()
        money_UI()

        click = False  # resets the mouse click

        # Checks for game events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                player.lose()
                quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True

        # updates the game and tick
        pygame.display.update()
        clock.tick(60)


def results(mode, outcome, answer, question):
    """the screen for the results of the bet"""

    """---------------------------------SETUP-------------------------------"""

    click = False  # resets the mouse click to avoid a bug where one click would trigger two events

    pygame.mouse.set_visible(True)  # deals with the visibility of the mouse. allows  user to see and move their mouse

    if outcome:
        money_won = player.win(mode)
    else:
        wage = player.money_on_table
        player.lose()

    table = pygame.image.load("Assets/table.png")
    table = pygame.transform.scale(table, (765, 464))
    table_rec = table.get_rect()
    table_rec.center = (640, 200)

    home_button = pygame.Rect(30, 20, 120, 60)
    quit_button = pygame.Rect(1130, 20, 120, 60)

    """"----------------------------------LOOP-------------------------------"""

    while True:  # screen loop
        main_screen.blit(start_background, (0, 0))  # creates the background image

        mx, my = pygame.mouse.get_pos()  # deals with the mouse positions

        universal_UI(home_button, quit_button, mx, my, click)

        if outcome:
            draw_text_outline(f"Correct! +${money_won}", big_font, (255, 255, 255), main_screen, (screen_width // 2),
                              screen_height // 2 + 100)
        else:
            draw_text_outline(f"Incorrect! -${wage}", big_font, (255, 255, 255), main_screen, (screen_width // 2),
                              screen_height // 2 + 100)
            draw_text_outline(f"Correct Answer: {answer}", big_font, (255, 255, 255), main_screen, (screen_width // 2),
                              screen_height // 2 + 150)

        # basic UI elements
        item_UI()
        money_UI()

        click = False  # resets the mouse click

        # Checks for game events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True

        main_screen.blit(table, table_rec)

        # draw last, so it's on top of the table image
        draw_text_outline(question, big_font, (255, 255, 255), main_screen, (screen_width // 2), 200)

        # updates the game and tick
        pygame.display.update()
        clock.tick(60)


def shop_screen():
    """the screen for the shop and progress"""

    """---------------------------------SETUP-------------------------------"""
    click = False  # resets the mouse click to avoid a bug where one click would trigger two events

    pygame.mouse.set_visible(True)  # deals with the visibility of the mouse. allows  user to see and move their mouse

    # Rects for the buttons
    double_bet_button = pygame.Rect(screen_width // 2 - 420, screen_height // 2 - 80, 370, 80)
    triple_bet_button = pygame.Rect(screen_width // 2 - 420, screen_height // 2 + 20, 370, 80)
    life_line_button = pygame.Rect(screen_width // 2 - 420, screen_height // 2 + 120, 370, 80)
    completed_tutorial_trophy = pygame.Rect(screen_width // 2 + 50, screen_height // 2 - 80, 370, 80)
    earn_money_trophy = pygame.Rect(screen_width // 2 + 50, screen_height // 2 + 20, 370, 80)
    bet_won_trophy = pygame.Rect(screen_width // 2 + 50, screen_height // 2 + 120, 370, 80)
    home_button = pygame.Rect(30, 20, 120, 60)
    quit_button = pygame.Rect(1130, 20, 120, 60)

    # Trophy booleans toggles
    tutorial_active = False
    money_active = False
    bet_active = False

    """"----------------------------------LOOP-------------------------------"""

    while True:
        main_screen.blit(start_background, (0, 0))  # creates the background image

        mx, my = pygame.mouse.get_pos()  # deals with the mouse positions

        universal_UI(home_button, quit_button, mx, my, click)

        """ITEM BUTTONS"""

        if player.total_money < 20:
            pygame.draw.rect(main_screen, (97, 12, 3), double_bet_button, 0, 5)
            if click and double_bet_button.collidepoint((mx, my)):
                error_sound.play()
        elif double_bet_button.collidepoint((mx, my)):
            pygame.draw.rect(main_screen, (240, 20, 20), double_bet_button, 0, 5)
            if click:
                button_sound.play()
                player.items["double_bet"] += 1
                player.total_money -= 20
        else:
            pygame.draw.rect(main_screen, (196, 16, 16), double_bet_button, 0, 5)

        if player.total_money < 35:
            pygame.draw.rect(main_screen, (97, 12, 3), triple_bet_button, 0, 5)
            if click and triple_bet_button.collidepoint((mx, my)):
                error_sound.play()
        elif triple_bet_button.collidepoint((mx, my)):
            pygame.draw.rect(main_screen, (240, 20, 20), triple_bet_button, 0, 5)
            if click:
                button_sound.play()
                player.items["triple_bet"] += 1
                player.total_money -= 35
        else:
            pygame.draw.rect(main_screen, (196, 16, 16), triple_bet_button, 0, 5)

        if player.total_money < 30:
            pygame.draw.rect(main_screen, (97, 12, 3), life_line_button, 0, 5)
            if click and life_line_button.collidepoint((mx, my)):
                error_sound.play()
        elif life_line_button.collidepoint((mx, my)):
            pygame.draw.rect(main_screen, (240, 20, 20), life_line_button, 0, 5)
            if click:
                button_sound.play()
                player.items["life_line"] += 1
                player.total_money -= 30
        else:
            pygame.draw.rect(main_screen, (196, 16, 16), life_line_button, 0, 5)

        """ACHIEVEMENT BUTTONS"""

        if completed_tutorial_trophy.collidepoint((mx, my)):
            pygame.draw.rect(main_screen, (240, 20, 20), completed_tutorial_trophy, 0, 5)
            if click:
                button_sound.play()
                tutorial_active = not tutorial_active
        else:
            pygame.draw.rect(main_screen, (196, 16, 16), completed_tutorial_trophy, 0, 5)

        if earn_money_trophy.collidepoint((mx, my)):
            pygame.draw.rect(main_screen, (240, 20, 20), earn_money_trophy, 0, 5)
            if click:
                button_sound.play()
                money_active = not money_active
        else:
            pygame.draw.rect(main_screen, (196, 16, 16), earn_money_trophy, 0, 5)

        if bet_won_trophy.collidepoint((mx, my)):
            pygame.draw.rect(main_screen, (240, 20, 20), bet_won_trophy, 0, 5)
            if click:
                button_sound.play()
                bet_active = not bet_active
        else:
            pygame.draw.rect(main_screen, (196, 16, 16), bet_won_trophy, 0, 5)

        # Draws text on the screen
        draw_text_outline("Distracting Shop", big_font, (255, 255, 255), main_screen, screen_width // 2,
                          screen_height // 2 - 170)
        draw_text_outline("X2 Bet-$20", medium_font, (255, 255, 255), main_screen, screen_width // 2 - 230,
                          screen_height // 2 - 40)
        draw_text_outline("X3 Bet-$35", medium_font, (255, 255, 255), main_screen, screen_width // 2 - 230,
                          screen_height // 2 + 60)
        draw_text_outline("Life Line-$30", medium_font, (255, 255, 255), main_screen, screen_width // 2 - 234,
                          screen_height // 2 + 160)  # shifts it a little to the left to make it fit the rect

        """TOGGLED TEXTS"""

        if tutorial_active:
            if len(player.tutorials_completed) == 7:
                draw_text_outline(f"Completed All", medium_font, (255, 255, 255),
                                  main_screen, screen_width // 2 + 240, screen_height // 2 - 40)
            else:
                draw_text_outline(f"{len(player.tutorials_completed)} Completed!", medium_font, (255, 255, 255),
                                  main_screen, screen_width // 2 + 240, screen_height // 2 - 40)
        else:
            draw_text_outline("Tutorials!", medium_font, (255, 255, 255), main_screen, screen_width // 2 + 230,
                              screen_height // 2 - 40)

        if money_active:
            draw_text_outline(f"${player.total_money_won} Won!", medium_font, (255, 255, 255), main_screen,
                              screen_width // 2 + 240, screen_height // 2 + 60)
        else:
            draw_text_outline("Money Won", medium_font, (255, 255, 255), main_screen, screen_width // 2 + 230,
                              screen_height // 2 + 60)

        if bet_active:
            draw_text_outline(f"{player.bet_won} Bets Won!", medium_font, (255, 255, 255), main_screen,
                              screen_width // 2 + 240, screen_height // 2 + 160)
        else:
            draw_text_outline("Bets Won", medium_font, (255, 255, 255), main_screen, screen_width // 2 + 230,
                              screen_height // 2 + 160)

        # basic UI elements
        item_UI()
        money_UI()

        click = False  # resets the click event, prevents one click -> two actions

        # Checks for game events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True

        pygame.display.update()
        clock.tick(60)


def tutorial_select(message):
    """the screen to select the unit to learn more about

    :param message: string for the message at the top of the screen
    """

    """---------------------------------SETUP-------------------------------"""
    click = False  # resets the mouse click to avoid a bug where one click would trigger two events

    pygame.mouse.set_visible(True)  # deals with the visibility of the mouse. allows  user to see and move their mouse

    # Rects for the tutorial buttons
    add_button = pygame.Rect((screen_width // 2) - 455, (screen_height // 2) - 80, 370, 80)
    multiply_button = pygame.Rect((screen_width // 2) + 85, (screen_height // 2) - 80, 370, 80)
    lcd_button = pygame.Rect((screen_width // 2) - 185, (screen_height // 2) + 40, 370, 80)
    transform_button = pygame.Rect((screen_width // 2) - 455, (screen_height // 2) + 160, 370, 80)
    y_button = pygame.Rect((screen_width // 2) + 85, (screen_height // 2) + 160, 370, 80)
    home_button = pygame.Rect(30, 20, 120, 60)
    quit_button = pygame.Rect(1130, 20, 120, 60)

    """"----------------------------------LOOP-------------------------------"""
    while True:  # screen loop
        main_screen.blit(start_background, (0, 0))  # creates the background image

        mx, my = pygame.mouse.get_pos()  # deals with the mouse positions

        universal_UI(home_button, quit_button, mx, my, click)

        if add_button.collidepoint((mx, my)):
            pygame.draw.rect(main_screen, (240, 20, 20), add_button, 0, 5)
            if click:
                button_sound.play()
                special_tutorials(['Add', 'Subtract'])
        else:
            pygame.draw.rect(main_screen, (196, 16, 16), add_button, 0, 5)

        if multiply_button.collidepoint((mx, my)):
            pygame.draw.rect(main_screen, (240, 20, 20), multiply_button, 0, 5)
            if click:
                button_sound.play()
                special_tutorials(['Multiply', 'Divide'])

        else:
            pygame.draw.rect(main_screen, (196, 16, 16), multiply_button, 0, 5)

        if lcd_button.collidepoint((mx, my)):
            pygame.draw.rect(main_screen, (240, 20, 20), lcd_button, 0, 5)
            if click:
                button_sound.play()
                tutorials('Find LCD')
        else:
            pygame.draw.rect(main_screen, (196, 16, 16), lcd_button, 0, 5)

        if y_button.collidepoint((mx, my)):
            pygame.draw.rect(main_screen, (240, 20, 20), y_button, 0, 5)
            if click:
                button_sound.play()
                tutorials('Transform Fraction')
        else:
            pygame.draw.rect(main_screen, (196, 16, 16), y_button, 0, 5)

        if transform_button.collidepoint((mx, my)):
            pygame.draw.rect(main_screen, (240, 20, 20), transform_button, 0, 5)
            if click:
                button_sound.play()
                tutorials('Find Y-intercept Form')

        else:
            pygame.draw.rect(main_screen, (196, 16, 16), transform_button, 0, 5)

        # Draws text on the tutorial menu screen
        draw_text_outline(message, big_font, (255, 255, 255), main_screen, screen_width // 2, screen_height // 2 - 170)
        draw_text_outline("Add/Subtract", small_font, (255, 255, 255), main_screen, (screen_width // 2) - 270,
                          screen_height // 2 - 40)
        draw_text_outline("Multiply/Divide", small_font, (255, 255, 255), main_screen, (screen_width // 2) + 270,
                          screen_height // 2 - 40)
        draw_text_outline("LCD", small_font, (255, 255, 255), main_screen, screen_width // 2, screen_height // 2 + 80)
        draw_text_outline("Transform Fraction", small_font, (255, 255, 255), main_screen, (screen_width // 2) + 270,
                          screen_height // 2 + 200)
        draw_text_outline("Y-Intercept Form", small_font, (255, 255, 255), main_screen, (screen_width // 2) - 270,
                          screen_height // 2 + 200)

        money_UI()

        click = False  # resets the mouse click

        # checks for game events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True

        # updates the game and tick
        pygame.display.update()
        clock.tick(60)


def special_tutorials(tut_types):
    """the screen for the player to select a special type of tutorial

    :param tut_types: either add/subtract or multiplication/division
    """

    """---------------------------------SETUP-------------------------------"""

    # for addition/subtraction tutorial or multiplication/division tutorial
    click = False  # resets the mouse click to avoid a bug where one click would trigger two events

    pygame.mouse.set_visible(True)  # deals with the visibility of the mouse. allows  user to see and move their mouse
    tutorial1 = tut_types[0]
    tutorial2 = tut_types[1]

    option1_button = pygame.Rect((screen_width // 4) - 185, screen_height/2, 370, 100)
    option2_button = pygame.Rect((3*(screen_width // 4)) - 185, screen_height/2, 370, 100)

    back_button = pygame.Rect(30, 20, 120, 60)
    quit_button = pygame.Rect(1130, 20, 120, 60)

    """"----------------------------------LOOP-------------------------------"""

    while True:
        main_screen.blit(start_background, (0, 0))  # creates the background image

        mx, my = pygame.mouse.get_pos()  # deals with the mouse positions

        """NAVIGATIONAL UI BUTTONS"""

        if back_button.collidepoint((mx, my)):
            pygame.draw.rect(main_screen, (64, 128, 230), back_button, 0, 5)
            if click:
                button_sound.play()
                tutorial_select("Select Tutorial")
        else:
            pygame.draw.rect(main_screen, (46, 102, 191), back_button, 0, 5)

        if quit_button.collidepoint((mx, my)):
            pygame.draw.rect(main_screen, (64, 128, 230), quit_button, 0, 5)
            if click:
                button_sound.play()
                sys.exit()
        else:
            pygame.draw.rect(main_screen, (46, 102, 191), quit_button, 0, 5)

        """TUTORIAL BUTTONS"""

        if option1_button.collidepoint((mx, my)):
            pygame.draw.rect(main_screen, (240, 20, 20), option1_button, 0, 5)
            if click:
                button_sound.play()
                tutorials(tutorial1)
        else:
            pygame.draw.rect(main_screen, (196, 16, 16), option1_button, 0, 5)

        if option2_button.collidepoint((mx, my)):
            pygame.draw.rect(main_screen, (240, 20, 20), option2_button, 0, 5)
            if click:
                button_sound.play()
                tutorials(tutorial2)
        else:
            pygame.draw.rect(main_screen, (196, 16, 16), option2_button, 0, 5)

        draw_text_outline(tutorial2, medium_font, (255, 255, 255), main_screen, 3 * screen_width // 4,
                          screen_height/2 + 50)
        draw_text_outline(tutorial1, medium_font, (255, 255, 255), main_screen, screen_width // 4, screen_height/2 + 50)

        draw_text_outline("Back", small_font, (255, 255, 255), main_screen, 90, 50)
        draw_text_outline("Quit", small_font, (255, 255, 255), main_screen, 1190, 50)

        money_UI()

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True

        # updates the game and tick
        pygame.display.update()
        clock.tick(60)


def tutorials(tutorial):
    """the screen for the different tutorials

    :param tutorial: the tutorial mode the player is on
    """

    """---------------------------------SETUP-------------------------------"""

    steps = tutorial_steps(tutorial)
    equation = steps[0]
    click = False  # resets the mouse click to avoid a bug where one click would trigger two events

    pygame.mouse.set_visible(True)  # deals with the visibility of the mouse. allows  user to see and move their mouse
    next_button = pygame.Rect((screen_width // 2) - 100, 600, 200, 100)

    back_button = pygame.Rect(30, 20, 120, 60)
    quit_button = pygame.Rect(1130, 20, 120, 60)

    clicks = 0

    finished = False

    """"----------------------------------LOOP-------------------------------"""

    while True:
        main_screen.blit(start_background, (0, 0))  # creates the background image

        mx, my = pygame.mouse.get_pos()  # deals with the mouse positions

        """NAVIGATIONAL UI BUTTONS"""

        if back_button.collidepoint((mx, my)):
            pygame.draw.rect(main_screen, (64, 128, 230), back_button, 0, 5)
            if click:
                button_sound.play()
                tutorial_select("Select Tutorial")
        else:
            pygame.draw.rect(main_screen, (46, 102, 191), back_button, 0, 5)

        if quit_button.collidepoint((mx, my)):
            pygame.draw.rect(main_screen, (64, 128, 230), quit_button, 0, 5)
            if click:
                button_sound.play()
                sys.exit()
        else:
            pygame.draw.rect(main_screen, (46, 102, 191), quit_button, 0, 5)

        """TUTORIAL BUTTONS"""

        if next_button.collidepoint((mx, my)):
            pygame.draw.rect(main_screen, (240, 20, 20), next_button, 0, 5)
            if click:
                button_sound.play()
                clicks += 1

        else:
            pygame.draw.rect(main_screen, (196, 16, 16), next_button, 0, 5)

        if (clicks >= 1) and (clicks < len(steps)):
            for index in range(1, clicks+1):
                height = (index - 1) * 50
                draw_text_outline(steps[index], medium_font, (255, 255, 255), main_screen, screen_width // 2,
                                  height + 170)

        if clicks == len(steps):
            clicks = 0

        draw_text_outline(tutorial, big_font, (255, 255, 255), main_screen, screen_width // 2, 50)

        # edge case for the special fraction format
        if tutorial == 'Transform Fraction':
            draw_text_outline('3', medium_font, (255, 255, 255), main_screen, screen_width // 2 - 10, 130)
            draw_text_outline('2', medium_font, (255, 255, 255), main_screen, screen_width // 2 + 15, 100)
            draw_text_outline('/', medium_font, (255, 255, 255), main_screen, screen_width // 2 + 20, 120)
            draw_text_outline('3', medium_font, (255, 255, 255), main_screen, screen_width // 2 + 35, 140)

        else:
            draw_text_outline(equation, medium_font, (255, 255, 255), main_screen, screen_width // 2, 100)

        if clicks == 0:
            draw_text_outline('Start', medium_font, (255, 255, 255), main_screen, screen_width//2, 650)
        elif clicks == len(steps) - 1:
            draw_text_outline('Again', medium_font, (255, 255, 255), main_screen, screen_width // 2, 650)
            if tutorial not in player.tutorials_completed:  # adds the tutorial to the completed list
                player.tutorials_completed.append(tutorial)
                player.total_money += 25  # can only earn the $25 once, prevents exploits
            finished = True
        else:
            draw_text_outline('Next', medium_font, (255, 255, 255), main_screen, screen_width // 2, 650)

        if finished:
            draw_text_outline("+$25", big_font, (255, 255, 255), main_screen, screen_width // 2, 500)

        draw_text_outline("Back", small_font, (255, 255, 255), main_screen, 90, 50)
        draw_text_outline("Quit", small_font, (255, 255, 255), main_screen, 1190, 50)

        click = False  # resets the mouse click

        money_UI()

        # Checks for game events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True

        # updates the game and tick
        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    player = Player()
    menu(mouse_click, "Fraction Distraction")
