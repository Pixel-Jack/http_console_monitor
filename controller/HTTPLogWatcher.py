import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from model.HistoricHTTPModel import HistoricHTTPModel
from model.InformationModel import InformationModel
from threading import Thread, RLock
import time
import glob
import re

lock = RLock()


class HTTPLogWatcher(Thread):
    """
    In the class if we give a file_path that's mean that we have a file to look.
    Otherwise we will look in the log directory and take the latest log file
    """

    def __init__(self, file_path='', delay_to_refresh=5, yield_to_update=None, hist_http_model=HistoricHTTPModel(),
                 information_model=InformationModel()):
        """
        :param file_path: The path of file with log in w3c format to read
        :param delay_to_refresh: specify the delay between each analysis
        :param look_at_me_now: function callback that the MainController pass in order to yield when a view update has to happen
        :param hist_http_model: the controller has to pass the model in which write the information
        """
        Thread.__init__(self)
        self.delay_refresh = delay_to_refresh
        self.sections_dico_infos = {}
        self.ip_dico_infos = {}
        self.user_dico_infos = {}
        self.yield_to_update = yield_to_update
        self.hist_http_model = hist_http_model
        self.information_model = information_model
        self.is_running = True
        self.file_to_watch = ''

        if file_path != '':
            self.file_to_watch = file_path
        else:
            list_files = glob.glob(os.path.join(os.path.dirname(__file__), '../log/*'))
            nb_files = len(list_files)
            if nb_files == 0:
                exit("There is no log to watch. Launch create_log.py or pass as parameter a path to log file")
            # So as to have have the log in chronological order
            list_files.sort()
            is_searching_log = True
            index_file = 1
            while is_searching_log and index_file <= nb_files:
                file = list_files[-index_file]
                # We know the format name of the file (see create_log)
                regex = r"\/log\/([0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{6}).log$"
                if re.search(regex, file):
                    is_searching_log = False
                    self.file_to_watch = file
                else:
                    index_file += 1
            try:
                pass
                # print("Log watched : {}".format(self.file_to_watch))
            except:
                exit("There is no log to watch. Launch create_log.py or pass as parameter a path to log file")

    def run(self):
        # we keep them to reduce the number of passage in the log file because it could be hudge
        # We need to read it few time because otherwise it could block the log generator
        last_line = ''
        index_last_line = -1

        while self.is_running:
            with open(self.file_to_watch, "r") as f:
                updated_data = [line for line in f]
            if len(updated_data) > 0 :
                # We assume that there can't be no changes before the last line that we checked at the previous iteration
                if index_last_line != -1 and updated_data[index_last_line] == last_line:
                    # We can be confident in the information saved before
                    data_to_interpret = self.update_information(updated_data[index_last_line + 1:])
                else:
                    # New data or corrupted data, we have to recheck everything again
                    data_to_interpret = self.build_information(updated_data)
                last_line = updated_data[-1]
                index_last_line = len(updated_data) - 1

            # Useful in order to stop this thread quicker if we quit the httpMonitoring
            i = 0
            while i < 10:
                # to avoid python bug such as 0.1 + 0.1 + 0.1  = 0.33333333333
                i += 1
                if self.is_running:
                    time.sleep(self.delay_refresh / 10)

    def stop(self):
        self.is_running = False
        print("\nEnd of HTTPLogWatcher after a call to stop()")

    def build_information(self, data):
        list_analysed_trame = []
        for line in data:
            analysed_trame = self.analyse_trame(line)
            list_analysed_trame.append(analysed_trame)
            path = analysed_trame[5]
            section = self.get_section_from_path(path)
            method = analysed_trame[4]
            status = analysed_trame[7]
            self.update_sections_dico_infos(section, method, status)
        return list_analysed_trame

    def update_information(self, data):
        """
        Here we can find information on the last period of delay_refresh
        such as number of request
        most hits
        active user
        :param data:
        :return: list of list of information about the request : [ip, user_identifier, user_name, date_request, method, path, protocol, status, size]
        """
        list_analysed_trame = []
        in_last_delay = []
        for d in data:
            analysed_trame = self.analyse_trame(d)
            in_last_delay.append(analysed_trame)
            list_analysed_trame.append(analysed_trame)
            ip_user = analysed_trame[0]
            user_name = analysed_trame[2]
            date_last_request = analysed_trame[3]
            path = analysed_trame[5]
            section = self.get_section_from_path(path)
            method = analysed_trame[4]
            status = analysed_trame[7]
            size = analysed_trame[8]
            self.update_sections_dico_infos(section, method, status)
            self.update_ip_dico_infos(ip_user, section, status, size, date_last_request)
            self.update_user_dico_infos(user_name,section,status,size,date_last_request)

        if self.hist_http_model:
            lock.acquire()
            self.hist_http_model.add_to_historic(in_last_delay)
            lock.release()
        if self.information_model:
            self.information_model.set_sections(self.sections_dico_infos)
        # Now we have modified the model we tell to the controller to update its state
        # We say to the controller that the sreen needs to be refreshed
        if self.yield_to_update:
            self.yield_to_update()
        return list_analysed_trame

    def update_sections_dico_infos(self, section, method, status):
        """
        create a structure to gather information about sections
        :param section:
        :param method:
        :param status:
        :return: 0
        """
        if section in self.sections_dico_infos.keys():
            self.sections_dico_infos[section]['count'] += 1
            if method in self.sections_dico_infos[section].keys():
                if status in self.sections_dico_infos[section][method].keys():
                    self.sections_dico_infos[section][method][status] += 1
                else:
                    self.sections_dico_infos[section][method][status] = 1
            else:
                self.sections_dico_infos[section][method] = {status: 1}
        else:
            self.sections_dico_infos[section] = {'count': 1, method: {status: 1}}
        return 0

    def update_ip_dico_infos(self, ip, section, status, size, date_last_request):
        """
        create a structure to gather information about ip
        :param section:
        :param method:
        :param status:
        :return: 0
        """
        if size == '-':
            size_int = 0
        else:
            size_int = int(size)

        if ip in self.ip_dico_infos.keys():
            self.ip_dico_infos[ip]['count'] += 1
            self.ip_dico_infos[ip]['volume'] += size_int
            self.ip_dico_infos[ip]['last_request'] = date_last_request
            if section in self.ip_dico_infos[ip].keys():
                if status in self.ip_dico_infos[ip][section].keys():
                    self.ip_dico_infos[ip][section][status] += 1
                else:
                    self.ip_dico_infos[ip][section][status] = 1
            else:
                self.ip_dico_infos[ip][section] = {status: 1}
        else:
            self.ip_dico_infos[ip] = {'count': 1, 'volume': size_int, 'last_request': date_last_request,
                                      section: {status: 1}}
        return 0

    def update_user_dico_infos(self, user, section, status, size, date_last_request):
        """
        create a structure to gather information about user
        :param section:
        :param method:
        :param status:
        :return: 0
        """
        if size == '-':
            size_int = 0
        else:
            size_int = int(size)

        if user in self.user_dico_infos.keys():
            self.user_dico_infos[user]['count'] += 1
            self.user_dico_infos[user]['volume'] += size_int
            self.user_dico_infos[user]['last_request'] = date_last_request
            if section in self.user_dico_infos[user].keys():
                if status in self.user_dico_infos[user][section].keys():
                    self.user_dico_infos[user][section][status] += 1
                else:
                    self.user_dico_infos[user][section][status] = 1
            else:
                self.user_dico_infos[user][section] = {status: 1}
        else:
            self.user_dico_infos[user] = {'count': 1, 'volume': size_int, 'last_request': date_last_request,
                                          section: {status: 1}}
        return 0

    @staticmethod
    def analyse_trame(trame):
        """"
        We will analyse the trame thanks to regex.
        We assume that there is only one information by trame otherwise it will be a loss of information
        :param trame: ex : 127.0.0.1 user-identifier frank [10/Oct/2000:13:55:36 -0700] "GET /apache_pb.gif HTTP/1.0" 200 2326
        :return : return a list of infos [ip, user_identifier, user_name, date_request, method, path, protocol, status, size] or an empty list if there is no information
        """
        regex = r"^(-|[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}) (.*) (.*) \[(-|.*)\] \"(-|[a-z A-Z]+) (.*) (.*)\" (-|[0-9]{1,3}) (-|[0-9]+)$"
        result = re.match(regex, trame)
        if result:
            ip = result.group(1)
            user_identifier = result.group(2)
            user_name = result.group(3)
            date_request = result.group(4)
            method = result.group(5)
            path = result.group(6)
            protocol = result.group(7)
            status = result.group(8)
            size = result.group(9)
            return [ip, user_identifier, user_name, date_request, method, path, protocol, status, size]
        return []

    @staticmethod
    def get_section_from_path(path):
        """
        Split the path in order to return the element before the second '/' We capture also the roots
        :param path: /profile/tomorrow/nfkznl
        :return: string with section /${section} or string null
        """
        regex = r"^(/.*?)(/.*)?$"
        result = re.match(regex, path)
        if result:
            return result.group(1)
        return ''

    def get_log_name(self):
        regex = r".*\/log\/([0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{6}.log)$"
        result = re.match(regex, self.file_to_watch)
        if result:
            return result.group(1)
        elif self.file_to_watch != '':
            return self.file_to_watch
        return "Error reading file name"

    def get_ip_dico_infos(self):
        return self.ip_dico_infos

    def get_user_dico_infos(self):
        return self.user_dico_infos


if __name__ == '__main__':
    watcher = HTTPLogWatcher()
    watcher.start()
