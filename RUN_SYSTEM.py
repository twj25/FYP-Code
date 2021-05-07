from f_data_scraper import download_images
from GUI_image_sorter import run_GUI
from C_2D_CNN_newmodel import run_prediction_model

data_source = ["mercedes","5577","2020","Aug"]
#Location = "rio_grande"
#Location = "mcdonald"
#Location = "mercedes"
#Location = "sutherland"

download_images(data_source)
run_GUI(data_source)
run_prediction_model(data_source)