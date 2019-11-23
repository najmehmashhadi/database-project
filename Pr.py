import tkinter as tk
from utils import*
#import time




def main():

    node1 = KVStorage('127.0.0.1:8081', ['127.0.0.1:8082','127.0.0.1:8083'])
    node2 = KVStorage('127.0.0.1:8082', ['127.0.0.1:8081','127.0.0.1:8083'])
    node3 = KVStorage('127.0.0.1:8083', ['127.0.0.1:8081','127.0.0.1:8082'])
    
#    node1.set('k3', [4,5,6])
#    time.sleep(2)
#    print(dataset1.get('k3'))
#    dataset1.set('k3', [4,8])
#    time.sleep(2)
#    print(dataset1.get('k3'))
    main_app=main_app_fun(node1)

    main_app.mainloop()


if __name__ == '__main__':
    main()


