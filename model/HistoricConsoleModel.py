class HistoricConsoleModel:
    def __init__(self, historic=[]):
        self.historic = historic

    def add_to_historic(self, new_line):
        self.historic.append(new_line)

    def get_historic(self, height, position):
        if height > len(self.historic):
            return self.historic
        else:
            if(position == 0):
                return self.historic[-height:]
            return self.historic[-(height + position) : -position]

    def get_historic_length(self):
        return len(self.historic)
