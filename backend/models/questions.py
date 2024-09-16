from pydantic import RootModel

class Question(RootModel[str]):
    pass