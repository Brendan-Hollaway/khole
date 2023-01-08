import pygame as pg
from pygame.locals import *  # Keys to press
import random
import math

from log import get_logger
from constants import *


def get_injector_names():
    return ["Smol Needle"]


def get_keys():
    """Press me, press me!"""
    # return [K_q, K_w]
    return [K_q, K_w, K_e, K_r, K_t, K_y, K_y, K_u, K_i, K_o, K_p]


def get_rect(i: int):
    """
    #GetRekt boyo

    Returns the rectangle representing the bounds of the injector
    """
    rows = NUM_INJECTORS // 2
    rect = pg.rect.Rect(0, 0, 0, 0) # size is irrelevant
    rect.top = (i % rows) * (SCREEN_HEIGHT / rows)
    if i <= 4:
        rect.left = 0
    else:
        rect.left = 3 * SCREEN_WIDTH / 4
    # get_logger().info(f"Rect {i}: {rect}. left: {rect.left}, right: {rect.right}")
    return rect


def get_injectors():
    """So many sharp objects to collect!"""
    base_cost = 10
    cost_mult = 1.5
    inject_mult = 1.3
    injectors = [
        KetamineInjectorVisualizer(
            init_cost=(base_cost ** (i + 1) if (i + 1) > 0 else base_cost / cost_mult),
            init_inject=(
                base_cost ** ((i + 1) - 1) if (i + 1) > 0 else 1 / inject_mult
            ),
            cost_mult=cost_mult,
            inject_mult=inject_mult,
            keyboard_key=key,
            rect=get_rect(i)
        )
        for i, key in enumerate(get_keys())
    ]
    # injectors = injectors[1:]
    return injectors


class KetamineInjector(object):
    """The fastest way to a khole or your money back!"""

    def __init__(
        self,
        init_cost: float,
        init_inject: float,
        cost_mult: float,
        inject_mult: float,
        keyboard_key: int,
        max_upgrade_count: int = 10,
    ):
        """Init functions, where a little copy-paste goes a long way"""
        self.cost = init_cost
        self.init_inject = init_inject
        self.cost_mult = cost_mult
        self.inject_mult = inject_mult
        self.key = keyboard_key

        # Start at 0, upgrade to init_inject once it's ready for injecting
        self.inject = 0

        self.upgrade_count = 0
        self.max_upgrade_count = max_upgrade_count

        self.log = get_logger()

    def get_cost(self):
        """What would you give for just a bit more ketamine?"""
        return math.ceil(self.cost)

    def inject_ketamine(self):
        """Returns the amount of that sweet sweet ketamine to inject right into those veins"""
        self.log.info(f"Inject is: {self.inject}")
        return self.inject

    def upgrade_injector(self):
        """Bigger. Deeper. Ketaminer."""
        self.cost *= self.cost_mult
        if self.inject == 0:
            self.inject = self.init_inject
        else:
            self.inject *= self.inject_mult
        self.upgrade_count += 1

    def can_upgrade(self, curr_ketamine: float):
        if self.upgrade_count >= self.max_upgrade_count:
            self.log.warning(f"Cannot upgrade: Already at max upgrade count of {self.max_upgrade_count}")
            return False
        if curr_ketamine < self.get_cost():
            self.log.warning(
                f"Cannot upgrade: Insufficient ketamine! Need {self.get_cost()}; only have {curr_ketamine}"
            )
            return False
        return True

    def handle_key_down(self, event: pg.event.Event, curr_ketamine: float) -> float:
        """
        Is it my turn?

        Handles upgrading the injector, if the key requires upgrading.
        If the key is for injecting, return the amount to inject.
        """
        # TODO(bhollaway): handle upgrades
        if event.key != self.key:
            return curr_ketamine

        self.log.debug(f"Mod: {event.mod}")
        if event.mod & pg.KMOD_SHIFT:
            if self.can_upgrade(curr_ketamine):
                cost = self.cost
                self.upgrade_injector()
                return curr_ketamine - cost
            else:
                # TODO(bhollaway): Better errors than just the text printouts?...
                return curr_ketamine

        # Just pressing the key, e.g. without a modifier like control
        # Oh god have we lost control? I'm going crazzzzzzy on ketamine!
        else:
            return curr_ketamine + self.inject_ketamine()

        self.log.error("Unknown key modifier combo! Assuming you want to inject...")
        return curr_ketamine + self.inject_ketamine()

def print_rect(rect):
    print(f"{rect.topleft}, {rect.bottomright}")

class KetamineInjectorVisualizer(KetamineInjector, pg.sprite.Sprite):
    """Because two classes is better than one!"""

    def __init__(self, rect: Rect,  **kwargs):
        pg.sprite.Sprite.__init__(self)
        KetamineInjector.__init__(self, **kwargs)

        self.image = self.init_image()
        # Fetch the rectangle object that has the dimensions of the image
        self.rect = self.image.get_rect()
        # Update the position of the image
        self.rect.topleft = rect.topleft

        self.draw_upgrade_button()
        # self.screen = screen


    def random_color(self):
        return tuple(random.randint(0, 255) for _ in range(3))

    def init_image(self):
        """Make me pretty! Pretty sharp, that is"""
        image = pg.Surface(INJECTOR_SIZE)
        color = self.random_color()
        image.fill(color)
        return image

    def upgrade_injector(self):
        """Lemme just sliiiiiiide into this function with some UI real quick"""
        KetamineInjector.upgrade_injector(self)
        self.update_upgrade_button()

    def update_upgrade_button(self):
        """Costs always going up? Damn inflation..."""
        self.image = self.init_image() # TODO(bhollaway): Do we want to update the rect?
        temp_rect = self.rect.copy()
        self.rect = self.image.get_rect()
        self.rect.topleft = temp_rect.topleft
        self.draw_upgrade_button()

    def get_upgrade_button_rect(self, upgrade_button: pg.Surface):
        """The rect to eRect the UPgrade button in"""
        # We need to get the rect of the base image as if it were at (0, 0)
        image_unoffset_rect = pg.rect.Rect((0, 0), self.image.get_size())
        # We then make a rect of the size of the upgrade button
        rect = pg.rect.Rect((0,0), upgrade_button.get_size())
        # And align it to the bottom of the image
        rect.midbottom = image_unoffset_rect.midbottom
        return rect


    def draw_upgrade_button(self):
        """Hey Micah, you're an artist, think you can do better, huh?"""
        antialias = True
        upgrade_or_buy = "Upgrade" if self.upgrade_count > 0 else "Buy"
        text = f"{upgrade_or_buy}: {self.get_cost():.0f}"
        # TODO(bhollaway): Make a surface that looks like a button, then draw text on it
        self.font = pg.font.Font("../assets/fonts/joystix_mono.ttf", 15)
        upgrade_button = self.font.render(text, antialias, UPGRADE_BUTTON_TEXT_COLOR)
        self.image.blit(upgrade_button, self.get_upgrade_button_rect(upgrade_button))



    def handle_mouse_down(self, event: pg.event.Event, curr_ketamine: float) -> float:
        """
        You can't just put a mouse down like that, Lenny; it's not humane

        Check whether this sprite was clicked. If so, add some ketamine!
        If we clicked this sprite and specifically the "upgrade" button, then
        upgrade!

        Return the new amount of ketamine post processing
        """
        if not self.rect.collidepoint(event.pos):  # Not today, Lenny
            self.log.info(f"event pos: {event.pos}, rect: {self.rect}")
            return curr_ketamine

        # TODO(bhollaway): handle upgrades
        return curr_ketamine + self.inject_ketamine()
