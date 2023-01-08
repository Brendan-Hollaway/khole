import pygame
from pygame.locals import * # Keys to press
import random


def get_keys():
    """Press me, press me!"""

    return [K_q]
    # return [K_q, K_w, K_e, K_r, K_t, K_y, K_y, K_u, K_i, K_o, K_p]


def get_injectors():
    """So many sharp objects to collect!"""
    base_cost = 10
    cost_mult = 1.5
    inject_mult = 1.3
    return [
        KetamineInjectorVisualizer(
            init_cost=(base_cost**(i+1) if (i+1) > 0 else 10 / cost_mult),
            init_inject=(base_cost ** ((i+1) - 1) if (i+1) > 0 else 1 / inject_mult),
            cost_mult=cost_mult,
            inject_mult=inject_mult,
            keyboard_key=key,
        )
        for i, key in enumerate(get_keys())
    ]


class KetamineInjector(object):
    """The fastest way to a khole or your money back!"""

    def __init__(
        self,
        init_cost: float,
        init_inject: float,
        cost_mult: float,
        inject_mult: float,
        keyboard_key: int,
    ):
        """Init functions, where a little copy-paste goes a long way"""
        self.cost = init_cost
        self.init_inject = init_inject
        self.cost_mult = cost_mult
        self.inject_mult = inject_mult
        self.key = keyboard_key

        # Start at 0, upgrade to init_inject once it's ready for injecting
        self.inject = 0

    def cost(self):
        """What would you give for just a bit more ketamine?"""
        return self.cost

    def inject_ketamine(self):
        """Returns the amount of that sweet sweet ketamine to inject right into those veins"""
        return self.inject

    def upgrade_injector(self):
        """Bigger. Deeper. Ketaminer."""
        self.cost *= self.cost_mult
        if self.inject == 0:
            self.inject = self.init_inject
        else:
            self.inject *= self.inject_mult

    def handle_key_down(self, event: pygame.event.Event) -> float:
        """
        Is it my turn?

        Handles upgrading the injector, if the key requires upgrading.
        If the key is for injecting, return the amount to inject.
        """
        # TODO(bhollaway): handle upgrades
        if event.key == self.key:
            return self.inject_ketamine()
        return 0


class KetamineInjectorVisualizer(KetamineInjector, pygame.sprite.Sprite):
    """Because two classes is better than one!"""

    # How big can you take?
    INJECTOR_SIZE = [50, 50]

    def __init__(self, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        KetamineInjector.__init__(self, **kwargs)

        self.image = self.init_image()
        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()

    def random_color(self):
        return tuple(random.randint(0, 255) for _ in range(3))

    def init_image(self):
        """Make me pretty! Pretty sharp, that is"""
        image = pygame.Surface(self.INJECTOR_SIZE)
        image.fill(self.random_color())
        return image
