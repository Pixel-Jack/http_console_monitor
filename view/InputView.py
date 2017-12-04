import curses
from curses.textpad import Textbox, rectangle


class InputView:
    def __init__(self, window, text='', begin_prompt=''):
        self.window = window
        self.text = str(text)
        self.begin_prompt = begin_prompt
        self.window.clear()
        self.refresh()

    def set_text(self, text):
        self.text = str(text)

    def refresh(self):
        height, width = self.window.getmaxyx()
        if height > 0 and width - len(self.begin_prompt) - 1 > 0:
            self.window.addstr(0, 0, self.begin_prompt, curses.color_pair(1))
            self.window.addstr(0, len(self.begin_prompt), self.text[:width - len(self.begin_prompt) - 1])
            # Refresh the screen
            self.window.refresh()
