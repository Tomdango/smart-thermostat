"""
Entrypoint
"""
from abc import ABC, abstractmethod
from typing import List

from displayhatmini import DisplayHATMini
from PIL import Image, ImageDraw, ImageFont


class State:
    _brightness: float = 1.0
    _power_saving_mode_enabled: bool = False

    @property
    def brightness(self):
        return 0.2 if self._power_saving_mode_enabled else self._brightness


class WindowObject(ABC):
    MIN_HEIGHT = 0
    MAX_HEIGHT = DisplayHATMini.HEIGHT
    MIN_WIDTH = 0
    MAX_WIDTH = DisplayHATMini.WIDTH

    def __init__(self, image: Image):
        """"""
        self.image = image
        self.draw = ImageDraw.Draw(self.image)

    def init(self) -> bool:
        return True

    def shouldRender(self) -> bool:
        """"""
        return True

    @abstractmethod
    def render(self):
        raise NotImplementedError()


class Window(WindowObject):
    _children: List[WindowObject] = []

    def init(self):
        self._render_background()

    def render(self):
        for child in self._children:
            child.render()

    def _render_background(self):
        """Render the basic background"""
        # Render
        self.draw.rectangle(
            (self.MIN_WIDTH, self.MIN_HEIGHT, self.MAX_WIDTH, self.MAX_HEIGHT),
            (180, 0, 0),
            width=10,
        )
        self.draw.rectangle(
            (
                self.MIN_WIDTH + 10,
                self.MIN_HEIGHT + 10,
                self.MAX_WIDTH - 10,
                self.MAX_HEIGHT - 10,
            ),
            (50, 50, 50),
        )


class Renderer:
    def __init__(self):
        self.image = Image.new("RGB", (DisplayHATMini.WIDTH, DisplayHATMini.HEIGHT))
        self.window = Window(self.image)

    def init(self):
        """"""
        self.window.init()

    def render(self):
        try:
            return self.window.render()
        except Exception:
            print("Failed to draw window")
            return False


if __name__ == "__main__":
    state = State()

    image = Image.new("RGB", (DisplayHATMini.WIDTH, DisplayHATMini.HEIGHT))
    renderer = Renderer()
    renderer.init()
    renderer.render()
