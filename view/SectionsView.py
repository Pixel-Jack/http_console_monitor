import curses
import operator

class SectionsView:
    def __init__(self, window, list_dict_sections={}):
        self.window = window
        self.list_dict_sections = list_dict_sections
        self.window.clear()
        self.update()

    def set_dict_sections(self, d_sections):
        list_items = [x for x in d_sections.items()]
        self.list_dict_sections = sorted(list_items, key=lambda x: x[1]['count'], reverse=True)

    def update(self):
        # Initialization
        self.window.clear()
        height, width = self.window.getmaxyx()
        height_space_write = height - 2
        width_space_write = width - 2
        title = "Information logged by section (order by number of hits)"

        if height_space_write > 0 and width_space_write > 7:
            ### Titre curses example
            # Turning on attributes for title
            self.window.attron(curses.color_pair(1))
            self.window.attron(curses.A_BOLD)

            # Rendering title
            self.window.addstr(1, 1, title[:width_space_write])

            # Turning off attributes for title
            self.window.attroff(curses.color_pair(1))
            self.window.attroff(curses.A_BOLD)
            #######################
            nb_row_written = 2
            for section_name, info in self.list_dict_sections:
                if nb_row_written >= height_space_write:
                    break
                self.window.addstr(nb_row_written, 1, section_name[:width_space_write - 1])
                nb_row_written += 1
                if nb_row_written > height_space_write:
                    break
                str_count = 'Count : {} *method : (status, count),...*'.format(info['count'])
                self.window.addstr(nb_row_written, 4, str_count[:width_space_write - 4])
                nb_row_written += 1
                if nb_row_written >= height_space_write:
                    break
                try:
                    method_list = sorted(info.items())
                    for key, status_dict in method_list:
                        if key != 'count':
                            status_list = map(str, sorted(status_dict.items(), key=lambda x: x[1],reverse=True))
                            status_str = ' '.join(status_list)
                            str_method = "{}: {}".format(key, status_str)
                            self.window.addstr(nb_row_written, 7, str_method[:width_space_write - 7])
                            nb_row_written += 1
                            if nb_row_written > height_space_write:
                                break
                except:
                    raise
            self.window.border()
