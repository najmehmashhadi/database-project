#!/usr/bin/env python
from __future__ import print_function
import timeit
import sys
sys.path.append("../")
from pysyncobj import SyncObj, SyncObjConf, replicated


class KVStorage(SyncObj):
    def __init__(self, selfAddress, partnerAddrs):
        cfg = SyncObjConf(dynamicMembershipChange = True)
        super(KVStorage, self).__init__(selfAddress, partnerAddrs, cfg)
        self.__data = {}

    @replicated
    def set(self, key, value):
        self.__data[key] = value

    @replicated
    def pop(self, key):
        self.__data.pop(key, None)

    def get(self, key):
        return self.__data.get(key, None)

_g_kvstorage = None

def get_node():
#    global key
#    global _g_kvstorage
    resp=_g_kvstorage.get(key)

def cal_delay():
#    global node1,node2,node3,node4,node5,node6,node7

    elapsed_time = timeit.timeit(get_node, number=1)
    
    return elapsed_time    
def main():
    global _g_kvstorage
    _g_kvstorage = KVStorage('127.0.0.1:8081', ['127.0.0.1:8082','127.0.0.1:8083','127.0.0.1:8084','127.0.0.1:8085'])

    def get_input(v):
        if sys.version_info >= (3, 0):
            return input(v)
        else:
            return raw_input(v)
    global key
    while True:
        cmd = get_input(">> ").split()
        if not cmd:
            continue
        elif cmd[0] == 'set':
            key=cmd[1]
            _g_kvstorage.set(cmd[1], cmd[2])
        elif cmd[0] == 'get':
            print(_g_kvstorage.get(cmd[1]))
            key=cmd[1]
        elif cmd[0] == 'pop':
            print(_g_kvstorage.pop(cmd[1]))
            key=cmd[1]
        elif cmd[0] == 'cal':
            print(cal_delay()) 
        else:
            print('Wrong command')

if __name__ == '__main__':
    main()
