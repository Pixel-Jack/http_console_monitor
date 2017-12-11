import curses


class StatisticsView:
    def __init__(self, window, dict_infos={}, delay=10):
        self.window = window
        self.dict_infos = dict_infos
        self.delay = delay
        self.window.clear()
        self.update()

    def set_dict_infos(self, d_infos):
        if not isinstance(d_infos, dict):
            raise BaseException("StatisticsView : set_list_infos wrong entry {}".format(d_infos))
        self.dict_infos = d_infos

    def update(self):
        # Initialization
        self.window.clear()
        height, width = self.window.getmaxyx()
        height_space_write = height - 3
        width_space_write = width - 3
        title = "Statistics about the last {}s:".format(self.delay)

        if height_space_write > 1 and width_space_write > 1:
            nb_row_written = 1
            ### Titre curses example
            # Turning on attributes for title
            self.window.attron(curses.color_pair(1))
            self.window.attron(curses.A_BOLD)

            # Rendering title
            self.window.addstr(nb_row_written, 1, title[:width_space_write])
            nb_row_written += 1
            # Turning off attributes for title
            self.window.attroff(curses.color_pair(1))
            self.window.attroff(curses.A_BOLD)
            #######################
            for key,info in self.dict_infos.items():
                if nb_row_written > height_space_write:
                    break
                text = "{} : {}".format(key, info)
                if len(text) <= width_space_write:
                    self.window.addstr(nb_row_written, 1, text[:width_space_write])
                else :
                    text = "{} :".format(key)
                    self.window.addstr(nb_row_written, 1, text[:width_space_write])
                    nb_row_written += 1
                    text = "   {}".format(info)
                    self.window.addstr(nb_row_written, 1, text[:width_space_write])
                nb_row_written +=1
        self.window.border()