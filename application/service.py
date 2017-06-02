import short_url
from contextlib import contextmanager
from application.models import Links
from sqlalchemy.orm.exc import NoResultFound


@contextmanager
def db_action(app_session):
    try:
        yield
        app_session.commit()
    except Exception as ex:
        print ex
        app_session.rollback()


class Service(object):
    def __init__(self, session):
        self.repository = LinkRepository(session)

    def create_link(self, url):
        link = self.repository.get_by_url(url)
        if not link:
            link = self.repository.add(url)

        if not link.hash:
            with db_action(self.repository.session):
                link.hash = short_url.encode_url(link.id)

    def get_link_by_hash(self, hash_):
        return self.repository.get_by_hash(hash_=hash_)

    def get_all_links(self):
        return self.repository.get_all()


class LinkRepository(object):
    def __init__(self, session):
        self.session = session

    def add(self, url):
        link = Links(url)
        with db_action(self.session):
            self.session.add(link)
        return link

    def get_by_url(self, url):
        try:
            return self.session.query(Links).filter(Links.url == url).one()
        except NoResultFound:
            return None

    def get_by_hash(self, hash_):
        try:
            return self.session.query(Links).filter(Links.hash == hash_).one()
        except NoResultFound:
            return None

    def get_all(self):
        return self.session.query(Links).order_by(Links.id.desc()).all()
