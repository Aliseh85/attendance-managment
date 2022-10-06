import tkinter as tk
from tkinter import *
import workers
import control
from PIL import ImageTk, Image


def which_button(w):
    if w == '1':
        tk.messagebox.showinfo("", "one second starting")
        control.savefaceimg()
    if w == '2':
        tk.messagebox.showinfo("", "it may take a while")
        control.savefaceencode()
    if w == '3':
        tk.messagebox.showinfo("", "going to check attendace")
        workers.start()


class BkgrFrame(tk.Frame):
    def __init__(self, parent, file_path, width, height):
        super(BkgrFrame, self).__init__(parent, borderwidth=0, highlightthickness=0)

        self.canvas = tk.Canvas(self, width=width, height=height)
        self.canvas.pack()

        pil_img = Image.open(file_path)
        self.img = ImageTk.PhotoImage(pil_img.resize((width, height), Image.ANTIALIAS))
        self.bg = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img)

    def add(self, widget, x, y):
        canvas_window = self.canvas.create_window(x, y, anchor=tk.NW, window=widget)
        return widget


if __name__ == '__main__':
    IMAGE_PATH = 'home.png'
    root = tk.Tk()
    width=root.winfo_screenwidth()
    height= root.winfo_screenheight()
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(),
                                       root.winfo_screenheight()))
    bkrgframe = BkgrFrame(root, IMAGE_PATH, root.winfo_screenwidth(), root.winfo_screenheight())
    bkrgframe.pack()

    # Put some tkinter widgets in the BkgrFrame.
    button1 = bkrgframe.add(tk.Button(root, text="check attendances", command=lambda m="3": which_button(m)), 1000, 10)
    button2 = bkrgframe.add(tk.Button(root, text="take picture",command=lambda m="1": which_button(m)), 1000, 40)
    button3 = bkrgframe.add(tk.Button(root, text="encode faces",command=lambda m="2": which_button(m)), 1000, 70)

    root.mainloop()
