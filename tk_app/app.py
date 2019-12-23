import tkinter as tk
#from PIL import ImageTk, Image
import os
import cv2
from tkinter import filedialog
from PIL import Image, ImageTk
from classifier import run_app_get_labels


START_IMG = r"imgs/descarga.png"
TEMPORAL_IMG_PATH = r"imgs/temporal20190812.png"

def create_temporal_image(path, size=(224,224) , 
							final_path=	TEMPORAL_IMG_PATH):
	img =  cv2.imread(path)
	img = cv2.resize(img, dsize=size, interpolation=cv2.INTER_CUBIC)
	# cv2.imsave(img, final_path)
	cv2.imwrite(final_path, img) 
class Window(tk.Tk):
	def __init__(self, *args, **kwargs):
		super(Window, self).__init__(*args, **kwargs)
		create_temporal_image(START_IMG, size=(224,224) , 
							final_path=	TEMPORAL_IMG_PATH)
		
		
		self.geometry("600x400")
		self.title("Dog App :D")
		
			
		self.main_frame = tk.Frame(self,padx = 10, pady=20)
		self.main_frame.pack()

		self.frameleftupper = tk.Frame(self.main_frame,padx= 20)
		self.frameleftupper.grid(row=1,  column=1)
		
		self.botonFile = tk.Button(self.frameleftupper,
								text = 'Open Image', width=25,command=self.update_img
								)
		self.botonFile.grid(row=1, column=1,pady=5)
		
		
		
		self.botonPrediction = tk.Button(self.frameleftupper, 
										text = 'Generate Prediction',
											width=25,
											command=lambda : self.update_label()
											)
		self.botonPrediction.grid(row=2, column=1,pady=5)


		self.framerightupper = tk.Frame(self.main_frame,padx= 20)
		self.framerightupper.grid(row=1,  column=2)
		#img = ImageTk.PhotoImage(Image.open(img_path))
		#panel = tk.Label(framerightupper, image = img)
		#img = tk.PhotoImage(file=TEMPORAL_IMG_PATH)
		self.labelImageupper = tk.Label(self.framerightupper , text= "")
		self.labelImageupper.grid(rows=1, column=1)
		
		#self.labelImagebottom = tk.Label(self.framerightupper , text= "test2")
		#self.labelImagebottom.grid(rows=3, column=1)
		
		self.labelImage = tk.Label(self.framerightupper)
		self.labelImage.grid(rows=2, column=1)
		
		#image = Image.open( TEMPORAL_IMG_PATH)
		#self.labelImage.img = ImageTk.PhotoImage( image,master = self.labelImage)
		self.labelImage.img = tk.PhotoImage(file=TEMPORAL_IMG_PATH,master = self.labelImage)
		self.labelImage.config(image=self.labelImage.img)
		
		self.labelPrediction = tk.Label(self.framerightupper,
								text="Open Image and then generate prediction",
								justify=tk.LEFT)
		self.labelPrediction.grid(row=3, column=1)

	def update_img(self):
		ftypes = [('jpg', '*.jpg'), ('png', '*.png'),('All files', '*')]
		file_name = filedialog.askopenfilename(initialdir = "",
											title = "Select file",
											filetypes = ftypes)	

		create_temporal_image(file_name, size=(224,224) , 
							final_path=	TEMPORAL_IMG_PATH)
		#img = tk.PhotoImage(file=file_name)
		#self.labelImage.configure( image=img)
		self.labelImage.img = tk.PhotoImage(file=TEMPORAL_IMG_PATH,master = self.labelImage)
		self.labelImage.config(image=self.labelImage.img)
				
		self.labelImageupper.config(text="Press the prediction  button!!")
		self.labelPrediction.config(text= "")
		
	def update_label(self):
		title , xlabel = run_app_get_labels(TEMPORAL_IMG_PATH)
		xlabel = xlabel.replace("_", " ").title()
		
		self.labelImageupper.config(text=title)
		self.labelPrediction.config(text= xlabel)
		
if __name__ == "__main__": 
		
	main = Window()
	main.mainloop()


		