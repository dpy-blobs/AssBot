import inspect

class BotAction:
    def __init__(self, coro, name, *args, **kwargs):
        self.coro = coro
        self.name = name
        self.args = args
        self.kwargs = kwargs

    def get_method(self):
        return self.coro.__func__

    def get_coro_parent(self):
        wrapped = self.coro.__func__

        if inspect.ismethod(wrapped):
            for cls in inspect.getmro(wrapped.__self__.__class__):
                if cls.__dict__.get(wrapped.__name__) is wrapped:
                    return cls
            wrapped = wrapped.__func__
        if inspect.isfunction(wrapped):
            cls = getattr(inspect.getmodule(wrapped),
                          wrapped.__qualname__.split('.<locals>', 1)[0].rsplit('.', 1)[0])
            if isinstance(cls, type):
                return cls
        return getattr(wrapped, '__objclass__', None)

    def get_coro_cog(self, bot):
        return bot.get_cog(self.get_coro_parent().__name__)
