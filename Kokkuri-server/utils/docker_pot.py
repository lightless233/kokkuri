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

import docker

from config import server_config
from utils import logger


class DockerPot(object):

    def __init__(self):
        super(DockerPot, self).__init__()
        self.client = docker.APIClient(base_url=server_config.DOCKER_BASE_URL)

        logger.info("Docker API Version: {0}".format(self.client.version().get("ApiVersion")))

    def create_container(self):
        pass


