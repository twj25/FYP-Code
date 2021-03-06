import requests
import os
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse


def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def get_all_images(url):
    """
    Returns all image URLs on a single `url`
    """
    soup = bs(requests.get(url).content, "html.parser")
    urls = []
    for img in tqdm(soup.find_all("img"), "Extracting images"):
        img_url = img.attrs.get("src")
        if not img_url:
            # if img does not contain src attribute, just skip
            continue
        # make the URL absolute by joining domain with the URL that is just extracted
        img_url = urljoin(url, img_url)
        # remove URLs like '/hsts-pixel.gif?c=3.2.5'
        try:
            pos = img_url.index("?")
            img_url = img_url[:pos]
        except ValueError:
            pass
        # finally, if the url is valid
        if is_valid(img_url):
            urls.append(img_url)
    return urls

def download(url, pathname, save_name):
    """
    Downloads a file given an URL and puts it in the folder `pathname`
    """
    # if path doesn't exist, make that path dir
    if not os.path.isdir(pathname):
        os.makedirs(pathname)
    # download the body of response by chunk, not immediately
    response = requests.get(url, stream=True)

    # get the total file size
    file_size = int(response.headers.get("Content-Length", 0))

    # get the file name
    save_name = save_name + '_' + url.split("/")[-1]
    filename = os.path.join(pathname, save_name)
    

    # progress bar, changing the unit to bytes instead of iteration (default by tqdm)
    progress = tqdm(response.iter_content(1024), f"Downloading {filename}", total=file_size, unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        for data in progress:
            # write data read to the file
            f.write(data)
            # update the progress bar manually
            progress.update(len(data))

def main(url, path, save_name):
    # get all images
    imgs = get_all_images(url)
    count = 0
    for img in imgs:
        if count % 2 == 0:
            # download every other image
            download(img, path, save_name)
        count += 1
    
def download_images(Location, Year, Frequency):
    # call a function to return a list of urls
    path = r"C:\Users\tomjo\OneDrive\Documents\50 University\Year 5\Individual Proj\Data\Unsorted"

    months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

    for month in months:
        for day in range(30):
            print("Month:", month, "  Day:", day)
            #baseurl = "http://sirius.bu.edu/data/?location=rio_grande&year=2020&filt=5577"
            baseurl = 'http://sirius.bu.edu/data/?location=' + Location + '&year=' + Year + '&filt=' + Frequency
            url = baseurl + "&month=" + month + "&day=" + str(day)

            save_name = Location + '_' + Frequency + '_' + str(day) + '_' + month + '_' + Year
            main(url, path, save_name)

    # loop and download all images
    #url = "http://sirius.bu.edu/data/?location=arecibo&year=2017&filt=6300&month=Jun&day=22"
    

#Location = "rio_grande"
#Location = "mcdonald"
Location = "mercedes"
#Location = "sutherland"
Year = '2020'
Frequency = '5577'
download_images(Location,Year,Frequency)