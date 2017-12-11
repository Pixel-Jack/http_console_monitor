import curses


class UsersView:
    def __init__(self, window, list_dict_users=[]):
        self.window = window
        self.list_dict_users = list_dict_users
        self.window.clear()
        self.update()

    def set_dict_users(self, d_users):
        list_items = [x for x in d_users.items()]
        self.list_dict_users = sorted(list_items, key=lambda x: x[1]['volume'], reverse=True)

    def update(self):
        # Initialization
        self.window.clear()
        height, width = self.window.getmaxyx()
        height_space_write = height - 2
        width_space_write = width - 2
        title = "Information logged by IP (order by Total size requests)"

        if height_space_write > 0 and width_space_write > 0:
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

            if len(self.list_dict_users) > 0:
                for info_ip in self.list_dict_users:
                    if len(info_ip) > 1 :
                        ip = info_ip[0]
                        info = info_ip[1]
                        if isinstance(info,dict):
                            if nb_row_written >= height_space_write:
                                break

                            self.window.addstr(nb_row_written, 2, ip[:width_space_write - 2])
                            nb_row_written += 1
                            if nb_row_written > height_space_write:
                                break

                            str_last_request = 'Last request : {}'.format(info['last_request'])
                            self.window.addstr(nb_row_written, 5, str_last_request[:width_space_write - 5])
                            nb_row_written += 1
                            if nb_row_written > height_space_write:
                                break

                            str_volume = 'Total size requests : {}'.format(info['volume'])
                            self.window.addstr(nb_row_written, 5, str_volume[:width_space_write - 5])
                            nb_row_written += 1
                            if nb_row_written > height_space_write:
                                break

                            str_count = 'Count : {} *section : (status, count),...*'.format(info['count'])
                            self.window.addstr(nb_row_written, 5, str_count[:width_space_write - 5])
                            nb_row_written += 1
                            if nb_row_written >= height_space_write:
                                break
                            try:
                                method_list = sorted(info.items())
                                for key, status_dict in method_list:
                                    if key not in ['count', 'volume', 'last_request']:
                                        status_list = map(str, sorted(status_dict.items(), key=lambda x: x[1], reverse=True))
                                        status_str = ' '.join(status_list)
                                        str_method = "{}: {}".format(key, status_str)
                                        self.window.addstr(nb_row_written, 8, str_method[:width_space_write - 8])
                                        nb_row_written += 1
                                        if nb_row_written > height_space_write:
                                            break
                            except:
                                raise
            self.window.border()
