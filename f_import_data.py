import random
from matplotlib import pyplot as plt
import cv2
import glob
from PIL import Image

def import_all_training(source, shuffle = False, img_size = 32):
    training_dataset = []
    Location = source[0]
    Frequency = source[1]
    Year = source[2]
    Month = source[3]
    #base_path = "C:/Users/Tom/OneDrive/Documents/50 University/Year 5/Individual Proj/Data/Final System Data/{}/{}/{}/{}/Sorted/".format(Location,Frequency,Year,Month)
    base_path = "C:/Users/tomjo/OneDrive/Documents/50 University/Year 5/Individual Proj/Data/Sorted/"
    
    # classes = ['Moon', 'Moon_Exposure', 'V_Cloudy', 'Cloudy', 'Almost_Clear', 'Clear', 'Speckle']
    # class_ids = [0,     1,              2,          3,         4,             5,        6]
    # classes = ['Moon', 'V_Cloudy', 'Cloudy', 'Almost_Clear', 'Clear', 'Speckle']
    # class_ids = [0,     1,          2,         3,             4,        5]

    classes = ['Moon', 'V_Cloudy', 'Cloudy', 'Almost_Clear', 'Clear', 'Speckle']
    class_ids = [0,     1,                2,          3,         4,             5]
    # classes = ['Moon', 'V_Cloudy', 'Cloudy', 'Almost_Clear', 'Clear']
    # class_ids = [0,     1,          1,         1,             1]

    i = 0
    for CLASS in classes:
        path = base_path + CLASS + '/*.gif'
        training_dataset = import_data(training_dataset,path,class_ids[i], compress_size= img_size)
        i += 1

    if shuffle:
        random.shuffle(training_dataset)

    return training_dataset

def import_data(dataset, path, class_idenfier, max = -1, compress_size = 32):
    counter = 0

    for filename in glob.glob(path): #assuming gif

        # Read image data
        img_array = plt.imread(filename)

        # Compress and flatten
        compressed_img = cv2.resize(img_array, dsize=(compress_size, compress_size))
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
        print(counter)

    return dataset

# ~~~ Function to import unlabelled images ~~~
def import_prediction(source, img_sz = 32):
    # unpack the data source information
    Location = source[0]
    Frequency = source[1]
    Year = source[2]
    Month = source[3]
    
    path = r"C:\Users\tomjo\OneDrive\Documents\50 University\Year 5\Individual Proj\Data\Final System Data\{}\{}\{}\{}\Unsorted\*.gif".format(Location,Frequency,Year,Month)
    data = []
    data = import_data(data,path,-1, compress_size= img_sz)
    return data


def import_all(max_quant):
    path = 'C:/Users/tomjo/OneDrive/Documents/50 University/Year 5/Individual Proj/Data/Unsorted/*.gif'
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