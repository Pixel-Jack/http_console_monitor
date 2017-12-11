import sys,os
from datetime import datetime
from random import randint
import time

DATE = datetime.now()
STATUS_1 = list(range(100, 103))
STATUS_2 = list(range(200, 209)) + [210, 226]
STATUS_3 = list(range(300, 309)) + [310]
STATUS_4 = list(range(400, 419)) + list(range(421, 427)) + [428, 429, 431, 449, 450, 451, 456]
STATUS_5 = list(range(500, 513))
STATUS_MORE = [200, 200, 200, 400, 403, 404] * 20
STATUS = STATUS_1 + STATUS_2 + STATUS_3 + STATUS_4 + STATUS_5 + STATUS_MORE
NB_STATUS = len(STATUS)

PATHS = ['/home', '/', '/user/samuel/imgDog', '/user/michel/imgDog', '/profile/beach', '/profile/sun',
         '/profile/tomorrow', '/util/stock', 'r']
NB_PATHS = len(PATHS)

USERS = ['michel', 'mark', 'philipe', 'monique', 'franck', 'r']

METHODS = ['GET', 'GET', 'GET', 'POST', 'HEAD', 'OPTIONS', 'CONNECT', 'TRACE', 'PUT', 'PATCH', 'DELETE']

PROTOCOLS = ['HTTP/0.9', 'HTTP/1.0', 'HTTP/1.1']


def gen_rd_ip():
    return "{}.{}.{}.{}".format(randint(1, 255), randint(0, 255), randint(0, 255), randint(0, 255))


def gen_rd_status():
    return STATUS[randint(0, NB_STATUS - 1)]


def gen_rd_size():
    return randint(0, 16000)


def gen_rd_user():
    user = USERS[randint(0, len(USERS) - 1)]
    if user == 'r':
        nb_char = randint(1, 10)
        user = ''
        for i in range(nb_char):
            user += chr(randint(33, 126))
    return user


def gen_rd_method():
    return METHODS[randint(0, len(METHODS) - 1)]


def gen_rd_protocol():
    return PROTOCOLS[randint(0, len(PROTOCOLS) - 1)]


def gen_rd_path():
    path = PATHS[randint(0, len(PATHS) - 1)]
    if path == 'r':
        nb_char = randint(4, 10)
        path = '/'
        for i in range(nb_char):
            path += chr(randint(33, 126))
        index_slash = randint(3, len(path) - 2)
        path = path[:index_slash] + '/' + path[index_slash:]
    return path


if __name__ == '__main__':
    for arg in sys.argv[1:]:
        if os.path.isfile(arg):
            FILE_NAME = arg
            break

    if not 'FILE_NAME' in vars():
        if len(sys.argv[1:]) > 0 :
            FILE_NAME = sys.argv[1]
        else :
            FILE_NAME = "log/{}.log".format(DATE)
        # creation of the file
        fichier = open(FILE_NAME,"w")
        fichier.close()

    count_before_attack = randint(15, 30)
    under_one_user_attack = False
    attack_decided = False
    while True:
        if not under_one_user_attack:
            ip_client = gen_rd_ip()
            user_name = gen_rd_user()
            date = datetime.utcnow().strftime("%d/%b/%Y:%H:%M:%S %z")
            method = gen_rd_method()
            path = gen_rd_path()
            protocol = gen_rd_protocol()
            status = gen_rd_status()
            size = gen_rd_size()
            to_write = '{} - {} [{}] "{} {} {}" {} {}\n'.format(ip_client, user_name, date, method, path, protocol,
                                                                      status,
                                                                      size)
        with open(FILE_NAME, "a") as f:
            f.write(to_write)
        print(to_write)
        if count_before_attack == 0:
            if not attack_decided:
                if randint(0,100) < 60:
                    under_one_user_attack = True
                attack_decided = True
                nb_attack = randint(1,500)

            print("Attack, ", end='')
            if under_one_user_attack:
                # One IP make the same attack on one Path
                print("IP {} on PATH {}".format(ip_client, path))
            else:
                print("Flood !")
            if nb_attack == 0:
                print("end\n")
                count_before_attack = randint(50, 100)
                attack_decided = False
                under_one_user_attack = False
            else :
                nb_attack -= 1
                print("{} attacks remaining".format(nb_attack))
        else:
            time_before_next_log = randint(0, 10) / 10
            time.sleep(time_before_next_log)
            count_before_attack -= 1
            print("{} before next attack".format(count_before_attack))
