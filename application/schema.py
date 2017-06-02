from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import mapper, relationship
from models import Links, Requests


def mapping_data(metadata):
    links_table = Table('links', metadata,
                        Column('id', Integer, primary_key=True, autoincrement=True),
                        Column('url', String, unique=True, nullable=False),
                        Column('hash', String, unique=True, nullable=True), )
    requests_table = Table('requests', metadata,
                           Column('id', Integer, primary_key=True, autoincrement=True),
                           Column('link_id', Integer, ForeignKey('links.id'), nullable=False))

    mapper(Links, links_table)
    mapper(Requests, requests_table,
           properties={'link': relationship(Links, backref='requests')})
