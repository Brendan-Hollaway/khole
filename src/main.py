import pygame as pg

pg.init()  # I hate pygame sometimes

from typing import Optional

# from ketamine_injector import KetamineInjector, get_injectors()
from ketamine_injector_visualizer import get_injectors
from constants import *
from text_writer import *
from log import get_logger
from ketamine_status import KetamineStatus

# Type aliases for type hints
Event = pg.event.Event


class Runner:
    """
    Wanna go for a run? Too bad, you're strapped down to the gurney
    and you'll be wayyyyyyy too loopy once we're done
    """

    # Who uses booleans when you could cooler booleans?
    TIME_TO_QUIT = False
    KEEP_PLAYING = True

    def __init__(self):
        """
        Started at the bottom, now I'm lying on my bottom, about to
        be injected with enough ketamine to see into the void.
        """
        self.log = get_logger()

        self.running_on_ketamine = True
        self.curr_ketamine = 50 * 12**9

        self.injectors = get_injectors()
        self.injectors[0].upgrade_injector()  # first injector is free!

        self.screen = pg.display.set_mode(SCREEN_SIZE)
        self.injecting_time_type = self.init_injecting_time()
        pg.event.set_blocked(pg.MOUSEMOTION)

        self.clear()
        self.all_sprites = self.init_all_sprites()
        self.status = KetamineStatus()

    def init_all_sprites(self):
        all_sprites = pg.sprite.Group()
        for injector in self.injectors:
            all_sprites.add(injector)

        all_sprites.update()
        all_sprites.draw(self.screen)
        self.log.debug("Done initting sprites")
        return all_sprites

    def save_progress(self):
        """Even quitters get a second chance..."""
        # TODO(bhollaway): Pickle the runner? Or just the curr_ketamine and injectors?
        pass

    def load_progress(self):
        """Welcome back to the K-hole"""
        # TODO(bhollaway)
        pass

    def handle_event(self, event: Event) -> bool:
        """
        I told you to handle it! C'mon, just like, handle it

        # Return TIME_TO_QUIT if it's time to quit :'(
        """
        self.log.debug(f"event: {event}")
        # Wow, giving up already?
        if event.type == pg.QUIT:
            self.running_on_ketamine = False
            # return self.TIME_TO_QUIT

        # Mash those keys
        elif event.type == pg.KEYDOWN:
            # Can't escape from the K-hole... Except via K_ESCAPE
            if event.key == pg.locals.K_ESCAPE:
                self.running_on_ketamine = False
                # return self.TIME_TO_QUIT

            old_ket = self.curr_ketamine
            for injector in self.injectors:
                self.curr_ketamine = injector.handle_key_down(event, self.curr_ketamine)
            if self.curr_ketamine != old_ket:
                self.log.info(
                    f"Ketamine post manual injection: {self.curr_ketamine:.2f}"
                )

        elif event.type == self.injecting_time_type:
            self.curr_ketamine += self.injecting_time()
            self.log.info(f"Ketamine post injection: {self.curr_ketamine:.2f}")

        elif event.type == pg.MOUSEBUTTONDOWN:
            for injector in self.injectors:
                self.curr_ketamine = injector.handle_mouse_down(
                    event, self.curr_ketamine
                )

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

    def clear(self):
        """Let me be clear with you: This just wipes the slate clean."""
        # Fill the screen with white
        self.screen.fill((255, 255, 255))

    def update_ketamine_counter(self):
        """C'mon man, how big is the next hit gonna be?"""
        counter_text = f"Ketamine: {self.curr_ketamine:.0f} Grams"
        counter_text_surface = write_text(
            counter_text,
            self.screen,
            Align.TOP_CENTER,
            KETAMINE_COUNTER_COLOR,
            font=KETAMINE_FONT,
        )

        status = self.status.get_status(self.curr_ketamine)
        font = (
            KETAMINE_STATUS_FONT
            if status != "ACHIEVED K-HOLE"
            else KETAMINE_VICTORY_FONT
        )
        status_text = f"Status: {status}"
        vert_offset = counter_text_surface.get_size()[1] # Put it below the counter
        write_text(
            status_text,
            self.screen,
            Align.TOP_CENTER,
            KETAMINE_COUNTER_COLOR,
            font=font,
            offset=(0, vert_offset),
        )

    def main_loop(self):
        """
        This shit's crazy. Just straight up loopy!

        Ba-dum-tss
        """
        clock = pg.time.Clock()
        while self.running_on_ketamine:
            clock.tick(FPS)

            event = pg.event.wait()
            self.handle_event(event)

            # Draw shit
            self.clear()
            self.all_sprites.update()
            self.all_sprites.draw(self.screen)
            self.update_ketamine_counter()

            pg.display.flip()

        self.log.warning("Exiting now!")
        self.save_progress()


def main():
    runner = Runner()
    runner.main_loop()
    pg.quit()


if __name__ == "__main__":  # If it's not, honestly, what are you even doing
    main()
