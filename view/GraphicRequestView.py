import curses


class GraphicRequestView:
    def __init__(self, window, list_historic=[], threshold=10, delay=10):
        self.window = window
        self.list_historic = list_historic
        self.window.clear()
        self.threshold = threshold
        self.delay = delay

        self.update()

    def set_list_historic(self, historic):
        if not isinstance(historic, list):
            raise BaseException("GraphicRequestView : set_list_historic wrong entry {}".format(historic))
        self.list_historic = list(historic)

    def update(self):
        # Initialization
        self.window.clear()
        height, width = self.window.getmaxyx()
        height_space_write = height - 1
        width_space_write = width - 3
        title = "Absc : {}s Threshold : {}".format(self.delay, self.threshold)
        if height_space_write > 1 and width_space_write > len(title) and len(self.list_historic) > 0:
            self.window.addstr(0, width_space_write - len(title),title)
            reverse_histo = list(self.list_historic)
            # we will fill the space from the right to left
            reverse_histo.reverse()
            if len(reverse_histo) > width_space_write:
                reverse_histo = reverse_histo[:width_space_write - 1]
            for index, value in enumerate(reverse_histo):
                if width_space_write < 0:
                    break
                col = width_space_write - index
                self._draw_col(col, value, height_space_write)
        self.window.refresh()

    def _split_text_width(self, text):
        max_width = self.width_sub_win
        return [text[i: i + max_width] for i in range(0, len(text), max_width)]

    def _draw_col(self, col_num, value, heigh_graph):
        if value > self.threshold:
            height_col_in_graph = heigh_graph - 1
            is_warning = True
        else:
            height_col_in_graph = int(value * heigh_graph / self.threshold)
            is_warning = False
        if height_col_in_graph == 0:
            self.window.addstr(heigh_graph - 1, col_num, '-')
        for y in range(height_col_in_graph):
            if is_warning:
                self.window.attron(curses.color_pair(2))
                self.window.attron(curses.A_BOLD)
            # Rendering title
            self.window.addstr(heigh_graph - y - 1, col_num, '*')

            if is_warning:
                # Turning off attributes for title
                self.window.attroff(curses.color_pair(2))
                self.window.attroff(curses.A_BOLD)
        return 0
