from Be import *



class Game(BApplication):
    def __init__(self,title='Seek Game'):
        super().__init__('application/x-vnd.seek')
        self.title=title
        self.first = 0  # starting room
        self.current_room = self.first
        self.doors = []
        self.places = []
        self.msg_what=1

    def ReadyToRun(self):
        self.window=BWindow(
            BRect(100, 100, 700, 600),
            self.title,
            B_TITLED_WINDOW_LOOK,
            B_NORMAL_WINDOW_FEEL,
            B_QUIT_ON_WINDOW_CLOSE,
        )
        self.window.SetSizeLimits(minWidth=150,maxWidth=2000,minHeight=150,maxHeight=2000)
        #self.minsize(width=150, height=150)
        self.name = self.places[self.first].name
        self.desc = self.places[self.first].desc

        #self.columnconfigure([0], weight=1)
        #self.rowconfigure([1], weight=1)
        
        self.layout=BGridLayout()
        self.window.SetLayout(self.layout)

        self.menu_font = be_plain_font
        self.menu_font.SetSize(14)
        
        self.place_font = be_plain_font
        self.place_font.SetSize(22)
        
        self.desc_font = be_plain_font
        self.desc_font.SetSize(18)

        self.name_label = BStringView('name_label',self.name)
        self.name_label.SetFont(self.place_font)
        self.name_label.SetAlignment(B_ALIGN_CENTER)
        self.desc_label = BTextView('desc_label')
        self.desc_label.SetText(self.desc,None)
        self.desc_label.MakeEditable(False)
        self.desc_label.MakeSelectable(False)
        self.desc_label.SetFont(self.desc_font)
        self.desc_label.SetAlignment(B_ALIGN_CENTER)
        self.layout.AddView(self.name_label,0,0)
        self.layout.AddView(self.desc_label,0,1)
        #self.name_label.grid(column=0, row=0, padx=7, pady=7, sticky="ew")
        #self.desc_label.grid(column=0, row=1, padx=7, pady=7, sticky="nsew")

        self.menu_layout = BGridLayout()
        
        self.layout.AddItem(self.menu_layout,0,2)
        #self.menu_frame.grid(column=0, row=2, padx=7, pady=7, sticky="nsew")
        #self.menu_frame.columnconfigure([0], weight=1)

        #total_height = sum(
        #    widget.winfo_reqheight() + 5 for widget in self.winfo_children()
        #)
        #total_width = sum(
        #    widget.winfo_reqwidth() + 5 for widget in self.winfo_children()
        #)

        #self.minsize(width=total_width, height=total_height)

        # Menus
        self.open_menu = BPopUpMenu('Door')
        self.open_menufield = BMenuField(
            'Door',
            "Open",
            self.open_menu
        )
        self.open_menufield.SetFont(self.menu_font)
        self.menu_layout.AddView(self.open_menufield,0,0)
        #self.open_menubutton.grid(column=0, row=0, padx=7, pady=7)

        self.look_at_menu = BPopUpMenu('Thing')
        self.look_at_menufield = BMenuField(
            'Thing',
            "Look at",
            self.look_at_menu
        )
        self.look_at_menufield.SetFont(self.menu_font)
        self.menu_layout.AddView(self.look_at_menufield,0,1)
        #self.look_at_menubutton.grid(column=0, row=1, padx=7, pady=7)

        self.take_menu = BPopUpMenu('Thing')
        self.take_menufield = BMenuField(
            'Thing',
            "Take",
            self.take_menu
        )
        self.take_menufield.SetFont(self.menu_font)
        self.menu_layout.AddView(self.take_menufield,0,2)
        #self.take_menubutton.grid(column=0, row=2, padx=7, pady=7)

        self.gen_menus(self.places[self.current_room], True)

        
        self.window.Show()

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
        return bool(menu.FindItem(name))
        
    def gen_menus(self, thing, new=False):
        # current_place = self.places[self.first]
        if new:
            self.open_menu.RemoveItems(0, -1)
            self.look_at_menu.RemoveItems(0, -1)
            self.take_menu.RemoveItems(0, -1)
        if thing in self.places:
            if thing.desc and not self.is_in_menu(self.look_at_menu, "Surroundings"):
                msg=BMessage()
                self.window.events[msg]=lambda item=thing: self.look_at(item, surr=True)
                self.look_at_menu.AddItem(BMenuItem(
                    "Surroundings",
                    msg,
                    '\0',
                    0
                ))

        if thing.items:
            for item in thing.items:
                if (
                    isinstance(item, Thing)
                    and item.moveable
                    and not self.is_in_menu(self.take_menu, item.name)
                ):
                    #self.take_menu.add_command(
                    #    label=item.name,
                    #    command=lambda item=item: self.take_item(item, thing),
                    #)
                    msg=BMessage()
                    self.window.events[msg]=lambda item=item: self.take_item(item, thing)
                    self.take_menu.AddItem(BMenuItem(
                        item.name,
                        msg,
                        '\0',
                        0
                    ))
                if (item.desc or item.items) and not self.is_in_menu(
                    self.look_at_menu, item.name
                ):
                    #self.look_at_menu.add_command(
                    #    label=item.name, command=lambda item=item: self.look_at(item)
                    #)
                    msg=BMessage()
                    self.window.events[msg]=lambda item=item: self.look_at(item)
                    self.take_menu.AddItem(BMenuItem(
                        item.name,
                        msg,                          
                        '\0',
                        0
                    ))
                    
                # if self.menu.index("end") != 0:
                #    self.menu_frame.add_cascade(label=item.name, menu=self.menu)
        if thing.places:
            for place in thing.places:
                if not self.is_in_menu(self.open_menu, place.name):
                    #self.open_menu.add_command(
                    #    label=place.name,
                    #    command=lambda door=place: self.open_door(door),
                    #)
                    msg=BMessage()
                    self.window.events[msg]=lambda door=place: self.open_door(door)
                    self.open_menu.AddItem(BMenuItem(
                        place.name,
                        msg,                          
                        '\0',
                        0
                    ))
                if place.desc and not self.is_in_menu(self.look_at_menu, place.name):
                    #self.look_at_menu.add_command(
                    #    label=place.name, command=lambda item=place: self.look_at(item)
                    #)
                    msg=BMessage()
                    self.window.events[msg]=lambda item=place: self.look_at(item)
                    self.look_at_menu.AddItem(BMenuItem(
                        place.name,
                        msg,                          
                        '\0',
                        0
                    ))


if __name__ == "__main__":
    game = Game()
    game.Run()
