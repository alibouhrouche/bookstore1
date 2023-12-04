import tkinter as tk
from tkinter import ttk

import requests
from ctypes import windll

windll.shcore.SetProcessDpiAwareness(1)
data = {
    "customers": requests.get("http://localhost:8000/customers/?skip=0&limit=100").json()["customers"]
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
        self.label = tk.Label(self, text="Customers")
        self.compose()

    def compose(self):
        self.lists.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.lists.insert(tk.END, *[x["name"] for x in data["customers"]])
        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)


class MainView(tk.Frame):
    def __init__(self, parent, onchange=None):
        tk.Frame.__init__(self, parent)
        self.save_button = None
        self.id = tk.IntVar()
        self.id.trace("w", lambda *args: self.id_changed())
        self.name = tk.StringVar()
        self.email = tk.StringVar()
        self.phone = tk.StringVar()
        self.address = tk.StringVar()
        self.orders = tk.IntVar()
        self.status = tk.BooleanVar()
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
        ttk.Entry(self, textvariable=self.name).grid(
            row=1, column=1, sticky=tk.EW)
        ttk.Label(self, text="Email :").grid(
            row=2, column=0, sticky=tk.W)
        ttk.Entry(self, textvariable=self.email).grid(
            row=2, column=1, sticky=tk.EW)
        ttk.Label(self, text="Phone :").grid(
            row=3, column=0, sticky=tk.W)
        ttk.Entry(self, textvariable=self.phone).grid(
            row=3, column=1, sticky=tk.EW)
        ttk.Label(self, text="Address :").grid(
            row=4, column=0, sticky=tk.W)
        ttk.Entry(self, textvariable=self.address).grid(
            row=4, column=1, sticky=tk.EW)
        ttk.Label(self, text="Orders :").grid(
            row=5, column=0, sticky=tk.W)
        ttk.Entry(self, textvariable=self.orders).grid(
            row=5, column=1, sticky=tk.EW)
        ttk.Label(self, text="Status :").grid(
            row=6, column=0, sticky=tk.W
        )
        ttk.Checkbutton(self, text="Active", variable=self.status).grid(
            row=6, column=1, sticky=tk.EW
        )
        self.save_button = ttk.Button(self, text="Add", command=self.save)
        self.save_button.grid(
            row=7, column=0, columnspan=2, sticky=tk.EW
        )
        self.pack(side=tk.RIGHT, fill=tk.BOTH, expand=10)

    def set_data(self, data):
        self.id.set(data["id"])
        self.name.set(data["name"])
        self.email.set(data["email"])
        self.phone.set(data["phone"])
        self.address.set(data["address"])
        self.orders.set(data["orders"])
        self.status.set(data["status"] == "active")

    def save(self):
        if self.save_button["text"] == "Add":
            ret = requests.post(
                "http://127.0.0.1:8000/customers/",
                json={
                    "name": self.name.get(),
                    "email": self.email.get(),
                    "phone": self.phone.get(),
                    "address": self.address.get(),
                    "orders": self.orders.get(),
                    "status": "active" if self.status.get() else "inactive"
                }
            )
            data["customers"].append(ret.json()["customer"])
        else:
            for i in range(len(data["customers"])):
                if data["customers"][i]["id"] == self.id.get():
                    data["customers"][i] = requests.put(
                        "http://127.0.0.1:8000/customers/" + str(self.id.get()),
                        json={
                            "name": self.name.get(),
                            "email": self.email.get(),
                            "phone": self.phone.get(),
                            "address": self.address.get(),
                            "orders": self.orders.get(),
                            "status": "active" if self.status.get() else "inactive"
                        }
                    ).json()["customer"]
        self.onchange()


class MainPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Customers")
        self.root.geometry("800x600+0+0")
        self.root.resizable(False, False)
        t = TopBar(self.root)
        t.add.configure(command=self.add_new)
        self.side = SideBar(self.root)
        self.view = MainView(self.root, onchange=self.update)
        self.side.lists.bind("<<ListboxSelect>>", self.onselect)

    def update(self):
        self.side.lists.delete(0, tk.END)
        self.side.lists.insert(tk.END, *[x["name"] for x in data["customers"]])

    def add_new(self):
        self.view.set_data({
            "id": 0,
            "name": "",
            "email": "",
            "phone": "",
            "address": "",
            "orders": 0,
            "status": "active"
        })
        self.side.lists.select_clear(0, tk.END)

    def onselect(self, evt):
        w = evt.widget
        index = int(w.curselection()[0])
        self.view.set_data(data["customers"][index])


if __name__ == "__main__":
    root = tk.Tk()
    obj = MainPage(root)
    root.mainloop()
