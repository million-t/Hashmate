import tkinter as tk
from tkinter import ttk
from startPage import *



LARGEFONT =("Verdana", 35)

class tkinterApp(tk.Tk):
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		
		container = tk.Frame(self)
		container.pack(side = "top", fill = "both", expand = True)
		container.grid_rowconfigure(0, weight = 1)
		container.grid_columnconfigure(0, weight = 1)

		
		self.frames = {}
		for FrameTemplate in (StartPage, GeneratePage, ComparePage):
			frame = FrameTemplate(container, self)
			self.frames[FrameTemplate] = frame
			frame.grid(row = 0, column = 0, sticky ="nsew")

		self.show_frame(StartPage)

	
	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.tkraise()
    


app = tkinterApp()
app.wm_state('zoomed')
app.mainloop()
