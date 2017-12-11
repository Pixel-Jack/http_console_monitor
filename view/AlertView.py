import curses


class AlertView:
    def __init__(self, window, list_historic=[]):
        self.window = window
        self.historic = list_historic
        self.update(0)

    def set_list_historic(self, list_historic):
        if not isinstance(list_historic, list):
            exit("AlertView : set_list_historic wrong entry {}".format(list_historic))
        self.historic = list_historic

    def update(self, position):
        positon_y = position
        # Initialization
        self.window.clear()
        height, width = self.window.getmaxyx()
        # because of borders
        height_write_space = height - 2
        width_write_space = width - 2
        if height_write_space > 2 and width_write_space > 2:

            # Declaration of strings
            title = "Historic Alerts"

            ### Titre curses example
            # Turning on attributes for title
            self.window.attron(curses.color_pair(1))
            self.window.attron(curses.A_BOLD)

            # Rendering title
            self.window.addstr(1, 1, title[:width_write_space])

            # Turning off attributes for title
            self.window.attroff(curses.color_pair(1))
            self.window.attroff(curses.A_BOLD)
            #######################


            nb_row_written = 2
            ### The rest
            # Print rest of text
            if len(self.historic) > 0:
                if len(self.historic) <= height_write_space:
                    historic_to_proceed = self.historic
                    positon_y = 0
                else:
                    if positon_y > len(self.historic) - height_write_space + 1:
                        positon_y = len(self.historic) - height_write_space + 1
                    historic_to_proceed = self.historic[-height_write_space + 1 - positon_y:]

                for hist in historic_to_proceed:
                    if hist[0]:
                        self.window.attron(curses.color_pair(2))
                    else:
                        self.window.attron(curses.color_pair(3))

                    self.window.addstr(nb_row_written, 1, str(hist[1])[:width_write_space])
                    nb_row_written += 1
                    if nb_row_written > height_write_space:
                        break

                    if hist[0]:
                        self.window.attroff(curses.color_pair(2))
                    else:
                        self.window.attroff(curses.color_pair(3))

            self.window.border()
            return positon_y
