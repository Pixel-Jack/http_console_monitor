class HistoricConsoleModel :
    def __init__(self, historic=[]):
        self.historic = historic


    def add_to_historic(self, new_line):
        self.historic.append(new_line)

    def get_historic(self,interval=()):
        if interval != ():
            begin = interval[0]
            end = interval[1]
            return self.historic[begin:end]
        return self.historic
