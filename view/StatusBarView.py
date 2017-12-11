import curses


class StatusBarView:
    def __init__(self, window, text='INIT'):
        self.window = window
        self.text = text
        self.window.clear()
        self.update()

    def set_text(self, text):
        self.text = text

    def update(self, is_alert=False):
        statusbarstr = "'q' to exit | {}".format(self.text)
        label_tabs = " ALERT ('a') | IP ('z') | USER ('e') | HTTP ('r')"
        height, width = self.window.getmaxyx()
        width_1_2 = int(width / 2)

        if height > 0 and width - len(statusbarstr) - len(label_tabs) - 1 > 0 and width_1_2 > 2:
            ### Status bar du bas
            if not is_alert:
                self.window.attron(curses.color_pair(4))
            else:
                self.window.attron(curses.color_pair(5))

            self.window.addstr(0, 0, statusbarstr[:width_1_2])
            if len(statusbarstr) < width_1_2:
                self.window.addstr(0, len(statusbarstr), " " * (width - width_1_2 - 1))
            self.window.addstr(0, width_1_2, label_tabs[:width_1_2])
            if len(label_tabs) < width_1_2:
                self.window.addstr(0, width_1_2 + len(label_tabs), " " * (width_1_2 - len(label_tabs) - 1))

            if not is_alert:
                self.window.attroff(curses.color_pair(4))
            else:
                self.window.attroff(curses.color_pair(5))
                ####################
