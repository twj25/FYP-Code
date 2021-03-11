from C_2D_CNN import CNN
from csv import reader
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image

with open('TrainingSet.csv', 'r') as read_obj:
    # pass the file object to reader() to get the reader object
    csv_reader = reader(read_obj)
    # Pass reader object to list() to get a list of lists
    training_data = list(csv_reader)

testimage = training_data[0][1]
testimage = np.array(testimage)
testimage = testimage.reshape(64,64)

# Show image
#img_array = plt.imread("T072142A269_.gif")
# img_array = testimage
# img = Image.fromarray(img_array, 'L')
# img.save('test.png')
# img.show()

newCNN = CNN(0.5,[64,128],128,'relu')
newCNN.load_evaluation_data(training_data, 80)
score = newCNN.CNN_evaluate()
score = score * 100.0
print(score)