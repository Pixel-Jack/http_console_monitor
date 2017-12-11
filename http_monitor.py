#!/usr/bin/env python3
import sys

from controller.MainController import MainController
import re
if __name__ == '__main__':
    dict_regex = {
        'file_path': r"^file_path=(.*)$",
        'delay_refresh_general': r"^delay_refresh_general=([0-9]+(\.[0-9]+)?)$",
        'delay_refresh_statistics': r"^delay_refresh_statistics=([0-9]+)$",
        'delay_refresh_alert': r"^delay_refresh_alert=([0-9]+(\.[0-9]+)?)$",
        'threshold': r"^threshold=([0-9]+)$",
    }
    dict_param = {}
    for arg in sys.argv[1:]:
        print(arg)
        for key,reg in dict_regex.items():
            match = re.match(reg,arg)
            if match:
                dict_param[key]=match.group(1)
                del dict_regex[key]
                break
    application = MainController(dict_param)
