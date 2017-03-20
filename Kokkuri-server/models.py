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

import sqlalchemy
from sqlalchemy import create_engine, func, Column, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.declarative import declarative_base

from utils import logger

logger.info("SQLAlchemy Version: {0}".format(sqlalchemy.__version__))
engine = create_engine('mysql+mysqldb://root:123456@127.0.0.1/kokkuri?charset=utf8mb4', encoding='utf8')
ModelBase = declarative_base()
Session = sessionmaker(bind=engine)


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

    def delete(self):
        self.is_deleted = 1

    def __init__(self, user, source_ip, target_host, result):
        self.user = user
        self.source_ip = source_ip
        self.target_host = target_host
        self.result = result

    def __str__(self):
        return "<KokkuriSSHEvent {0}>".format(self.created_time)

    def __repr__(self):
        return "<KokkuriSSHEvent {0}>".format(self.created_time)


class KokkuriSSHPot(ModelBase):
    """
    记录SSH的蜜罐以及状态
    """

    __tablename__ = "kokkuri_ssh_pot"

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    container_name = Column(String(length=64))
    container_id = Column(String(length=64), index=True)
    honeypot_ip = Column(String(16), index=True)
    attacker_ip = Column(String(length=16), index=True)

    # 0: 关闭; 1: 开启
    status = Column(INTEGER(2, unsigned=True), default=1)
    ssh_port = Column(String(length=6))

    created_time = Column(DateTime, server_default=func.now(), default=func.now(), index=True)
    updated_time = Column(DateTime, onupdate=func.now(), server_onupdate=func.now(), server_default=func.now())
    is_deleted = Column(INTEGER(2, unsigned=True), default=0, server_default="0")

    def delete(self):
        self.is_deleted = 1

    def __init__(self, container_name, container_id, pot_ip, attacker_ip, ssh_port, status=1):
        self.container_name = container_name
        self.container_id = container_id
        self.honeypot_ip = pot_ip
        self.attacker_ip = attacker_ip
        self.status = status
        self.ssh_port = ssh_port

if __name__ == '__main__':
    ModelBase.metadata.create_all(engine)

