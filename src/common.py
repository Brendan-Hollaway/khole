import pygame as pg


def read_img(img_name: str):
    return pg.image.load(f"../assets/{img_name}")
