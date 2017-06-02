from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker
from schema import mapping_data


def init_db(config):
    metadata = MetaData()
    engine = create_engine(config['SQLALCHEMY_DATABASE_URI'])
    mapping_data(metadata)
    metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    session.commit()

    return session
