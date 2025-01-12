from tkinter import Toplevel,Tk, Frame, Label

'''
Class represents the pop up window that provides the status message
'''
class pop_up_window(Toplevel):

	def __init__(self,pop_up_message: str ='', pop_up_title: str = '',pop_up_message_title:str='',*args, **kwargs):
		super().__init__(*args, **kwargs)

		# Get the screen width and height
		screen_width = self.winfo_screenwidth()
		screen_height = self.winfo_screenheight()

		# Calculate the x and y coordinates for the window to be centered
		x = (screen_width - 700) // 2
		y = (screen_height - 400) // 2

		# Set the window's position
		self.geometry(f"+{x}+{y}")

		self.configure(relief='raised')
		self.frame = Frame(self)
		self.message = pop_up_message
		self.pop_up_title = pop_up_message
		self.top_title_label = Label(master=self.frame,text=pop_up_message_title,justify='center')
		self.message_label = Label(master=self.frame,text=pop_up_message,justify='left')
		self.title(pop_up_title)
		self.message_label.place(relx=.5, rely=.5, anchor="w")
		self.top_title_label.pack(side='top')
		self.message_label.pack()
		self.frame.pack()

	def set_window_title(self, title_in: str) -> None:
		'''
		Set the title of the actual window
		:param title_in: @str the title of the window
		:return: @None
		'''
		self.title(title_in)

	def set_message_title(self,message_title_in: str) -> None:
		'''
		Set the message title of the label located in the frame of the Tk instance
		:param message_title_in: @str title located in the frame of the window
		:return: @None
		'''
		self.top_title_label.configure(text=message_title_in)

	def set_message(self,message_in: str) -> None:
		'''
		Sets the message displayed by the status window
		:param message_in: @str the message located in the status window
		:return: @None
		'''
		self.message_label.configure(text=message_in)

# Designed, Written, and Tested By Ramzi Reilly Adil