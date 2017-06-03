import short_url
from contextlib import contextmanager
from application.models import Links, Requests
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
        self.link_service = LinkService(session)
        self.request_service = RequestService(session)

    def create_request(self, url):
        link = self.get_link(url)
        self.request_service.add(link)

    def get_link(self, url):
        link = self.link_service.get_by_url(url)
        if not link:
            link = self.link_service.add(url)

            with db_action(self.link_service.session):
                link.hash = short_url.encode_url(link.id)

        return link

    def get_link_by_hash(self, hash_):
        return self.link_service.get_by_hash(hash_=hash_)

    def get_last_requests(self):
        return self.request_service.get_all(limit=5)

    def prepare_url(self, url):
        return url.strip()


class LinkService(object):
    def __init__(self, session):
        self.session = session

    def add(self, url):
        with db_action(self.session):
            link = Links(url)
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


class RequestService(object):
    def __init__(self, session):
        self.session = session

    def add(self, link):
        with db_action(self.session):
            request = Requests(link)
            self.session.add(request)

    def get_all(self, limit):
        try:
            return self.session.query(Requests).order_by(Requests.id.desc()).limit(limit=limit).all()
        except NoResultFound:
            return None
