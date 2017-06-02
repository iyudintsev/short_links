from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.orm import mapper
from models import Links


def mapping_data(metadata):
    links_table = Table('links', metadata,
                        Column('id', Integer, primary_key=True, autoincrement=True),
                        Column('url', String, unique=True, nullable=False),
                        Column('hash', String, unique=True, nullable=True), )
    mapper(Links, links_table)
