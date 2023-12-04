import tkinter as tk
from tkinter import ttk

import requests
from ctypes import windll

windll.shcore.SetProcessDpiAwareness(1)
data = {
    "items": requests.get("http://localhost:8000/inventory/?skip=0&limit=100").json()["items"]
}


class TopBar(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.add = ttk.Button(self, text="Add")
        self.compose()

    def compose(self):
        self.columnconfigure(0, weight=1)
        self.add.pack(fill=tk.BOTH, expand=1)
        self.pack(side=tk.TOP, fill=tk.X)


class SideBar(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.lists = tk.Listbox(self)
        self.compose()

    def compose(self):
        self.lists.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.lists.insert(tk.END, *[x["title"] for x in data["items"]])
        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)


class MainView(tk.Frame):
    def __init__(self, parent, onchange=None):
        tk.Frame.__init__(self, parent)
        self.save_button = None
        self.id = tk.IntVar()
        self.id.trace("w", lambda *args: self.id_changed())
        self.title = tk.StringVar()
        self.description = tk.StringVar()
        self.price = tk.IntVar()
        self.stock = tk.IntVar()
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
        ttk.Label(self, text="Title :").grid(
            row=1, column=0, sticky=tk.W)
        ttk.Entry(self, textvariable=self.title).grid(
            row=1, column=1, sticky=tk.EW)
        ttk.Label(self, text="Description :").grid(
            row=2, column=0, sticky=tk.W)
        ttk.Entry(self, textvariable=self.description).grid(
            row=2, column=1, sticky=tk.EW)
        ttk.Label(self, text="Price :").grid(
            row=3, column=0, sticky=tk.W)
        ttk.Entry(self, textvariable=self.price).grid(
            row=3, column=1, sticky=tk.EW)
        ttk.Label(self, text="Stock :").grid(
            row=4, column=0, sticky=tk.W)
        ttk.Entry(self, textvariable=self.stock).grid(
            row=4, column=1, sticky=tk.EW)
        self.save_button = ttk.Button(self, text="Add", command=self.save)
        self.save_button.grid(
            row=6, column=0, columnspan=2, sticky=tk.EW
        )
        self.pack(side=tk.RIGHT, fill=tk.BOTH, expand=10)

    def set_data(self, data):
        self.id.set(data["id"])
        self.title.set(data["title"])
        self.description.set(data["description"])
        self.price.set(data["price"])
        self.stock.set(data["stock"])

    def save(self):
        if self.save_button["text"] == "Add":
            ret = requests.post(
                "http://127.0.0.1:8000/inventory/",
                json={
                    "title": self.title.get(),
                    "description": self.description.get(),
                    "price": self.price.get(),
                    "stock": self.stock.get()
                }
            )
            data["items"].append(ret.json()["items"])
            self.onchange()
        else:
            for i in range(len(data["items"])):
                if data["items"][i]["id"] == self.id.get():
                    data["items"][i] = requests.put(
                        "http://127.0.0.1:8000/inventory/" + str(self.id.get()),
                        json={
                            "title": self.title.get(),
                            "description": self.description.get(),
                            "price": self.price.get(),
                            "stock": self.stock.get()
                        }
                    ).json()["items"]
        self.onchange()


class MainPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory")
        self.root.geometry("800x600+0+0")
        self.root.resizable(False, False)
        t = TopBar(self.root)
        t.add.configure(command=self.add_new)
        self.side = SideBar(self.root)
        self.view = MainView(self.root, onchange=self.update)
        self.side.lists.bind("<<ListboxSelect>>", self.onselect)

    def update(self):
        self.side.lists.delete(0, tk.END)
        self.side.lists.insert(tk.END, *[x["title"] for x in data["inventory"]])

    def add_new(self):
        self.view.set_data({
            "id": 0,
            "title": "",
            "description": "",
            "price": 0,
            "stock": 0
        })
        self.side.lists.select_clear(0, tk.END)

    def onselect(self, evt):
        w = evt.widget
        index = int(w.curselection()[0])
        self.view.set_data(data["items"][index])


if __name__ == "__main__":
    root = tk.Tk()
    obj = MainPage(root)
    root.mainloop()
