# encoding: utf-8
"""
@version: 1.0
@author: Jarrett
@file: check_license
@time: 2020/5/27 9:24
"""

from active_license.get_mac_addr import get_mac_address, hash_msg
from datetime import datetime

class CheckLicense():
    """
    Check user's license.
    """
    def __init__(self):
        pass
    def check_psw(self, psw):
        """
        check encoded password in user's license.
        :param psw: str, encoded password.
        :return: boolean, check result.
        """
        mac_addr = get_mac_address()
        hashed_msg = hash_msg('faw' + str(mac_addr))
        if psw == hashed_msg:
            return True
        else:
            return False
    def check_date(self, lic_date):
        """
        check datetime in user's license.
        :param lic_date: str, license datetime.
        :return: boolean, if the active days smaller than current_time, return Flase.
        """
        current_time = datetime.now().isoformat()   # get current time which is iso format.
        current_time_array = datetime.strptime(current_time, "%Y-%m-%dT%H:%M:%S.%f")    # switch the str datetime to array.
        lic_date_array = datetime.strptime(lic_date, "%Y-%m-%dT%H:%M:%S")    # the array type is datetime.datetime.
        remain_days = lic_date_array - current_time_array
        remain_days = remain_days.days
        if remain_days < 0 or remain_days == 0:
            return False
        else:
            return True
    def get_authorization_days(self):
        """
        active datetime by user in first time.
        :return: str, current datetime.
        """
        active_date = datetime.now().isoformat(sep=' ')     # current time, the separator is space.
        return active_date


if __name__ == '__main__':
    # # current_time = datetime.now().isoformat('T') # https://www.cnblogs.com/yyds/p/6369211.html
    # # print(current_time)
    # # current_time = datetime.strptime('2017/02/04 20:49', '%Y/%m/%d %H:%M')
    # time1 = '2020-05-27T10:43:12.400947'
    # timeArray = datetime.strptime(time1, "%Y-%m-%dT%H:%M:%S.%f")
    # # timeArray = datetime.fromtimestamp(time1)
    # print(timeArray)
    # print(type(timeArray))
    # time2 = '2018-05-27T10:43:12.400947'
    # timeArray_2 = datetime.strptime(time2, "%Y-%m-%dT%H:%M:%S.%f")
    # d_delta = timeArray_2 - timeArray
    # print(d_delta)
    # print(d_delta.days)
    # # day_time = datetime(timeArray)
    # # print(day_time)
    # # dt = datetime.fromtimestamp(timeArray)
    # # print(dt)
    # # d1 = datetime(timeArray)
    # # print(d1)
    #
    # # d2 = datetime('')
    # # day_delta = d1 - d2
    # # print(day_delta)
    time1 = '2022-05-27T10:43:12.400947'
    check_date_result = CheckLicense().check_date(time1)
    print(check_date_result)

    pass
    # mac_addr = get_mac_address()
    # hash_result = hash_msg(mac_addr)
    # print(hash_result)
    # check_lic = CheckLicense()
    # check_state = check_lic.check_psw(hash_result)
    # print(check_state)
