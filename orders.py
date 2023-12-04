import tkinter as tk
from tkinter import ttk
import tksheet

import requests
from ctypes import windll

windll.shcore.SetProcessDpiAwareness(1)
data = requests.get("http://localhost:8000/orders/").json()
frames = {}


class TopBar(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.add = ttk.Button(self, text="Add", command=lambda: controller.show_frame("AddPage"))
        self.compose()

    def compose(self):
        self.columnconfigure(0, weight=1)
        self.add.pack(fill=tk.BOTH, expand=1)
        self.pack(side=tk.TOP, fill=tk.X)


class SideBar(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.lists = tk.Listbox(self, width=20)
        self.compose()

    def compose(self):
        self.lists.pack(side=tk.LEFT, fill=tk.BOTH, expand=0)
        self.lists.insert(tk.END, *[x["title"] for x in data])
        self.pack(side=tk.LEFT, fill=tk.Y)


class MainView(tk.Frame):
    def __init__(self, parent, onchange=None):
        tk.Frame.__init__(self, parent)
        self.save_button = None
        self.id = tk.IntVar()
        self.id.trace("w", lambda *args: self.id_changed())
        self.title = tk.StringVar()
        self.owner = tk.IntVar()
        self.status = tk.StringVar()
        self.sheet = tksheet.Sheet(
            self,
            headers=["id", "title", "description", "price", "quantity"],
            height=200,
        )
        self.onchange = onchange if onchange is not None else lambda: None
        self.compose()

    def id_changed(self):
        if self.id.get() == 0:
            self.save_button["text"] = "Add"
        else:
            self.save_button["text"] = "Save"

    def compose(self):
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=3)
        ttk.Label(self, text="ID :").grid(
            row=0, column=0, sticky=tk.W)
        ttk.Entry(self, textvariable=self.id, state=tk.DISABLED).grid(
            row=0, column=1, sticky=tk.EW)
        ttk.Label(self, text="Name :").grid(
            row=1, column=0, sticky=tk.W)
        ttk.Entry(self, textvariable=self.title).grid(
            row=1, column=1, sticky=tk.EW)
        ttk.Label(self, text="Owner :").grid(
            row=2, column=0, sticky=tk.W)
        ttk.Entry(self, textvariable=self.owner).grid(
            row=2, column=1, sticky=tk.EW)
        ttk.Label(self, text="Status :").grid(
            row=3, column=0, sticky=tk.W
        )
        ttk.Combobox(
            self,
            textvariable=self.status,
            values=["carted", "invoiced", "paid", "pending", "shipped", "cancelled"],
            state="readonly",
        ).grid(row=3, column=1, sticky=tk.EW)
        ttk.Label(self, text="Items :").grid(
            row=4, column=0, sticky=tk.W
        )
        self.sheet.grid(
            row=5, column=0, columnspan=2, sticky=tk.NSEW
        )
        self.save_button = ttk.Button(self, text="Add", command=self.save)
        self.save_button.grid(
            row=6, column=0, columnspan=2, sticky=tk.EW
        )
        self.pack(side=tk.RIGHT, fill=tk.BOTH, expand=15)

    def set_data(self, data):
        self.id.set(data["id"])
        self.title.set(data["title"])
        self.owner.set(data["owner_id"])
        self.status.set(data["status"])

    def set_items(self, items):
        self.sheet.set_sheet_data([[x["id"], x["title"], x["description"], x["price"], x["quantity"]] for x in items])

    def save(self):
        pass


class AddPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.back = ttk.Button(self, text="Add", command=lambda: controller.show_frame("AddPage"))
        self.compose()

    def compose(self):
        self.back.pack(side=tk.TOP, fill=tk.X)
        # self.columnconfigure(0, weight=1)
        # self.pack(side=tk.TOP, fill=tk.BOTH, expand=1)


class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        t = TopBar(self, controller)
        t.add.configure(command=self.add_new)
        self.side = SideBar(self)
        self.view = MainView(self, onchange=self.update)
        self.side.lists.bind("<<ListboxSelect>>", self.onselect)

    def update(self):
        self.side.lists.delete(0, tk.END)
        self.side.lists.insert(tk.END, *[x["title"] for x in data])

    def add_new(self):
        self.view.set_data({
            "id": 0,
            "title": "",
            "owner_id": 0
        })
        self.side.lists.select_clear(0, tk.END)
        self.view.set_items([])

    def onselect(self, evt):
        w = evt.widget
        index = int(w.curselection()[0])
        self.view.set_data(data[index])
        item = requests.get("http://127.0.0.1:8000/orders/" + str(self.view.id.get())).json()
        self.view.set_items(item["order_items"])


class MainApp:
    def __init__(self, parent):
        self.root = parent
        self.root.title("Orders")
        self.root.geometry("850x600+0+0")
        self.root.resizable(False, False)
        container = tk.Frame(self.root)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (MainPage,):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


if __name__ == "__main__":
    root = tk.Tk()
    obj = MainApp(root)
    root.mainloop()
