#!/usr/bin/env python
# -*- coding: utf-8 -*-
import thread
import socket

clients = []


# 为每一个客户端连接 创立一个线程
def server_run(cli, addr, name):
    global clients
    while True:
        try:
            data = cli.recv(1024)
            if not data:
                # 当存在断开的客户端的时候 从cclients里面把其移除
                clients.remove((cli, addr, name))
                cli.close()

                # 移除之后 通知其他客户端，他的离开
                for c in clients:
                    c[0].send(name + " is out!")
                break
        except Exception, e:
            print e
            clients.remove((cli, addr, name))
            cli.close()
            # 移除之后 通知其他客户端，他的离开
            for c in clients:
                c[0].send(name + " is out!")
            break

        # 遍历 给每一个连接客户端发送消息
        for c in clients:
            c[0].send(name + " say: " + data)


def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("localhost", 5555))
    s.listen(5)
    while True:
        print 'waiting for connection...'
        client, addr = s.accept()
        name = client.recv(1024)
        print '...connected from :', addr

        # 把一个连接 放入全局变量clients中
        clients.append((client, addr, name),)

        # 为每一个客户端连接 创立一个线程
        thread.start_new_thread(server_run, (client, addr, name))


if __name__ == '__main__':
    server()
