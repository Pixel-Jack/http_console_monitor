import curses

from controller.HTTPLogWatcher import HTTPLogWatcher
from controller.HistoricHTTPWatcher import HistoricHTTPWatcher
from model.AlertHTTPModel import AlertHTTPModel
from model.HistoricHTTPModel import HistoricHTTPModel
from model.InformationModel import InformationModel
from view.AlertView import AlertView
from view.GraphicRequestView import GraphicRequestView
from view.HistoricHTTPView import HistoricHTTPView
from view.IPsView import IPsView
from view.SectionsView import SectionsView
from view.StatisticsView import StatisticsView
from view.StatusBarView import StatusBarView
from view.UsersView import UsersView


class MainController:
    def __init__(self, dict_param):
        self.stdscr = None
        ### Attributs
        self.delay_general = int(dict_param.get('delay_refresh_general', 2))
        self.threshold = int(dict_param.get('threshold', 400))
        self.delay_statistics = int(dict_param.get('delay_refresh_statistics', 10))
        self.file_path = dict_param.get('file_path', '')

        self.__state_tab = 'ALERT'

        ### Model
        self.historic_http = HistoricHTTPModel()
        self.information = InformationModel()
        self.alert_http = AlertHTTPModel()

        ### Threads
        self.http_log_watcher = HTTPLogWatcher(file_path=self.file_path, delay_to_refresh=self.delay_general,
                                               yield_to_update=self.__log_watcher_ask_to_refresh,
                                               hist_http_model=self.historic_http, information_model=self.information)
        self.log_name = self.http_log_watcher.get_log_name()
        self.historic_http_watcher = HistoricHTTPWatcher(historic_http_model=self.historic_http,
                                                         alert_http_model=self.alert_http,
                                                         delay_statics=self.delay_statistics,
                                                         yield_to_update=self.__http_watcher_ask_to_refresh,
                                                         average=self.threshold)

        ### Dimensions
        self.input_ch = 0
        self.height, self.width = 0, 0
        self.height_sub_1_2 = 0
        self.width_sub_1_2 = 0
        self.height_sub_1_2_inf = 0
        self.height_input = 1
        self.height_status_bar = 1
        self.width_sub_1_3 = 0
        self.width_sub_2_3 = 0

        # value to refresh
        self.historic_count_hit_in_delay = []
        self.statistics = {}

        # Views and windows
        # sections
        self.window_sections_view = None
        self.sections_view = None
        #### Tabs
        # HTTP
        self.window_tab = None
        self.http_view = None
        # IP
        self.ip_view = None
        # USER
        self.user_view = None
        # ALERT
        self.alert_view = None
        ######
        # StatusBar
        self.window_status_bar_view = None
        self.status_bar_view = None
        # GraphicRequest
        self.window_graphic_request_view = None
        self.graphic_request_view = None
        # Statistics
        self.window_statistics_view = None
        self.statistics_view = None

        self.position = 0

        # Wrap for more stability
        curses.wrapper(self.setup)

    def __del__(self):
        self.__end_threads()

    def _define_dimensions(self):
        self.height, self.width = self.stdscr.getmaxyx()
        self.height_sub_1_2_inf = max(int(self.height / 3), 0)
        self.height_sub_1_2 = max(0, self.height - self.height_sub_1_2_inf - 1)
        self.width_sub_1_2 = int(self.width / 2)
        self.width_sub_1_3 = int(self.width / 3)
        self.width_sub_1_4 = int(self.width / 4)
        self.width_sub_2_3 = int(self.width * 2 / 3)

    def setup(self, screen):
        try:
            self.stdscr = screen
            self._define_dimensions()
            # Clear and refresh the screen for a blank canvas
            self.stdscr.clear()
            self.stdscr.refresh()
            self.__init_color()

            # Views and windows initialisation
            # All the right part
            self.__display_tab_window()

            # sections
            self.window_sections_view = self.stdscr.subwin(self.height_sub_1_2, self.width_sub_1_2, 0, 0)
            self.sections_view = SectionsView(self.window_sections_view,
                                              self.information.get_sections_info())

            # StatusBar
            self.window_status_bar_view = self.stdscr.subwin(self.height_status_bar, self.width,
                                                             self.height - self.height_status_bar, 0)
            self.status_bar_view = StatusBarView(self.window_status_bar_view,
                                                 "{} | ".format(self.log_name))
            # Graphic Request
            self.window_graphic_request_view = self.stdscr.subwin(self.height_sub_1_2_inf,
                                                                  self.width_sub_1_4, self.height_sub_1_2, 0)
            self.graphic_request_view = GraphicRequestView(self.window_graphic_request_view, delay=self.delay_general,
                                                           threshold=self.threshold)
            # Statistics
            self.window_statistics_view = self.stdscr.subwin(self.height_sub_1_2_inf,
                                                             self.width_sub_1_4, self.height_sub_1_2,
                                                             self.width_sub_1_3)
            self.statistics_view = StatisticsView(self.window_statistics_view, delay=self.delay_statistics)

            # we launch the application
            self.start()

        except KeyboardInterrupt:
            pass
        finally:
            self.__end_threads()
            curses.endwin()

    def start(self):

        # # LAUNCH of thread
        self.http_log_watcher.start()
        self.historic_http_watcher.start()

        self.file_name = self.http_log_watcher.get_log_name()

        if self.file_name != '':

            # Loop where self.input_ch is the last character pressed
            while self.input_ch is not None:
                if self.input_ch == ord('q'):
                    break
                elif self.input_ch == ord('a'):
                    self.__state_tab = 'ALERT'
                elif self.input_ch == ord('z'):
                    self.__state_tab = 'IP'
                elif self.input_ch == ord('e'):
                    self.__state_tab = 'USER'
                elif self.input_ch == ord('r'):
                    self.__state_tab = 'HTTP'
                elif self.input_ch == curses.KEY_UP:
                    self.position += 1
                elif self.input_ch == curses.KEY_DOWN:
                    self.position = max(0, self.position - 1)

                self.__refresh_window()
                # Wait for next input
                self.input_ch = self.stdscr.getch()
        else:
            self.__end_threads()
            curses.endwin()

    def __refresh_window(self):
        # Initialization
        self.stdscr.clear()
        # each time we have to check that the window hasn't been resized
        self._define_dimensions()

        self.__resize_window()

        self.sections_view.set_dict_sections(
            self.information.get_sections_info())
        self.sections_view.update()

        is_in_alert = self.alert_http.is_in_alert()
        str_alert = ''
        if is_in_alert:
            str_alert = 'ALERT'
        self.status_bar_view.set_text(
            "{} | {} | {}".format(self.log_name, str_alert, self.position))
        self.status_bar_view.update(is_in_alert)

        self.__display_tab_window()

        self.historic_count_hit_in_delay = self.historic_http.get_count_request_historic()
        self.graphic_request_view.set_list_historic(self.historic_count_hit_in_delay)
        self.graphic_request_view.update()

        self.statistics_view.set_dict_infos(self.statistics)
        self.statistics_view.update()

        self.stdscr.refresh()

    def __resize_window(self):
        try:
            ### Modification of views
            self.window_sections_view.resize(self.height_sub_1_2, self.width_sub_1_2)
            self.window_sections_view.mvderwin(0, 0)

            self.window_status_bar_view.resize(self.height_status_bar, self.width)
            self.window_status_bar_view.mvderwin(self.height - self.height_status_bar, 0)

            self.window_tab.resize(self.height - self.height_status_bar, self.width_sub_1_2)
            self.window_tab.mvderwin(0, self.width_sub_1_2)

            self.window_graphic_request_view.resize(self.height_sub_1_2_inf, self.width_sub_1_4)
            self.window_graphic_request_view.mvderwin(self.height_sub_1_2, 0)

            self.window_statistics_view.resize(self.height_sub_1_2_inf, self.width_sub_1_4)
            self.window_statistics_view.mvderwin(self.height_sub_1_2, self.width_sub_1_4)
        except curses.error:
            if self.height > 1 and self.width > 1:
                # if an error occur its because of the resize so at least we move the window in order to allow a future resize
                self.window_status_bar_view.mvderwin(self.height_sub_1_2, 0)
                self.window_tab.mvderwin(0, self.width_sub_1_2)
                self.window_graphic_request_view.mvderwin(self.height_sub_1_2, 0)
                self.window_sections_view.mvderwin(0, 0)
                self.window_statistics_view.mvderwin(self.height_sub_1_2, self.width_sub_1_4)

    def __display_tab_window(self):
        if self.__state_tab == 'HTTP':
            try:
                self.http_view.set_list_historic(list(self.historic_http.get_historic()))
                self.http_view.update()
            except AttributeError:
                # HTTP
                self.window_tab = self.stdscr.subwin(self.height - self.height_status_bar, self.width_sub_1_2, 0,
                                                     self.width_sub_1_2)
                self.http_view = HistoricHTTPView(self.window_tab, list(self.historic_http.get_historic()))
                self.http_view.update()
        elif self.__state_tab == 'IP':
            try:
                self.ip_view.set_dict_ips(self.http_log_watcher.get_ip_dico_infos())
                self.ip_view.update()
            except AttributeError:
                # IP
                self.window_tab = self.stdscr.subwin(self.height - self.height_status_bar, self.width_sub_1_2, 0,
                                                     self.width_sub_1_2)
                self.ip_view = IPsView(self.window_tab, self.http_log_watcher.get_ip_dico_infos())
                self.ip_view.update()
        elif self.__state_tab == 'USER':
            try:
                self.user_view.set_dict_users(self.http_log_watcher.get_user_dico_infos())
                self.user_view.update()
            except AttributeError:
                # USER
                self.window_tab = self.stdscr.subwin(self.height - self.height_status_bar, self.width_sub_1_2, 0,
                                                     self.width_sub_1_2)
                self.user_view = UsersView(self.window_tab, self.http_log_watcher.get_user_dico_infos())
                self.user_view.update()
        elif self.__state_tab == 'ALERT':
            try:
                self.alert_view.set_list_historic(self.alert_http.get_historic())
                self.position = self.alert_view.update(self.position)
            except AttributeError:
                # USER
                self.window_tab = self.stdscr.subwin(self.height - self.height_status_bar, self.width_sub_1_2, 0,
                                                     self.width_sub_1_2)
                self.alert_view = AlertView(self.window_tab, self.alert_http.get_historic())
                self.position = self.alert_view.update(self.position)

    def __log_watcher_ask_to_refresh(self):
        self.__refresh_window()

    def __http_watcher_ask_to_refresh(self):
        self.statistics = self.historic_http_watcher.get_statistics()
        self.statistics_view.set_dict_infos(self.statistics)
        self.statistics_view.update()

    def __end_threads(self):
        try:
            self.http_log_watcher.stop()
        except:
            pass
        try:
            self.historic_http_watcher.stop()
        except:
            pass

    @staticmethod
    def __init_color():
        # Start colors in curses
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK)
