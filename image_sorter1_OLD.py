import tkinter as tk
import os
class Layout(tk.Frame):

    def __init__(self, current_file):
        super().__init__()
        self.current_file = current_file
        self.initUI()

    def initUI(self):

        self.master.title("Image Sorter")
        #tk.Style().configure("TButton", padding(0,5,5,5,5))

        self.columnconfigure(0, pad=3)
        self.columnconfigure(1, pad=3)
        self.columnconfigure(2, pad=3)
        self.columnconfigure(3, pad=3)
        self.columnconfigure(4, pad=4)

        self.rowconfigure(0, pad=3)
        self.rowconfigure(1, pad=3)

        photo = tk.PhotoImage(file = self.current_file)
        label = tk.Label(image = photo)
        label.grid(row=0, columnspan=5)

        btn_moon = tk.Button(
            text="Moon Cover",
            width=25,
            height=5,
            bg="blue",
            fg="yellow",
            command = self.class_moon
        )
        btn_moon.grid(row=1, column=0)

        btn_cloud_heavy = tk.Button(
            text="Heavy Cloud",
            width=25,
            height=5,
            bg="yellow",
            fg="blue",
            command = self.class_cloud_heavy
        )
        btn_cloud_heavy.grid(row=1, column=2)

        #self.pack()

    def class_moon():
        pass
        return 
    
    def class_cloud_heavy():
        pass
        return


unsorted_path = "C:/Users/tomjo/OneDrive/Documents/50 University/Year 5/Individual Proj/Data/Test/"
unsorted_files = os.listdir(unsorted_path)
unsorted_count = 0
current_file = unsorted_path + unsorted_files[unsorted_count]

window = tk.Tk()
app = Layout(current_file)
window.mainloop()