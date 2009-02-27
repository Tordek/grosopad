#!/usr/bin/env python
#
#    Copyright 2009 Guillermo O. Freschi
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import glob
import user
import os
import os.path
import time
import Tkinter as tk
import tkFileDialog

base_path = os.path.join(user.home, '.grosopad')

class Note(object):
    def __init__(self, master, filename=None):
        self.master = master

        root = tk.Toplevel(master)
        text = tk.Text(root)
        text.pack(fill=tk.BOTH, expand=1)
        text.focus_set()

        root.bind("<Control-n>",
                  lambda e: Note(self.master))
        root.bind("<Control-d>",
                  lambda e: self.delete(filename))
        root.bind("<Control-q>",
                  lambda e: self.quit())
        root.bind("<Control-s>",
                  lambda e: self.save(text.get(1.0, tk.END)))

        text.bind("<Key>",
                  lambda e: self.save(text.get(1.0, tk.END), filename))

        self.window = root

        if filename is None:
            filename = os.path.join(base_path, str(time.time()))
        else:
            file = open(filename, "r")
            text.insert(tk.END, file.read())
            file.close()

    def quit(self):
        self.master.destroy()

    def delete(self, filename):
        if os.path.exists(filename):
            os.remove(filename)

        self.window.destroy()

        if not self.master.winfo_children():
            Note(self.master)

    def save(self, content, filename=None):
        if filename is None:
            filename = tkFileDialog.asksaveasfilename()

        file = open(filename, "w")
        file.write(content.encode('utf-8'))
        file.close()


def main():
    root = tk.Tk()
    root.withdraw()

    if not os.path.exists(base_path):
        os.mkdir(base_path)

    if glob.glob(os.path.join(base_path, '*')):
        for i in glob.glob(os.path.join(base_path, '*')):
            Note(root, i)
    else:
        Note(root)

    root.mainloop()


if __name__ == "__main__":
    main()
