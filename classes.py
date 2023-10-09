class Thing:
    def __init__(
        self,
        name,
        desc=None,
        items=None,
        on_take=None,
        places=None,
        # moveable=False,
    ):
        self.name = name  # for all
        self.desc = desc  # for all (look)
        self.items = items  # for all (look)
        self.on_take = on_take  # for take
        self.places = places  # for place (open)
        self.moveable = not not self.on_take
        # self.moveable = moveable  # for item (take)


class Door:
    def __init__(self, name, dest, desc=None, locked=False):
        self.name = name
        self.dest = dest
        self.desc = desc
        self.locked = locked
        self.items = False
