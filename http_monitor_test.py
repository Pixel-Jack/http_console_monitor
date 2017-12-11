#!/usr/bin/env python

import _thread
import random as rd
from _datetime import datetime, timezone
from time import sleep

from controller.MainController import MainController

list_request = [
    '10.99.113.5 - monique [{0}] "OPTIONS /profile/tomorrow HTTP/1.1" 101 3617',
    '201.12.163.230 - philipe [{0}] "DELETE /profile/beach HTTP/1.0" 200 1106',
    '214.74.139.77 - michel [{0}] "GET / HTTP/0.9" 200 8882',
    '193.108.27.240 - philipe [{0}] "OPTIONS /home HTTP/1.1" 200 3070'
    '37.91.210.139 - mark [{0}] "GET /util/stock HTTP/1.1" 412 4676',
    '226.157.137.2 - ^Tom<+<6K [{0}] "PATCH /util/stock HTTP/0.9" 510 3267',
    '22.163.176.10 - michel [{0}] "GET /profile/beach HTTP/0.9" 400 3758',
    '89.36.16.149 - U [{0}] "HEAD /util/stock HTTP/1.1" 501 1850',
    '86.201.44.199 - monique [{0}] "HEAD / HTTP/1.1" 404 14132',
    '172.22.146.197 - mark [{0}] "POST /home HTTP/1.1" 507 8747',
    '219.126.109.122 - mark [{0}] "CONNECT /user/michel/imgDog HTTP/1.1" 200 4455',
    '126.88.234.191 - franck [{0}] "GET /profile/tomorrow HTTP/0.9" 200 14639',
    '13.95.41.45 - michel [{0}] "GET /home HTTP/1.1" 200 741',
    '129.50.139.4 - michel [{0}] "POST /profile/beach HTTP/1.1" 407 1665',
    '95.46.38.227 - monique [{0}] "GET /profile/tomorrow HTTP/0.9" 415 0',
    '4.26.48.201 - franck [{0}] "PUT /`un/`0] HTTP/0.9" 200 9226']
FILE_NAME = 'log_test.log'


def create_log_test(threadName, delay):
    # with 1s by refresh
    # with a threshold set to 200 => alert between 10s to 20s
    list_nb_to_send = [20] * 20 + [0] * 60
    # creation of the file
    fichier = open(FILE_NAME, "w")
    fichier.close()
    for nb_to_send in list_nb_to_send:
        request_to_send = list_request[rd.randint(0, len(list_request) - 1)]

        with open(FILE_NAME, 'a') as f:
            for i in range(nb_to_send):
                time = datetime.utcnow().replace(tzinfo=timezone.utc).strftime("%d/%b/%Y:%H:%M:%S %z")
                to_send = request_to_send.format(time)
                f.write(to_send + '\n')

        sleep(delay)


if __name__ == '__main__':
    _thread.start_new_thread(create_log_test, ("Thread-1", 1))
    application = MainController({'file_path': 'log_test.log', 'threshold':200})
