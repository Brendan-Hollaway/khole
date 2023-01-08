import pygame as pg
from typing import Optional
import log

# from ketamine_injector import KetamineInjector, get_injectors()
from ketamine_injector import get_injectors

# Type aliases for type hints
Event = pg.event.Event


class Runner:
    """
    Wanna go for a run? Too bad, you're strapped down to the gurney
    and you'll be wayyyyyyy too loopy once we're done
    """

    # Want to change this? Unleash the horrors within...
    SCREEN_SIZE = [800, 800]

    # Who uses booleans when you could cooler booleans?
    TIME_TO_QUIT = False
    KEEP_PLAYING = True

    def __init__(self):
        """
        Started at the bottom, now I'm lying on my bottom, about to
        be injected with enough ketamine to see into the void.
        """
        self.log = log.get_logger()

        self.running_on_ketamine = True
        self.curr_ketamine = 0

        self.injectors = get_injectors()
        self.injectors[0].upgrade_injector()  # first injector is free!

        self.screen = pg.display.set_mode(self.SCREEN_SIZE)
        self.injecting_time_type = self.init_injecting_time()
        pg.event.set_blocked(pg.MOUSEMOTION)

    def save_progress(self):
        """Even quitters get a second chance..."""
        # TODO(bhollaway)
        pass

    def handle_event(self, event: Event) -> bool:
        """
        I told you to handle it! C'mon, just like, handle it

        Return TIME_TO_QUIT if it's time to quit :'(
        """
        self.log.debug(f"event: {event}")
        # Wow, giving up already?
        if event.type == pg.QUIT:
            self.running_on_ketamine = False
            return self.TIME_TO_QUIT

        # Mash those keys
        elif event.type == pg.KEYDOWN:
            if event.key == pg.locals.K_ESCAPE:
                self.running_on_ketamine = False
                return self.TIME_TO_QUIT

            for injector in self.injectors:
                self.curr_ketamine = injector.handle_key_down(event, self.curr_ketamine)

        elif event.type == self.injecting_time_type:
            self.curr_ketamine += self.injecting_time()
            self.log.info(f"Ketamine post injection: {self.curr_ketamine:.2f}")

        return self.KEEP_PLAYING

    def injecting_time(self) -> float:
        """
        It's time for us to all go to our special place now... It's injecting time!

        Return the amount of ketamine to inject
        """
        self.log.debug("It's injecting time!")
        moar_ketamine = 0
        for injector in self.injectors:
            moar_ketamine += injector.inject_ketamine()
        return moar_ketamine

    def init_injecting_time(self) -> int:
        """
        We're on the clock y'all: every second, it's injecting time!
        """
        injecting_time_type = pg.event.custom_type()
        injecting_time_ms = 1000
        pg.time.set_timer(injecting_time_type, injecting_time_ms)
        return injecting_time_type

    # def draw(self):
    #     """ TODO(bhollaway): move this to its own file """
    #     # Fill the screen with white
    #     screen.fill((255, 255, 255))

    def main_loop(self):
        """
        This shit's crazy. Just straight up loopy!

        Ba-dum-tss
        """
        while self.running_on_ketamine:
            event = pg.event.wait()
            update = self.handle_event(event)
            if update == self.TIME_TO_QUIT:
                break
            curr_ketamine = update

        self.log.warning("Exiting now!")
        self.save_progress()


def main():
    pg.init()
    runner = Runner()
    runner.main_loop()
    pg.quit()


if __name__ == "__main__":  # If it's not, honestly, what are you even doing
    main()
