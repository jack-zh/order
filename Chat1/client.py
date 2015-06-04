#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import time
import thread

name = ""


def send(cli):
    global name
    while True:
        world = raw_input('')
        world = world.strip()
        if len(world) > 0:
            cli.send(world)


def recv(cli):
    while True:
        dat = cli.recv(1024)
        if not dat:
            break
        print dat


def tcpClient():
    global name
    clisock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clisock.connect(('localhost', 5555))
    clisock.send(name)
    # 此线程负责发送消息
    thread.start_new_thread(send, (clisock,))
    # 此线程负责接收消息
    thread.start_new_thread(recv, (clisock,))
    while True:
        _t = time.localtime(int(time.time()))
        time_str = time.strftime('%Y-%m-%d %H:%M:%S', _t)
        print "--------" + time_str + "----------"
        time.sleep(30)


if __name__ == "__main__":
    _name = raw_input('your name:')
    name = _name
    tcpClient()
