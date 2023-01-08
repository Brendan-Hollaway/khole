import pygame as pg
from pygame.locals import *  # Keys to press
import random

from log import get_logger
from common import read_img
from constants import *
from text_writer import *
from ketamine_injector import KetamineInjector


class InjectorParams:
    """
    Could this whole class just be a dict? Oh absolutely. Will I make it a dict?
    Nah, I kinda feel like being a dict about it tbh
    """

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        if not "text_color" in self.kwargs:
            self.kwargs["text_color"] = IMAGE_NAME_TEXT_COLOR


def get_injector_params():
    return [
        InjectorParams(key=K_q, name="1mg of K-Dust", img_name="dust_pile.png"),
        InjectorParams(
            key=K_w, name="The PinpricKer", img_name="pinpricker.jpg", text_color=WHITE
        ),
        InjectorParams(key=K_e, name="Pile o' Pill Kaps", img_name="pile_of_pills.jpg"),
        InjectorParams(key=K_r, name="IV: K in My Veins!", img_name="iv.jpg"),
        InjectorParams(
            key=K_t, name="Wheelbarrow of K-Dust", img_name="wheelbarrow.png"
        ),
        InjectorParams(key=K_y, name="Cement TrucK", img_name="cement_truck.jpg"),
        InjectorParams(
            key=K_u, name="NuKe", img_name="nuke_explosion.jpeg", text_color=WHITE
        ),
        InjectorParams(
            key=K_i, name="Planet K", img_name="planet_k.jpg", text_color=WHITE
        ),
        InjectorParams(
            key=K_o, name="GalaKsy", img_name="galaxy.jpg", text_color=WHITE
        ),
        InjectorParams(
            key=K_p, name="BlacK Hole", img_name="black_hole.jpg", text_color=WHITE
        ),
    ]


def get_rect(i: int):
    """
    #GetRekt boyo

    Returns the rectangle representing the bounds of the injector
    """
    rows = NUM_INJECTORS // 2
    rect = pg.rect.Rect(0, 0, 0, 0)  # size is irrelevant
    rect.top = ((i % rows) * (TOTAL_INJECTOR_HEIGHT / rows)) + STATUS_BAR_SIZE[1]
    if i <= 4:
        rect.left = 0
    else:
        rect.left = SCREEN_WIDTH / 2
    # get_logger().info(f"Rect {i}: {rect}. left: {rect.left}, right: {rect.right}")
    return rect


def get_injectors():
    """So many sharp objects to collect!"""
    base_cost = 10
    cost_exp = 15
    inject_exp = 8
    cost_mult = 1.5
    injectors = [
        KetamineInjectorVisualizer(
            init_cost=(base_cost * (cost_exp ** i) if (i + 1) > 0 else base_cost / cost_mult),
            init_inject=inject_exp ** i,
            cost_mult=cost_mult,
            rect=get_rect(i),
            **params.kwargs,
        )
        for i, params in enumerate(get_injector_params())
    ]
    # injectors = injectors[1:]
    return injectors


class KetamineInjectorVisualizer(KetamineInjector, pg.sprite.Sprite):
    """Because two classes is better than one!"""

    def __init__(self, rect: pg.rect.Rect, img_name: str, text_color: tuple, **kwargs):
        pg.sprite.Sprite.__init__(self)
        KetamineInjector.__init__(self, **kwargs)

        self.image_name = img_name
        self.text_color = text_color

        # Antialias text
        self.antialias = True

        self.button_rect = None  # set in add_button

        self.original_image = self.init_image()
        self.image = self.original_image.copy()

        # Fetch the rectangle object that has the dimensions of the image
        self.rect = self.image.get_rect()
        # Update the position of the image
        self.rect.topleft = rect.topleft
        # Update the button_rect to be an absolute, rather than relative, rect
        self.button_rect.move_ip(self.rect.topleft)

        self.draw_upgrade_button()

    def random_color(self):
        return tuple(random.randint(0, 255) for _ in range(3))

    def add_button(self, image):
        """must... resist... urge... to... click..."""
        button = read_img("shiny_green_button_cropped.png")
        button = pg.transform.scale(button, UPGRADE_BUTTON_SIZE)
        self.button_rect = rect_for_alignment(button, image, Align.BOT_CENTER)
        image.blit(button, self.button_rect)

    def init_image(self):
        """Make me pretty! Pretty sharp, that is"""
        image = pg.Surface(INJECTOR_SIZE)
        image.fill(WHITE)
        if self.image_name != "":
            picture = read_img(self.image_name)
            picture = pg.transform.scale(picture, IMAGE_SIZE)
            image.blit(picture, pg.rect.Rect((0, 0), IMAGE_SIZE))

        write_text(self.name, image, Align.TOP_CENTER, self.text_color)
        self.add_button(image)

        return image

    def upgrade_injector(self):
        """Lemme just sliiiiiiide into this function with some UI real quick"""
        KetamineInjector.upgrade_injector(self)
        self.update_upgrade_button()

    def update_upgrade_button(self):
        """Costs always going up? Damn inflation..."""
        self.image = self.original_image.copy()
        temp_rect = self.rect.copy()
        self.rect = self.image.get_rect()
        self.rect.topleft = temp_rect.topleft
        self.draw_upgrade_button()

    def draw_upgrade_button(self):
        # TODO(bhollaway): Better joke here
        """Hey Micah, you're an artist, think you can do better, huh?"""
        upgrade_or_buy = "Upgrade" if self.upgrade_count > 0 else "Buy"
        text = f"{upgrade_or_buy}: {self.get_cost():.0f}"
        write_text(text, self.image, Align.BOT_CENTER, UPGRADE_BUTTON_TEXT_COLOR)

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

        if self.button_rect.collidepoint(event.pos):
            return self.try_upgrade(curr_ketamine)

        return curr_ketamine + self.inject_ketamine()
