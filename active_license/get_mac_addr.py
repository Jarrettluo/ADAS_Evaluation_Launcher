# encoding: utf-8
"""
@version: 1.0
@author: Jarrett
@file: get_mac_addr
@time: 2020/5/26 13:13
"""

import uuid
import hashlib

from Config import Config

def get_mac_address():
    mac = uuid.UUID(int = uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e+2] for e in range(0,11,2)])

def hash_msg(msg):
    sha256 = hashlib.sha256()
    sha256.update(msg.encode('utf-8'))
    res = sha256.hexdigest()
    return res


# if __name__ == '__main__':
#     # a = get_mac_address()
#     # print(a)
#     str_1 = 'd8:f2:ca:b3:9c:4a'
#     a = Config.SECRET_KEY
#     print(a)
#     psw = hash_msg(str_1)
#     print(psw)