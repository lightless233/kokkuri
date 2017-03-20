#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Kokkuri Server Tests
    ~~~~~~~~~~~~~~~~~~~~

    Tests file.

    :author:    lightless <root@lightless.me>
    :homepage:  https://github.com/LiGhT1EsS/kokkuri
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""


import socket


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("0.0.0.0", 12666))
sock.listen(5)

while True:
    client, client_info = sock.accept()
    print(client.recv(1024))
