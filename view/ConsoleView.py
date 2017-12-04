import curses


class ConsoleView:
    def __init__(self, window, list_historic=[]):
        self.window = window
        self.list_historic = list_historic
        self.window.clear()
        self.refresh()

    def set_list_historic(self,historic):
        self.list_historic = historic

    def refresh(self):
        height, width = self.window.getmaxyx()
        if height > 0 and width > 0:
            ### The rest
            # Print rest of text
            for index, row_text in enumerate(self.list_historic):
                try :
                    self.window.addstr(1 + index, 1, row_text[:width - 1])
                except:
                    self.window.addstr(1 + index, 1, 'Error with {}'.format(row_text))
            ##############

            # Refresh the screen
            self.window.refresh()
            self.window.border()


    def _split_text_width(self,text):
        max_width = self.width_sub_win
        return [text[i: i + max_width] for i in range(0, len(text), max_width)]

