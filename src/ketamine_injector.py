import pygame as pg
import math

from log import get_logger
from constants import *


class KetamineInjector(object):
    """The fastest way to a khole or your money back!"""

    def __init__(
        self,
        init_cost: float,
        init_inject: float,
        cost_mult: float,
        key: int,
        name: str,
        max_upgrade_count: int = 10,
    ):
        """Init functions, where a little copy-paste goes a long way"""
        self.cost = init_cost
        self.init_inject = init_inject
        self.cost_mult = cost_mult
        self.key = key  # key on the keyboard
        self.name = name

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
        self.inject += self.init_inject
        self.upgrade_count += 1

    def can_upgrade(self, curr_ketamine: float):
        """I dunno yungin'... Are you ready for this level of power?"""
        if self.upgrade_count >= self.max_upgrade_count:
            self.log.warning(
                f"Cannot upgrade: Already at max upgrade count of {self.max_upgrade_count}"
            )
            return False
        if curr_ketamine < self.get_cost():
            self.log.warning(
                f"Cannot upgrade: Insufficient ketamine! Need {self.get_cost()}; only have {curr_ketamine}"
            )
            return False
        return True

    def try_upgrade(self, curr_ketamine: float):
        """
        You think you can handle an upgrade, huh?
        You think you're cool enough for the big leagues now??

        Returns new ketamine, post (lack of) upgrade.
        """
        if self.can_upgrade(curr_ketamine):
            cost = self.cost
            self.upgrade_injector()
            return curr_ketamine - cost
        # TODO(bhollaway): Better errors than just the text printouts?...
        return curr_ketamine

    def handle_key_down(self, event: pg.event.Event, curr_ketamine: float) -> float:
        """
        Is it my turn?

        Handles upgrading the injector, if the key requires upgrading.
        If the key is for injecting, return the amount to inject.
        """
        if event.key != self.key:
            return curr_ketamine

        self.log.debug(f"Mod: {event.mod}")
        if event.mod & pg.KMOD_SHIFT: # Press shift to upgrade!
            return self.try_upgrade(curr_ketamine)

        # Inject!
        return curr_ketamine + self.inject_ketamine()
