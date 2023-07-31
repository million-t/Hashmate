import tkinter as tk
from tkinter import ttk
import hashlib
import os
import tkinter as tk
from tkinter import filedialog, messagebox
# from PIL import Image, ImageTk

LARGEFONT =("Verdana", 35)


class StartPage(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
			
		menu_frame = ttk.Frame(self)
		menu_frame.grid(row = 0, column = 0, padx = 20, pady = 2, sticky='n')

		middle_frame = ttk.Frame(self)
		middle_frame.grid(row = 0, column = 1, padx = 20, pady = 2)

		button1 = ttk.Button(menu_frame, text ="Generate Hash",
		command = lambda : controller.show_frame(GeneratePage), width=20)
		button1.grid(row = 1, column = 1, padx = 20, pady = 2)


		button2 = ttk.Button(menu_frame, text ="Compare Hash",
		command = lambda : controller.show_frame(ComparePage), width=20)
		button2.grid(row = 2, column = 1, padx = 20, pady = 2)

		
		label = tk.Label(middle_frame, text="HashMate", font=('Verdana', 45))
		label.grid( row=0, column=1, padx = 60, pady = 80)


class ComparePage(tk.Frame):
	def __init__(self, parent, controller):
		self.hash_algorithms = ["md5", "md5", "sha1", "sha256", "sha512"]
		self.selected = tk.StringVar()
		self.selected.set(self.hash_algorithms[0])
		self.filepath = tk.StringVar()
		self.computed_hash = tk.StringVar()
		self.input_hash = tk.StringVar()
		self.hash_file_path = tk.StringVar()
		self.status = tk.StringVar()
		
		
		tk.Frame.__init__(self, parent)

		menu_frame = ttk.Frame(self)
		menu_frame.grid(row = 0, column = 0, padx = 20, pady = 2, sticky='n')

		middle_frame = ttk.Frame(self)
		middle_frame.grid(row = 0, column = 1, padx = 20, pady = 2)

		label = ttk.Label(middle_frame, text ="Compare Hash", font = ([LARGEFONT[0], 25]))
		label.grid(row = 0, column = 4, padx = 10, pady = 20)

		button1 = ttk.Button(menu_frame, text ="Generate Hash",
							command = lambda : controller.show_frame(GeneratePage), width=20)

		button1.grid(row = 1, column = 1, padx = 20, pady = 2)


		button2 = ttk.Button(menu_frame, text ="Home",
							command = lambda : controller.show_frame(StartPage), width=20)
	

		button2.grid(row = 2, column = 1, padx = 20, pady = 2)

		topFrame = ttk.Frame(middle_frame)
		topFrame.grid(row=2, column=4)
		algorithm_label = ttk.Label(topFrame, text="Select Hash Algorithm:")
		algorithm_label.grid(row=1, column=4, padx=10, pady=2, sticky=tk.E)
		algorithm_menu = ttk.OptionMenu(topFrame, self.selected, *self.hash_algorithms)
		algorithm_menu.grid(row=1, column=5, pady=2, sticky="w")

		file_label = ttk.Label(topFrame, text="Select File:")
		file_label.grid(row=2, column=4, padx=10, pady=2, sticky=tk.E)
		file_entry = ttk.Entry(topFrame, textvariable=self.filepath, width=50)
		file_entry.grid(row=2, column=5, padx=10, pady=2, sticky="w")
		file_button = ttk.Button(topFrame, text="Browse", command=self.browse_file)
		file_button.grid(row=2, column=6, padx=10, pady=2, sticky="w")

		hash_label = ttk.Label(topFrame, text="Select Hash File:")
		hash_label.grid(row=3, column=4, padx=10, pady=2, sticky=tk.E)
		hash_entry = ttk.Entry(topFrame, textvariable=self.input_hash, width=50)
		hash_entry.grid(row=3, column=5, padx=10, pady=2, sticky="w")
		hash_button = ttk.Button(topFrame, text="Browse", command=self.browse_hash_file)
		hash_button.grid(row=3, column=6, padx=10, pady=2, sticky="w")

		compute_button = ttk.Button(middle_frame, text="Verify Hash", command=self.compare_hashes)
		compute_button.grid(row=3, column=4, padx=10, pady=10, sticky="w")
	
		status_label = ttk.Label(middle_frame, text="Status:")
		status_label.grid(row=9, column=3, padx=10, pady=10, sticky=tk.E)
		self.status_entry = ttk.Entry(middle_frame, textvariable=self.status, width=50)
		self.status_entry.grid(row=9, column=4, padx=2, pady=10, sticky="w")

	def browse_file(self):
		"""Open a file dialog and set the file path variable to the selected file."""
		filepath = filedialog.askopenfilename()
		if filepath:
			self.filepath.set(filepath)
	
	def browse_hash_file(self):
		"""Open a file dialog and set the file path variable to the selected file."""
		
		filetypes = [("Text Files", "*.txt")]
		filepath = filedialog.askopenfilename(filetypes=filetypes)
		if filepath:
			self.input_hash.set(filepath)
	

	
	def compare_hashes(self):
		
		try:
			computed_hash = self.compute_hash()
			if not computed_hash:
				self.status.set("ERROR: No hash value computed.")
				self.status_entry.config(foreground='black')
				return
			
			with open(self.input_hash.get(), "r") as f:
				expected_hash = f.read().strip()
				if computed_hash == expected_hash:
					self.status.set("Hash values match.")
					self.status_entry.config(foreground='green')
		
				else:
					self.status.set("Hash values do not match.")
					self.status_entry.config(foreground='red')
		except Exception as e:
			self.status.set(f"ERROR: Failed to Compare hashes. {e}")
			self.status_entry.config(foreground='black')
			
		
	


	def compute_hash(self):
		"""Compute the hash value of the selected file using the selected hash algorithm."""
		filepath = self.filepath.get()
		if not os.path.exists(filepath):
			self.status.set("ERROR: File not found.")
			return None
        
		hash_algorithm = self.selected.get()
		try:
			with open(filepath, "rb") as f:
				data = f.read()
				hash_object = hashlib.new(hash_algorithm)
				hash_object.update(data)
				self.computed_hash.set(hash_object.hexdigest())
				self.status.set("Hash value computed successfully.")
				return self.computed_hash.get()
			
		except Exception as e:
			self.status.set(f"ERROR: Failed to compute hash value. {e}")
			self.computed_hash.set("")
			return None

class GeneratePage(tk.Frame):
	def __init__(self, parent, controller):
		self.hash_algorithms = ["md5", "md5", "sha1", "sha256", "sha512"]
		self.selected = tk.StringVar()
		self.selected.set(self.hash_algorithms[0])
		self.filepath = tk.StringVar()
		self.computed_hash = tk.StringVar()
		self.hash_file_path = tk.StringVar()
		self.status = tk.StringVar()
		
		tk.Frame.__init__(self, parent)

		menu_frame = ttk.Frame(self)
		menu_frame.grid(row = 0, column = 0, padx = 20, pady = 2, sticky='n')

		middle_frame = ttk.Frame(self)
		middle_frame.grid(row = 0, column = 1, padx = 20, pady = 2)
		right_frame = ttk.Frame(self)
		right_frame.grid(row = 0, column = 2, padx = 20, pady = 2)
        
		
		label = ttk.Label(middle_frame, text ="Generate Hash", font = ([LARGEFONT[0], 25]))
		label.grid(row = 0, column = 1, padx = 10, pady = 20)
		button1 = ttk.Button(menu_frame, text ="Home", command = lambda : controller.show_frame(StartPage), width=20)
		button1.grid(row = 1, column = 1, padx = 20, pady = 2)
		
		
		button2 = ttk.Button(menu_frame, text ="Compare Hash", command = lambda : controller.show_frame(ComparePage), width=20)
		button2.grid(row = 2, column = 1, padx = 20, pady = 2)
		
		
		algorithm_label = ttk.Label(middle_frame, text="Select Hash Algorithm:")
		algorithm_label.grid(row=1, column=0, padx=10, pady=2, sticky=tk.E)
		algorithm_menu = ttk.OptionMenu(middle_frame, self.selected, *self.hash_algorithms)
		algorithm_menu.grid(row=1, column=1, pady=2, sticky="w")

		file_label = ttk.Label(middle_frame, text="Select File:")
		file_label.grid(row=2, column=0, padx=10, pady=2, sticky=tk.E)
		file_entry = ttk.Entry(middle_frame, textvariable=self.filepath, width=50)
		file_entry.grid(row=2, column=1, padx=10, pady=2, sticky="w")
		file_button = ttk.Button(middle_frame, text="Browse", command=self.browse_file, width=20)
		file_button.grid(row=2, column=2, padx=10, pady=2, sticky="w")

		compute_button = ttk.Button(middle_frame, text="Compute Hash Value", command=self.compute_hash, width=20)
		compute_button.grid(row=3, column=2, padx=10, pady=20, sticky="w")


		self.hash_display = tk.Text(right_frame, width=50)
		self.hash_display.grid(row=0, column=0,padx=10, pady=10, sticky=tk.E)



		status_label = ttk.Label(middle_frame, text="Status:")
		status_label.grid(row=6, column=0, padx=10, pady=35, sticky=tk.E)
		self.status_entry = ttk.Entry(middle_frame, textvariable=self.status, width=50)
		self.status_entry.grid(row=6, column=1, padx=10, pady=35, sticky="w")

		generate_label = ttk.Label(middle_frame, text="Hash Save Directory:")
		generate_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")
		generate_entry = ttk.Entry(middle_frame, textvariable=self.hash_file_path, width=50)
		generate_entry.grid(row=4, column=1, padx=10, pady=10, sticky="w")
		generate_path = ttk.Button(middle_frame, text="Browse", command=self.browse_directory, width=20)
		generate_path.grid(row=4, column=2, padx=10, pady=10, sticky="w")
		generate_button = ttk.Button(middle_frame, text="Save", command=self.generate_hash_file, width=20)
		generate_button.grid(row=5, column=2, padx=10, pady=2, sticky="w")


	
	def browse_file(self):
		"""Open a file dialog and set the file path variable to the selected file."""
		filepath = filedialog.askopenfilename()
		if filepath:
			self.filepath.set(filepath)
	

	def browse_directory(self):
		"""Open a file dialog and set the hash file path variable to the selected directory."""
		filepath = self.filepath.get()
		if not os.path.exists(filepath):
			self.status.set("ERROR: File not found/selected.")
			self.status_entry.config(foreground='red')

			return 
		
		directory = filedialog.askdirectory()
		if directory:
			file_name = filepath.split('/')[-1]
			suffix = 1
			new_file_name = file_name

			# Check if the file exists
			while os.path.exists(f"{directory}/{new_file_name}.txt"):

				new_file_name = f"{file_name}{suffix}"
				suffix += 1


			self.hash_file_path.set(os.path.join(directory, new_file_name + ".txt"))


	def compute_hash(self):
		"""Compute the hash value of the selected file using the selected hash algorithm."""
		filepath = self.filepath.get()
		if not os.path.exists(filepath):
			self.status.set("ERROR: File not found.")
			self.status_entry.config(foreground='red')

			return None
        
		hash_algorithm = self.selected.get()
		try:
			with open(filepath, "rb") as f:
				data = f.read()
				hash_object = hashlib.new(hash_algorithm)
				hash_object.update(data)
				self.computed_hash.set(hash_object.hexdigest())
				self.hash_display.delete("1.0", tk.END)
				self.hash_display.insert(tk.END, self.computed_hash.get())
				self.status.set("Hash value computed successfully.")
				self.status_entry.config(foreground='green')

				return self.computed_hash.get()
			
		except Exception as e:
			self.status.set(f"ERROR: Failed to compute hash value. {e}")
			self.status_entry.config(foreground='red')

			self.computed_hash.set("")
			return None
		
	def generate_hash_file(self):
		"""Generate a hash file for the selected file."""
		original_file = self.filepath.get()
		
		if not os.path.exists(original_file):
			self.status.set("ERROR: File not found.")
			self.status_entry.config(foreground='red')

			return
        
		hash_file_path = self.hash_file_path.get()
		try:
			with open(hash_file_path, "w") as f:
				hash_value = self.compute_hash()
				if hash_value:
					f.write(hash_value)
					self.status.set("Hash file generated successfully.")
					self.status_entry.config(foreground='green')

				
		except Exception as e:
			self.status.set(f"ERROR: Failed to generate hash file. {e}")
			self.status_entry.config(foreground='red')

	