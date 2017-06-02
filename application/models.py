class Links(object):
    def __init__(self, url, hash_=None):
        self.url = url
        self.hash = hash_

    def __repr__(self):
        return '<Links: url {0}, hash {1}>'.format(self.url, self.hash)
