import curses


class InputView:
    def __init__(self, window, text='', begin_prompt=''):
        self.window = window
        self.text = str(text)
        self.begin_prompt = begin_prompt
        self.window.clear()
        self.update()

    def set_text(self, text):
        self.text = str(text)

    def update(self):
        height, width = self.window.getmaxyx()
        if height > 0 and width - len(self.begin_prompt) - 1 > 0:
            self.window.addstr(0, 0, self.begin_prompt, curses.color_pair(1))
            self.window.addstr(0, len(self.begin_prompt), self.text[:width - len(self.begin_prompt) - 1])
