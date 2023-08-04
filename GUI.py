import tkinter as tk
import customtkinter as ctk
from functions import is_a_graph

ctk.set_appearance_mode("dark")


def drawing_info():
    info = is_a_graph(textbox.get())
    if info == 'Enter the degree set of a graph in this form: 6,6,4,3,3,2,2' or info == ('The degree set does not '
                                                                                         'belong to a graph'):
        label = tk.Label(master=rt,
                         text=info,
                         fg='red')

        label.place(x=20, y=63)


# Drawing the UI using tk and Ctk
rt = tk.Tk()
rt.geometry('500x500')
rt.title('Graph Drawer')

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
