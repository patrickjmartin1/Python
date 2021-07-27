import requests
from bs4 import BeautifulSoup
import pandas

base_url = 'https://www.apartments.com/houses/chicago-il/2-bedrooms-2-bathrooms-1500-to-4000/'

r = requests.get(base_url, auth=('user', 'pass'))
c = r.content
soup = BeautifulSoup(c, 'html.parser')

# To extract the first and last page numbers
paging = soup.find('div', {'id' : 'placardContainer'}).find('div', {'id' : 'paging'}).find_all('a')
start_page = paging[1].text
last_page = paging[len(paging)-2].text

web_content_list = []

for page_number in range(int(start_page), int(last_page) + 1):
    # To form the url based on page numbers
    url = base_url + str(page_number) + "/.html"
    r = requests.get(base_url + str(page_number) + "/")
    c = r.content
    soup = BeautifulSoup(c, "html.parser")
    # To extract the Title and the Location
    placard_header = soup.find_all("header", {"class": "placardHeader"})
    # To extract the Rent, No of Beds and Phone Number
    placard_content = soup.find_all("section", {"class": "placardContent"})
    # To process property by property by looping
    for item_header, item_content in zip(placard_header, placard_content):
        # To store the information to a dictionary
        web_content_dict = {}
        web_content_dict["Title"] = \
            item_header.find("a", {"class": "placardTitle js-placardTitle "}).text.replace("\r", "\n", "")
        web_content_dict["Address"] = item_header.find("div", {"class": "location"}).text
        web_content_dict["Price"] = item_content.find("span", {"class": "altRentDisplay"}).text
        web_content_dict["Beds"] = item_content.find("span", {"class": "unitLabel"}).text
        web_content_dict["Phone"] = item_content.find("div", {"class": "phone"}).find("span").text

        # To store the dictionary to into a list
        web_content_list.append(web_content_dict)

# To make a dataframe with the list
df = pandas.DataFrame(web_content_list)

# To write the dataframe to a csv file
df.to_csv("Output.csv")
