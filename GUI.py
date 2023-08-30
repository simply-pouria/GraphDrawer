import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import functions

ctk.set_appearance_mode("dark")


def drawing_info():
    info = functions.is_a_graph(textbox.get())
    if info == 'Enter the degree set of a graph in this form: 6,6,4,3,3,2,2' or info == ('The degree set does not '
                                                                                         'belong to a graph'):
        messagebox.showerror(title='wrong input', message=info)
    else:
        canvas.delete("all")
        functions.draw_graph(canvas,info)


# Drawing the UI using tk and Ctk
rt = tk.Tk()
rt.geometry('500x500')
rt.title('Graph Drawer')
rt.wm_iconbitmap("Graph Drawer.ico")

button = ctk.CTkButton(master=rt,
                       corner_radius=10,
                       command=drawing_info,
                       width=100,
                       height=40,
                       text='Draw!')

textbox = ctk.CTkEntry(master=rt,
                       corner_radius=10,
                       width=300,
                       height=40)

canvas = tk.Canvas(master=rt,
                   width=455,
                   height=400,
                   bg='Gray')


button.place(x=380, y=20)
textbox.place(x=20, y=20)
canvas.place(x=20, y=80)


rt.mainloop()
