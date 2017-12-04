import curses

class HistoricHTTPView :
    def __init__(self,window,text=''):
        self.window = window
        self.text = str(text)
        self.window.clear()
        self.refresh()

    def set_list_historic(self,text):
        self.text=str(text)

    def refresh(self):
        # Initialization
        self.window.clear()
        height, width = self.window.getmaxyx()
        if height > 2 and width > 2 : # borders

            # Declaration of strings
            title = "View Historic HTTP"[:width-1]


            ### En haut a gauche
            # Rendering some text
            whstr = "Width: {}, Height: {}".format(width, height)[:width-1]
            self.window.addstr(1, 1, whstr, curses.color_pair(1))
            #####################


            ### Titre curses example
            # Turning on attributes for title
            self.window.attron(curses.color_pair(2))
            self.window.attron(curses.A_BOLD)

            # Rendering title
            self.window.addstr(3, 1, title[:width-1])

            # Turning off attributes for title
            self.window.attroff(curses.color_pair(2))
            self.window.attroff(curses.A_BOLD)
            #######################

            ### The rest
            # Print rest of text
            self.window.addstr(4, 1, self.text)
            ##############

            # Refresh the screen
            self.window.refresh()
            self.window.border()

