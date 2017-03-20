#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    utils.docker_pot
    ~~~~~~~~~~~~~~~~

    Control docker via docker api.

    :author:    lightless <root@lightless.me>
    :homepage:  https://github.com/LiGhT1EsS/kokkuri
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""

import random

import docker

from config import server_config
from utils import logger


class DockerPot(object):

    def __init__(self):
        super(DockerPot, self).__init__()
        self.client = docker.APIClient(base_url=server_config.DOCKER_BASE_URL)

        logger.info("Docker API Version: {0}".format(self.client.version().get("ApiVersion")))

    def create_container(self, container_name):
        """
        Create a honeypot container.
        Just open SSH service.
        :param container_name:
        :return:
        """

        ssh_port = random.randint(10000, 11000)

        container_id = self.client.create_container(
            "ubuntu_pot:v1", ports=[22],
            name=container_name,
            host_config=self.client.create_host_config(port_bindings={
                22: ssh_port,
            })
        )
        logger.debug(container_id)

        cid = container_id.get("Id")

        self.client.start(container_id)
        logger.info("A new honeypot start success. port: {0}".format(ssh_port))
        return cid, ssh_port


