from enum import Enum
import pygame as pg
from constants import *


class Align(Enum):
    """No, patrick, "a line" is not an alignment either"""

    TOP_CENTER = 1
    BOT_CENTER = 2


def write_text(
    text: str,
    image: pg.Surface,
    alignment: Align,
    color: tuple,
    font: pg.font.Font = DEFAULT_FONT,
    antialias=True,
):
    """
    I don't even have a joke here. I'm just... sad. So sad that something so braindead
    simple as "hey, can I write some text on this object?" requires multiple steps
    and a helper function to make it usable. Why is this not built in? Like honestly
    this is kinda ridiculous smh
    """
    text_img = font.render(text, antialias, color)
    rect = rect_for_alignment(text_img, image, alignment)
    image.blit(text_img, rect)


def rect_for_alignment(small_img: pg.Surface, big_img: pg.Surface, alignment: Align):
    """Chaotic evil or lawful good? Either way, you're gonna get #Rect"""
    # We need to get the rect of the base image as if it were at (0, 0)
    big_img_rect = pg.rect.Rect((0, 0), big_img.get_size())
    # We then make a rect of the size of the small image
    rect = pg.rect.Rect((0, 0), small_img.get_size())

    # And then align it!
    if alignment == Align.TOP_CENTER:
        rect.midtop = big_img_rect.midtop
    elif alignment == Align.BOT_CENTER:
        rect.midbottom = big_img_rect.midbottom

    return rect
