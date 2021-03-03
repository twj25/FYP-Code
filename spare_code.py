
# Code to display a .gif image
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