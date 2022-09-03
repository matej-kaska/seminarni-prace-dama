from pygame import draw, font

class Button:
    def __init__(self, color, highlight_color, x, y, width, height, text=""):
        self._color = color
        self._default_color = color
        self._highlight_color = highlight_color
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._text = text

    @property
    def color(self):
        return self._color
    
    @color.setter
    def color(self, val):
        self._color = val

    @property
    def default_color(self):
        return self._default_color

    @default_color.setter
    def default_color(self, val):
        self._default_color = val

    @property
    def highlight_color(self):
        return self._highlight_color

    @highlight_color.setter
    def highlight_color(self, val):
        self._highlight_color = val

    @property
    def text(self):
        return self._text

    def draw(self, win, outline=None):
        if outline:
            draw.rect(win, outline, (self._x - 2, self._y - 2, self._width + 4, self._height + 4), 0)
            
        draw.rect(win, self._color, (self._x, self._y, self._width, self._height), 0)
        
        if self._text != "":
            font_type = font.SysFont("inkfree", 16)
            text = font_type.render(self._text, 1, (0, 0, 0))
            win.blit(text, (self._x + (self._width / 2 - text.get_width() / 2), self._y + (self._height / 2 - text.get_height() / 2)))

    def is_over(self, pos):
        if pos[0] > self._x and pos[0] < self._x + self._width:
            if pos[1] > self._y and pos[1] < self._y + self._height:
                return True
            
        return False