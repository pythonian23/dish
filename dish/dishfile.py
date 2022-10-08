import typing


class DishFile(typing.TypedDict):
    command: str
    aliases: typing.List[str]
    description: str
    run: str
