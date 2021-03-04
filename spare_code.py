
# ------------ Code to display a .gif image
test = Image.fromarray(res, 'L')
test.save('test.png')
test2 = Image.fromarray(img_array, 'L')
test2.save('test2.png')
test2.show()
test.show()

img_array = plt.imread("T072142A269_.gif")
img = Image.fromarray(img_array, 'L')
img.save('test.png')
img.show()


# ------------- Code for GUI
#frame1 = tk.Frame(master=window, width=100, height=100, bg="blue")

label.grid(row=0, column=1, sticky="nsew")

#frame2 = tk.Frame(master=window, width=50, height=50, bg="yellow")
window.rowconfigure(0, minsize=50, weight=3)
window.columnconfigure([0, 1, 2], minsize=50, weight=1)

#button1.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
btn_moon.grid(row=0, column=0, sticky="nsew")

frame3 = tk.Frame(master=window, width=50, height=50, bg="yellow")

#button2.pack(fill=tk.BOTH, side=tk.RIGHT, expand=True)