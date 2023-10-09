from Be import *
from classes import *
from seek import Game
#import tkinter as tk
#import customtkinter as ctk
#from tkinter import ttk
#from tkinter import messagebox


class AfikomanHunt(Game):
    def __init__(self ):
        super().__init__('Afikoman Hunt')
        self.first = 2  # starting room
        self.current_room = self.first
        self.doors = [
            Door(
                "Cupboard door",
                {1: 0, 0: 1},
                desc="This is the door to the walk-in cupboard.",
            ),
            Door(
                "Master Bedroom door",
                {2: 1, 1: 2},
                desc="This is the the door to the master bedroom.",
                locked=True,
            ),
            Door("Kitchen Door", {2: 3, 3: 2}, desc="This is the door to the kitchen."),
            Door(
                "Serving door",
                {3: 4, 4: 3},
                desc="This is the door between the kitchen and dining room.",
            ),
            Door(
                "Dining room door",
                {2: 4, 4: 2},
                desc="This is the door to the dining room.",
            ),
            Door(
                "Older kids bedroom door",
                {2: 5, 5: 2},
                desc="This is the door to the older kids bedroom.",
            ),
            Door(
                "Younger kids bedroom door",
                {2: 6, 6: 2},
                desc="This is the door to the younger kids bedroom.",
            ),
            Door(
                "Front door", {7: 2, 0: 7}, desc="This is the door back to the house."
            ),
        ]

        self.places = [
            Thing(
                "Walk-in cupboard",
                desc="You are in the walk-in cupboard.\n"
                + "As you look around the slightly cramped space,\n"
                + "You see mostly empty shelves\n"
                + "and some clothes hanging from\n"
                + "a rod on the wall.",
                items=[
                    Thing(
                        "Pile of clothes",
                        desc="These clothes must have fallen from the rod.",
                        items=[
                            Thing(
                                "Afikoman",
                                desc="This is the Afikoman you've been looking for.",
                                on_take=self.win,
                                # moveable=True,
                            )
                        ],
                    )
                ],
                places=[self.doors[0]],
            ),
            Thing(
                "Master bedroom",
                desc="As you look around the bedroom you see\n"
                + "a queen bed and a king bed\n"
                + "with a bedside table betweeen them,\n"
                + "a walk-in cupboard,\n"
                + "and several cardboard boxes.",
                places=[self.doors[1], self.doors[0]],
            ),
            Thing(
                "Hallway",
                desc="As you look around the hallway\n" + "you see nothing of note.",
                places=[
                    self.doors[1],
                    self.doors[2],
                    self.doors[4],
                    self.doors[5],
                    self.doors[6],
                ],
            ),
            Thing(
                "Kitchen",
                desc="You are in a kitchen with\n"
                + "a tiled floor.\n"
                + "You see\n"
                + "a marble counter with a sink,\n"
                + "a small oven,\n"
                + "and a disproportionately large fridge/freezer.",
                items=[
                    Thing(
                        "Cupboard",
                        desc="This is the kitchen cupboard.\n" + "It is locked.",
                    )
                ],
                places=[self.doors[2], self.doors[3]],
            ),
            # Dining room
            Thing(
                "Dining room",
                desc="As you enter the dining room you see\n"
                + "numerous bookshelves lining one wall\n"
                + "with a breakfront in the center.",
                items=[
                    Thing(
                        "Table",
                        desc="This is the table.\n" + "It is empty.",
                        items=[Thing("Note", desc="The note reads: update zork")],
                    )
                ],
                places=[self.doors[4], self.doors[3]],
            ),
            Thing(
                "Older kids bedroom",
                desc="In the older kids bedroom you see\n"
                + "two single beds,\n"
                + "and a clothes cupboard",
                items=[
                    Thing(
                        "Bookshelf",
                        desc="On the bookshelf you see various titles,\n"
                        + "including '101 BASIC computer games'.",
                    )
                ],
                places=[self.doors[5]],
            ),
            Thing(
                "Younger kids bedroom",
                desc="In the younger kids bedroom you see\n"
                + "two single beds\n"
                + "in green and yellow,\n"
                + "and a clothes cupboard.",
                items=[
                    Thing(
                        "Toybox",
                        desc="You look through the toybox.",
                        items=[
                            Thing(
                                "Key",
                                desc="This is the key to the master bedroom.",
                                on_take=self.get_key,
                            )
                        ],
                    )
                ],
                places=[self.doors[6]],
            ),
            Thing(
                "Garden",
                desc="You are in the garden\n" + "at the end of the game.",
                items=[
                    Thing(
                        "Plaque",
                        desc="The plaque reads:\n"
                        + "Credits:\n"
                        + "Game: coolcoder613(Elozor Bruce)\n"
                        + "Haiku-PyAPI": "coolcoder613 & ZardShard",
                    ),
                ],
                places=[self.doors[7]],
            ),
        ]

    def show(self, text, action="", showcmd=True):
        self.desc.set(
            "\n".join(
                (
                    self.desc.get()
                    + "\n"
                    + (f"[{action}:]\n" if showcmd else "")
                    + text
                ).splitlines()[-20:]
            )
        )

    def open_door(self, door, show=True):
        if not door.locked:
            self.current_room = door.dest[self.current_room]
            self.name.set(self.places[self.current_room].name)
            self.show(
                self.look_at(self.places[self.current_room], show=False),
                f"Open {door.name}",
                showcmd=show,
            )
            self.gen_menus(self.places[self.current_room], True)
        else:
            self.show("That door is locked.", f"Open {door.name}", showcmd=show)

    def look_at(self, thing, showcmd=True, surr=False, show=True):
        desc = (
            "\n".join(
                (
                    thing.desc if thing.desc else "...",
                    *(f"There is a {x.name} here." for x in thing.items),
                )
            )
            if thing.items
            else thing.desc
        )
        if thing.items:
            self.gen_menus(thing)
        if show:
            self.show(
                desc,
                f"Look at {'Surroundings' if surr else thing.name}",
                showcmd=showcmd,
            )
        else:
            return desc

    def take_item(self, item, parent):
        parent.items.pop(parent.items.index(item))
        self.gen_menus(self.places[self.current_room], new=True)
        item.on_take()

    def win(self):
        self.show("***YOU WON***\n" + "There is a loud whoosh.", "Take Afikoman")
        self.open_door(self.doors[7], False)

    def get_key(self):
        self.show("You take the key.", "Take Key")
        self.doors[1].locked = False

    def is_in_menu(self, menu, name):
        last = menu.index(tk.END)
        last = last if last != None else 0
        for x in range(last + 1):
            if menu.entrycget(x, "label") == name:
                return True
        return False

    def gen_menus(self, thing, new=False):
        # current_place = self.places[self.first]
        if new:
            self.open_menu.delete(0, "end")
            self.look_at_menu.delete(0, "end")
            self.take_menu.delete(0, "end")
        if thing in self.places:
            if thing.desc and not self.is_in_menu(self.look_at_menu, "Surroundings"):
                self.look_at_menu.add_command(
                    label="Surroundings",
                    command=lambda item=thing: self.look_at(item, surr=True),
                )

        if thing.items:
            for item in thing.items:
                if (
                    isinstance(item, Thing)
                    and item.moveable
                    and not self.is_in_menu(self.take_menu, item.name)
                ):
                    self.take_menu.add_command(
                        label=item.name,
                        command=lambda item=item: self.take_item(item, thing),
                    )
                if (item.desc or item.items) and not self.is_in_menu(
                    self.look_at_menu, item.name
                ):
                    self.look_at_menu.add_command(
                        label=item.name, command=lambda item=item: self.look_at(item)
                    )
                # if self.menu.index("end") != 0:
                #    self.menu_frame.add_cascade(label=item.name, menu=self.menu)
        if thing.places:
            for place in thing.places:
                if not self.is_in_menu(self.open_menu, place.name):
                    self.open_menu.add_command(
                        label=place.name,
                        command=lambda door=place: self.open_door(door),
                    )
                if place.desc and not self.is_in_menu(self.look_at_menu, place.name):
                    self.look_at_menu.add_command(
                        label=place.name, command=lambda item=place: self.look_at(item)
                    )


if __name__ == "__main__":
    game = Game()
    game.Run()
