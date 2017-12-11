import os
import re
import sys
import time
from _datetime import datetime, timezone
from threading import Thread, RLock

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from model.HistoricHTTPModel import HistoricHTTPModel
from model.AlertHTTPModel import AlertHTTPModel
from controller.write_log_application import write
import curses
lock = RLock()


class HistoricHTTPWatcher(Thread):
    """
    This class is the thread which will look into the HistoricHTTPModel in order to see if there is a problem or not
    If it find an issue it will create an alert entry in the AlertHTTPModel
    This class is also responsible of statics return
    """

    def __init__(self, historic_http_model=HistoricHTTPModel(), alert_http_model=AlertHTTPModel(), delay_statics=10,
                 yield_to_update=None, average=600):
        """
        Creation of the thread which will check the state of the current historic and return statics and Alert
        :param alert_http_model:
        :param delay_statics:
        """
        Thread.__init__(self)
        self.alert_http_model = alert_http_model
        self.historic_http_model = historic_http_model
        self.delay_statics = delay_statics
        self.__is_running = True
        self.sections_dico_infos = {}
        self.statistics = {}
        self.yield_to_update = yield_to_update
        self.average = average
        self.is_alert = False

    def run(self):
        while self.__is_running:
            # each iteration clean the dico
            self.sections_dico_infos = {}
            self.statistics = {}
            lock.acquire()
            requests_in_delay = self.historic_http_model.get_historic_in_last_delay(self.delay_statics)
            first_request = self.historic_http_model.get_first_request()
            total_request, number_status_200 = self.historic_http_model.get_info_total_historic('200')
            lock.release()
            # return a list of request
            nb_requests = len(requests_in_delay)

            for request in requests_in_delay:
                try:
                    regex = r"(\/[^/]*)(\/.*)?"
                    section = re.search(regex, request[5])[1]
                    method = request[4]
                    status = request[7]
                    self.update_sections_dico_infos(section, method, status)

                except IndexError:
                    # if request = []
                    pass
                except TypeError:
                    # if section is corrupted
                    pass
                except:
                    write(sys.exc_info())

            if len(self.sections_dico_infos.items()) > 0:
                section, count_hit, count_200, count_401, count_403, count_404, count_500 = self.__get_info_about_most_hit_section()
                self.statistics = {'Number of Request in delay': nb_requests, 'Most hit': section,
                                   'Total hit': count_hit, 'Hit with response status 200': count_200,
                                   'Hit with response status 401': count_401, 'Hit with response status 403': count_403,
                                   'Hit with response status 404': count_404, 'Hit with response status 500': count_500,
                                   'First request logged in the file': first_request[3],
                                   "Total requests logged": total_request, "Total of status 200": number_status_200}

                if self.yield_to_update:
                    self.yield_to_update()
            # Useful in order to stop this thread quicker if we quit the httpMonitoring
            i = 0

            average_2_min = self.historic_http_model.get_average_in_last_two_min()
            if not self.is_alert:
                if  average_2_min >= self.average:
                    curses.beep()
                    self.is_alert = True
                    self.alert_http_model.add_to_historic([True,
                                                           "High traffic generated an alert - hits = {}, triggered at {}".format(
                                                               average_2_min,
                                                               datetime.utcnow().replace(
                                                                   tzinfo=timezone.utc))])
            else:
                if average_2_min <= self.average:
                    self.is_alert = False
                    self.alert_http_model.add_to_historic([False,
                                                           "Traffic recovered - hits = {}, triggered at {}".format(
                                                               average_2_min,
                                                               datetime.utcnow().replace(
                                                                   tzinfo=timezone.utc))])

            while i < 10:
                # to avoid python bug such as 0.1 + 0.1 + 0.1  = 0.33333333333
                i += 1
                if self.__is_running:
                    time.sleep(self.delay_statics / 10)

    def stop(self):
        self.__is_running = False
        exit("\nEnd of HistoricHTTPWatcher after a call to stop()")

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

    def __get_info_about_most_hit_section(self):
        list_tuple_section_info = [x for x in self.sections_dico_infos.items()]
        most_hit_section = sorted(list_tuple_section_info, key=lambda x: x[1]['count'])[
            -1]  # we take the last element of a list ascending sorted list
        section_name = most_hit_section[0]
        count_hit = most_hit_section[1]['count']
        # We will count the number of succeeded request
        count_200 = 0
        count_401 = 0
        count_403 = 0
        count_404 = 0
        count_500 = 0
        # Ex of most_hit_section : ('/pme', {'count': 500, 'GET': {'200': 1, '404': 1}, 'POST': {'200': 1, '404': 1}})
        for key_method, value in most_hit_section[1].items():
            if key_method != 'count':
                for key_status, count_status in value.items():
                    try:
                        if key_status == '200':
                            count_200 += count_status
                    except:
                        # There is no status 200
                        pass
                    try:
                        if key_status == '401':
                            count_401 += count_status
                    except:
                        # There is no status 200
                        pass
                    try:
                        if key_status == '403':
                            count_403 += count_status
                    except:
                        # There is no status 200
                        pass
                    try:
                        if key_status == '404':
                            count_404 += count_status
                    except:
                        # There is no status 200
                        pass
                    try:
                        if key_status == '500':
                            count_500 += count_status
                    except:
                        # There is no status 200
                        pass
        return section_name, count_hit, count_200, count_401, count_403, count_404, count_500

    def get_statistics(self):
        return self.statistics
