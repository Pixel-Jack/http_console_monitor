import curses


class HistoricHTTPView:
    def __init__(self, window, list_historic=[]):
        self.window = window
        self.historic = list_historic
        self.update()

    def set_list_historic(self, list_historic):
        if not isinstance(list_historic, list):
            exit("HistoricHTTPView : set_list_historic wrong entry {}".format(list_historic))
        self.historic = list_historic

    def update(self):
        # Initialization
        self.window.clear()
        height, width = self.window.getmaxyx()
        # because of borders
        height_write_space = height - 1
        width_write_space = width - 2
        if height_write_space > 2 and width_write_space > 2:

            # Declaration of strings
            title = "Historic HTTP"

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

            ### The rest
            # Print rest of text
            if len(self.historic) > 0:
                nb_line_written = 0
                # We fill the View from the bottom
                reversed_historic = list(self.historic)
                reversed_historic.reverse()
                for historic_in_delay in reversed_historic:
                    historic_in_delay.reverse()
                    nb_line_written += 1
                    for request in historic_in_delay:
                        if nb_line_written >= height_write_space - 1:  # because of the Title
                            break
                        request_str = ' '.join(request)
                        chunks = len(request_str)
                        # if a string overthrows the width we must put a carriage return
                        list_row_to_write = [request_str[i:i + width_write_space] for i in
                                             range(0, chunks, width_write_space)]
                        list_row_to_write.reverse()
                        for row in list_row_to_write:
                            try :
                                self.window.addstr(height_write_space - nb_line_written, 1, row)
                                nb_line_written += 1
                            except :
                                # Issue with the resize of the window, we break
                                nb_line_written = height_write_space + 1
                                break
                    if nb_line_written >= height_write_space - 1:  # because of the Title
                        break
            self.window.border()
