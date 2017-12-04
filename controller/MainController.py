import sys
import curses
from tools import handle_input
from view.ConsoleView import ConsoleView
from view.HistoricHTTPView import HistoricHTTPView
from view.StatusBarView import StatusBarView
from view.InputView import InputView
from model.HistoricConsoleModel import HistoricConsoleModel
import subprocess


class MainController:
    def __init__(self):
        self.stdscr = None
        self.historic_console = HistoricConsoleModel()
        self.input_ch = 0
        self.cursor_position = 0
        self.position_console = 0
        self.text_prompt = ''
        self.begin_prompt = '>> '
        self.height, self.width = 0, 0
        self.height_sub_win = 0
        self.width_sub_win = 0
        self.height_input = 1
        self.console_view_height = 0

        # Views and windows
        self.window_input_view = None
        self.input_view = None
        # console
        self.window_console_view = None
        self.console_view = None
        # HTTP
        self.window_http_view = None
        self.http_view = None
        # StatusBar
        self.window_status_bar_view = None
        self.status_bar_view = None

        # Wrap for more stability
        curses.wrapper(self.setup)

    def setup(self, screen):
        self.stdscr = screen
        self.height, self.width = self.stdscr.getmaxyx()
        self.height_sub_win = self.height - 1
        self.width_sub_win = self.width / 2
        self.console_view_height = self.height_sub_win - self.height_input
        # Clear and refresh the screen for a blank canvas
        self.stdscr.clear()
        self.stdscr.refresh()
        self.init_color()

        # Views and windows initialisation
        # input
        self.window_input_view = self.stdscr.subwin(self.height_input, self.width_sub_win,
                                                    self.height - self.height_input - 1, 0)
        self.input_view = InputView(self.window_input_view, self.text_prompt, self.begin_prompt)
        self.stdscr.move(self.height_sub_win - self.height_input, self.cursor_position + len(self.begin_prompt))
        # console
        self.window_console_view = self.stdscr.subwin(self.console_view_height, self.width_sub_win, 0, 0)
        self.console_view = ConsoleView(self.window_console_view,
                                        self.historic_console.get_historic(self.height_sub_win - 3,
                                                                           self.position_console))
        # HTTP
        self.window_http_view = self.stdscr.subwin(self.height_sub_win, self.width_sub_win, 0, self.width_sub_win)
        self.http_view = HistoricHTTPView(self.window_http_view, '')
        # StatusBar
        self.window_status_bar_view = self.stdscr.subwin(1, self.width, self.height_sub_win, 0)
        self.status_bar_view = StatusBarView(self.window_status_bar_view, self.input_ch)

        # we launch the application
        self.start()

    def init_color(self):
        # Start colors in curses
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_GREEN)

    def start(self):
        # Loop where self.input_ch is the last character pressed
        while self.input_ch != None:

            # Initialization
            self.stdscr.clear()
            # each time we have to check that the window hasn't been resized
            self.height, self.width = self.stdscr.getmaxyx()
            self.height_sub_win = self.height - 1;
            self.width_sub_win = self.width / 2
            self.height_input = 1
            self.console_view_height = self.height_sub_win - self.height_input

            # We check the input in the prompt
            self.text_prompt, self.cursor_position, push_command = handle_input(self.input_ch, self.text_prompt,
                                                                                self.cursor_position)

            self.according_to_push_command(push_command)
            self.resize_window()

            self.input_view.set_text(self.text_prompt)
            self.input_view.refresh()
            self.stdscr.move(self.height_sub_win - self.height_input, self.cursor_position + len(self.begin_prompt))

            self.console_view.set_list_historic(
                self.historic_console.get_historic(self.height_sub_win - 3, self.position_console))
            self.console_view.refresh()

            self.status_bar_view.set_text(self.input_ch)
            self.status_bar_view.refresh()

            self.http_view.set_list_historic(push_command)
            self.http_view.refresh()

            # Wait for next input
            self.input_ch = self.stdscr.getch()

    def resize_window(self):
        try:
            ### Modification of views
            self.window_input_view.resize(self.height_input, self.width_sub_win)
            # we want that the prompt entry always be at the bottom
            self.window_input_view.mvderwin(self.height - self.height_input - 1, 0)

            self.stdscr.move(self.height_sub_win - self.height_input, self.cursor_position + len(self.begin_prompt))

            self.window_console_view.resize(self.console_view_height, self.width_sub_win)
            self.window_status_bar_view.resize(1, self.width)
            self.window_status_bar_view.mvderwin(self.height_sub_win, 0)

            self.window_http_view.resize(self.height_sub_win, self.width_sub_win)
            self.window_http_view.mvderwin(0, self.width_sub_win)

        except curses.error:
            # if an error occur its because of the resize so at least we move the window in order to allow a future resize
            self.window_input_view.mvderwin(self.height - self.height_input - 1, 0)
            self.window_status_bar_view.mvderwin(self.height_sub_win, 0)
            self.stdscr.move(self.height_sub_win - self.height_input, self.cursor_position + len(self.begin_prompt))
            self.window_http_view.mvderwin(0, self.width_sub_win)

    def according_to_push_command(self, command):
        if command == 'exit':
            sys.exit()
        elif len(command) != 0 and command != '':
            historic_console_length = self.historic_console.get_historic_length()

            if command == 'UP':
                self.position_console = min(max(0, historic_console_length - self.console_view_height + 2),
                                            self.position_console + 1)
            elif command == 'DOWN':
                self.position_console = max(0, self.position_console - 1)
            elif command.split(' ')[0] in ['ls', 'netstat', 'w', 'who', 'ifconfig', 'pwd']:
                prompt = self.begin_prompt + command
                self.historic_console.add_to_historic(prompt)
                try:
                    retour = subprocess.check_output(command.split(' ')).split('\n')
                except:
                    retour = ["Error in command {}".format(sys.exc_info())]
                for e in retour:
                    self.historic_console.add_to_historic(e)
            else:
                prompt = self.begin_prompt + command
                self.historic_console.add_to_historic(prompt)
                self.historic_console.add_to_historic("This command can't be used here")
