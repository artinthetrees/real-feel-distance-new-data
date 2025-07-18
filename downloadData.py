import requests
import os

##########################################################################
# define utility functions
# https://medium.com/@armaansinghbhau8/automate-file-downloads-from-urls-with-python-a-simple-guide-9a98cde10095
##########################################################################

def download_file(url, save_path):
    try:
        # Send GET request to the URL
        response = requests.get(url)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Write the content of the response to a local file
            with open(save_path, 'wb') as file:
                file.write(response.content)
            print(f"File downloaded successfully: {save_path}")
        else:
            print(f"Failed to download file. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

def download_multiple_files(urls, save_folder):
    for url in urls:
        try:
            # Extract the file name from the URL
            file_name = url.split("/")[-1]
            save_path = os.path.join(save_folder, file_name)
            
            # Download the file
            download_file(url, save_path)
            print("successfully downloaded file from url: ",url)
        
        except Exception as e:
            print(f"Error downloading {url}: {e}")

##########################################################################
# define utility functions
##########################################################################

days = [15, 16, 17, 18, 19, 20, 21]
hours = [6, 10, 14, 18, 20]

url_string = "https://urbanheatmaps.s3.us-east-1.amazonaws.com/chicago/year2021-month7-dayX-hourX-minute0-MRT-mask.tif"
urls_replace_day = [url_string.replace("dayX","day"+str(d)) for d in days]
print(urls_replace_day)
print(len(urls_replace_day))

urls_replace_hour = [url_d.replace("hourX","hour"+str(h)) for url_d in urls_replace_day for h in hours] 
print(urls_replace_hour)
print(len(urls_replace_hour))

urls = urls_replace_hour
save_folder = "./downloads"  # Replace with the folder where you want to save the files
# Create the folder if it doesn't exist
os.makedirs(save_folder, exist_ok=True)
download_multiple_files(urls, save_folder)



















