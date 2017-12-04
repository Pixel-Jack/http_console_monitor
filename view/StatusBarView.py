import curses

class StatusBarView:
    def __init__(self,window, text ='INIT'):
        self.window = window
        self.text = text
        self.window.clear()
        self.refresh()

    def set_text(self,text):
        self.text = text

    def refresh(self):
        statusbarstr = " Send 'exit' to exit | STATUS BAR | {}".format(self.text)
        height, width = self.window.getmaxyx()
        if height > 0 and width - len(statusbarstr) - 1 > 0 :
            ### Status bar du bas
            self.window.attron(curses.color_pair(4))
            self.window.addstr(0, 0, statusbarstr)
            self.window.addstr(0, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
            self.window.attroff(curses.color_pair(4))
            ####################

            # Refresh the screen
            self.window.refresh()