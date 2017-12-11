from _datetime import datetime, timedelta, timezone

from controller.write_log_application import write


class HistoricHTTPModel:
    """
    Historic of HTTP request
    filled every 10sec with a new list of request ask in the last 10 sec
    So historic is a list of list of w3c-format-string ex : [[ip, user_identifier, user_name, date_request, method, path, protocol, status, size],...]
    """

    def __init__(self, historic=[]):
        self.historic = historic

    def add_to_historic(self, new_entry):
        if not isinstance(new_entry, list):
            write("HistoricHTTPModel : add_to_historic wrong entry {}".format(new_entry))
        self.historic.append(list(new_entry))

    def get_historic(self, interval=()):
        if interval != ():
            begin = interval[0]
            end = interval[1]
            return list(self.historic[begin:end])
        return list(self.historic)

    def get_count_request_historic(self, interval=()):
        """
        Function called in order to get the number of request by 10secs to build the graphic
        :param interval:
        :return: list of int which represents the number of request by 10sec
        """
        data = list(self.historic)
        if interval != ():
            begin = interval[0]
            end = interval[1]
            data[begin:end]
        nb_request_list = []
        for d in data:
            nb_request_list.append(len(d))
        return nb_request_list

    def get_historic_in_last_delay(self, delay):
        """
        Function will return all request in the last delay seconds
        :param delay: int (second)
        :return: list of request ex :  ['74.70.42.49', '-', 'franck', '10/Dec/2017:09:16:07 ', 'GET', '/util/stock', 'HTTP/0.9', '404', '15275'], ['162.27.33.144', '-', 'mark', '10/Dec/2017:09:16:06 ', 'PUT', '/profile/tomorrow', 'HTTP/1.1', '503', '15457']
        """
        if not isinstance(delay, int):
            write("HistoricHTTPModel : add_to_historic wrong entry {}".format(delay))
        data = list(self.historic)
        data.reverse()
        info_to_return = []
        ready_to_return = False
        for refresh in data:
            refresh.reverse()
            for request in refresh:
                info_to_return.append(request)
            for request in refresh:
                str_time_request = request[3]
                try:
                    datetime_time = datetime.strptime(str_time_request, "%d/%b/%Y:%H:%M:%S %z")
                except:
                    # We presume that no timezone entered means UTC zone
                    datetime_time = datetime.strptime(str_time_request, "%d/%b/%Y:%H:%M:%S ")
                    datetime_time = datetime_time.replace(tzinfo=timezone.utc)
                datetime_now = datetime.utcnow().replace(tzinfo=timezone.utc)
                if datetime_now - datetime_time <= timedelta(days=0, minutes=0, seconds=delay):
                    info_to_return.append(request)
                else:
                    ready_to_return = True
                    break
            if ready_to_return:
                break
        return info_to_return

    def get_average_in_last_two_min(self):
        data = list(self.historic)
        data.reverse()
        info_to_return = []
        ready_to_return = False
        for refresh in data:
            refresh.reverse()
            for request in refresh:
                info_to_return.append(request)
            for request in refresh:
                str_time_request = request[3]
                try:
                    datetime_time = datetime.strptime(str_time_request, "%d/%b/%Y:%H:%M:%S %z")
                except:
                    # We presume that no timezone entered means UTC zone
                    datetime_time = datetime.strptime(str_time_request, "%d/%b/%Y:%H:%M:%S ")
                    datetime_time = datetime_time.replace(tzinfo=timezone.utc)
                datetime_now = datetime.utcnow().replace(tzinfo=timezone.utc)
                if datetime_now - datetime_time <= timedelta(days=0, minutes=2, seconds=0):
                    info_to_return.append(request)
                else:
                    ready_to_return = True
                    break
            if ready_to_return:
                break
        return len(info_to_return)

    def get_first_request(self):
        """
        :return: return list of information about the first request or empty list if the historic is empty
        """
        try:
            return list(self.historic[0][0])
        except:
            return []

    def get_info_total_historic(self, status):
        if not isinstance(status, str):
            return 0
        count_status = 0
        count_requests = 0
        for packet in self.historic:
            for request in packet:
                count_requests += 1
                if request[7] == status:
                    count_status += 1
        return count_requests, count_status
