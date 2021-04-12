import random
from matplotlib import pyplot as plt
import cv2
import glob
from PIL import Image

def import_all_training(shuffle = False):
    training_dataset = []
    base_path = 'C:/Users/Tom/OneDrive/Documents/50 University/Year 5/Individual Proj/Data/Sorted/'
    classes = ['Moon', 'Moon_Exposure', 'V_Cloudy', 'Cloudy', 'Almost_Clear', 'Clear', 'Speckle']
    class_id = 0

    for CLASS in classes:
        path = base_path + CLASS + '/*.gif'
        training_dataset = import_data(training_dataset,path,class_id)
        class_id += 1

    if shuffle:
        random.shuffle(training_dataset)

    return training_dataset

def import_data(dataset, path, class_idenfier, max = -1):
    counter = 0

    for filename in glob.glob(path): #assuming gif

        # Read image data
        img_array = plt.imread(filename)

        # Compress and flatten
        compressed_img = cv2.resize(img_array, dsize=(64, 64))
        #compressed_img = compressed_img.flatten()

        # Assign class identifier as the first digit of each line
        # -1 = unsupervised learning, therefore don't add identifier
        if class_idenfier == -1:
            training_array = [filename.split("\\")[-1], compressed_img]
            dataset.append(training_array)
        # else = supervised learning, therefore add identifier
        else:
            training_array= [class_idenfier,compressed_img]
            dataset.append(training_array)

        # This break allows a maximum quantity of data to be set
        counter += 1
        if counter == max:
            break

    return dataset

def import_all(max_quant):
    path = 'C:/Users/Tom/OneDrive/Documents/50 University/Year 5/Individual Proj/Data/Unsorted/*.gif'
    training_dataset = []
    # Import all data, -1 tells function not to add a class identifier to each entry
    training_dataset = import_data(training_dataset,path,-1, max=max_quant)
    return training_dataset

def check_dataset_entry(dataset, entry):
    # Print Lable
    print(dataset[entry][0])

    # Show image
    img_array = dataset[entry][1]
    img = Image.fromarray(img_array, 'L')
    img.save('test.png')
    img.show()
    return