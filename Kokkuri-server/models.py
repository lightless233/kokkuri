#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    models
    ~~~~~~

    Server's database models.

    :author:    lightless <root@lightless.me>
    :homepage:  https://github.com/LiGhT1EsS/kokkuri
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""

import datetime

import sqlalchemy
from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy import func
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.declarative import declarative_base

from utils import logger

logger.debug("SQLAlchemy Version: {0}".format(sqlalchemy.__version__))
engine = create_engine('mysql+mysqldb://root:123456@192.168.198.130/kokkuri?charset=utf8mb4', encoding='utf8')
ModelBase = declarative_base()


class KokkuriSSHEvent(ModelBase):
    """
    记录SSH登录事件
    """

    __tablename__ = "kokkuri_ssh_event"

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    user = Column(String(length=32), index=True)
    source_ip = Column(String(16), index=True)
    target_host = Column(String(64), index=True)
    result = Column(String(64), default=0, server_default="0")

    created_time = Column(DateTime, server_default=func.now(), default=func.now(), index=True)
    updated_time = Column(DateTime, onupdate=func.now(), server_onupdate=func.now(), server_default=func.now())
    is_deleted = Column(INTEGER(2, unsigned=True), default=0, server_default="0")


if __name__ == '__main__':
    ModelBase.metadata.create_all(engine)

