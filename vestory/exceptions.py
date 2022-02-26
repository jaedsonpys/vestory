class Base(Exception):
    pass


class RepoNotExistsError(Base):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
