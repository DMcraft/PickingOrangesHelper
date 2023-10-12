import random
import arcade
from loguru import logger as log

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
# Константы цветов
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 133, 10)


class TestView(arcade.Window):
    def __init__(self, width, height, title):
        """ Initializer """
        # Calls "__init__" of parent class (arcade.Window) to setup screen
        super().__init__(width, height, title, resizable=True)

        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT

        self.x = 0
        self.y = 0
        self.freq_sq_update = 0

    def on_draw(self):
        """ Draw everything for the game. """
        self.clear()
        arcade.draw_rectangle_filled(self.x, self.y, 15, 15, ORANGE)
        arcade.draw_text(f'({self.x} : {self.y})', self.x - 25, self.y + 10, arcade.color.ROSE, 10)

        arcade.draw_text(f'Draw x:{self.x}, y:{self.y}', 15, 15, arcade.color.GREEN)

    def on_key_press(self, key, _modifiers):
        """ Handle key presses. In this case, we'll just count a 'space' as
        game over and advance to the game over view. """
        if key == arcade.key.ESCAPE:
            arcade.close_window()
        arcade.close_window()

    def on_update(self, delta_time):
        """ Movement and game logic """
        self.freq_sq_update += delta_time
        if self.freq_sq_update > 3:
            self.x, self.y = random.randint(1, self.screen_width), random.randint(1, self.screen_height)
            self.freq_sq_update = 0

    def on_resize(self, width, height):
        """
        Resize window
        Handle the user grabbing the edge and resizing the window.
        """
        super().on_resize(width, height)
        #log.info(f'resize window w:{width}, h:{height}')
        self.screen_width = width
        self.screen_height = height


def main():
    window = TestView(SCREEN_WIDTH, SCREEN_HEIGHT, 'SCREEN_TITLE')
    arcade.run()


if __name__ == "__main__":
    main()

