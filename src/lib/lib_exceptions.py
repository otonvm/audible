class HTTPException(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg


class URLException(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg


class BS4Exception(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg


class RegExException(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg


class FileError(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg


class FolderNotFound(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg


class MP4BoxError(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg


class APError(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg
