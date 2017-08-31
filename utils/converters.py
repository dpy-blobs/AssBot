from discord.ext import commands


class CaseInsensitiveDict(dict):
    def __contains__(self, k):
        return super().__contains__(k.lower())

    def __delitem__(self, k):
        return super().__delitem__(k.lower())

    def __getitem__(self, k):
        return super().__getitem__(k.lower())

    def get(self, k, default=None):
        return super().get(k.lower(), default)

    def __setitem__(self, k, v):
        super().__setitem__(k.lower(), v)


class CaseInsensitiveGroup(commands.Group):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.all_commands = CaseInsensitiveDict()


def caseinsensitivegroup(name=None, **attrs):
    return commands.command(name=name, cls=CaseInsensitiveGroup, **attrs)
