#!/usr/bin/env python
import sys
import signal
import socket
import struct
import threading
import time
import random

import rospy
from std_msgs.msg import String
from marvelmind_nav.msg import hedge_pos


class ClientThread(threading.Thread):
    def __init__(self, client_address, clientsock):
        threading.Thread.__init__(self)
        self.client_socket = clientsock
        print ("New connection added: ", client_address)
        rospy.Subscriber("/hedge_pos", hedge_pos, self.callback, queue_size=1)

        self.eps = 0

    def run(self):
        rospy.spin()

    def callback(self, data):
        # get message from tracking device
        x = data.x_m
        y = data.y_m
        z = data.z_m

        # # test
        # if self.eps > 5:
        #     self.eps = 0
        # else:
        #     self.eps += 1
        #
        # x += self.eps

        print(x, y, z)
        flag = 0
        sign = True
        for elem in [x, y, z, flag]:
            elem_hex = struct.pack('f', elem)
            if sign:
                msg = elem_hex
                sign = False
            else:
                msg += elem_hex
        try:
            self.client_socket.sendall(msg)
            print(msg)
            time.sleep(1)
        except socket.error:
            self.client_socket.close()
            print("Error client lost")
            return


def quit_server(signal_num, frame):
    print("you stop the threading")
    sys.exit()


if __name__ == '__main__':
    rospy.init_node('message_arm_server', anonymous=True)

    # create a socket:
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # listen port:
    serverSocket.bind(('192.168.1.100', 49152))

    serverSocket.listen(5)
    print("Server started")
    print("Waiting for client request..")
    try:
        while True:
            signal.signal(signal.SIGINT, quit_server)
            signal.signal(signal.SIGTERM, quit_server)
            time.sleep(2)
            serverSocket.listen(5)
            clientsock, client_address = serverSocket.accept()
            newthread = ClientThread(client_address, clientsock)
            newthread.setDaemon(True)
            newthread.start()
    except KeyboardInterrupt as e:
        print("you stop the threading")
