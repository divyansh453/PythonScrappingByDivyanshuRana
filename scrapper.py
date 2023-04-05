# PROGRAM STARTS HERE
from bs4 import BeautifulSoup #Python Library to Parse HTML Content.
import requests #This Module is  used to get HTML content of Website.
import csv #Python Module for CSV files.
csv_file=open('amazon_scraper.csv','w') #File opens here if it exists then new data overwrites old one otherwise newfile is created.

csv_writer=csv.writer(csv_file) 
csv_writer.writerow(['Product Name','Price','Rating','Seller Name']) #First Row Which contains is written here

# Headers are used because server can block us so we take the help of agent to prevent it.
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}

print("Scrapping.....") #Scrappping starts here.

#Here we get the Whole content of website.
source=requests.get('https://www.amazon.in/s?rh=n%3A6612025031&fs=true&ref=lp_6612025031_sa',headers=headers).text  

soup=BeautifulSoup(source,'lxml') # Parsing is done using lxml parser

article=soup.find('div',class_="s-search-results") #Find HTML code of that part whose class is "s-search-results"


for content in article.find_all('div',class_="a-section a-spacing-small puis-padding-left-small puis-padding-right-small"):
    #"find" returns  only first match whereas "find_all" returns all matches and append all matching items into a list.

    #Product name is fetched here which is before first comma.
    product_name=content.find('h2').text.split(',')[0] 

    #Price is fetched using the class and tag and then text is extracted form it.
    price=content.find('span',class_='a-price-whole').text 
    
    #Price is fetched using the class and tag and then text is extracted form it.
    rating=content.find('span',class_='a-size-base').text

    #Here I extracted the id of particular product to get all its details and to scrap webpage related to it.
    try:
        product_id=content.find('a')['href'].split('/')[3]
    except:
        #If url does not exist then empty string will be assigned to product_id.
        product_id=" "
    
    #Here I created the url of particular product.
    item_url=f'https://www.amazon.in/dp/{product_id}'
    # Now I again uses beautifulsoup to scrap the webpage of product.
    source1=requests.get(item_url,headers=headers).text
    soup1 = BeautifulSoup(source1, 'lxml')
    try:
        #Here I again use try and except as those elements can't be fetched whose url is  not correct and to remove errors it is done. 
        seller=soup1.find(id="merchant-info").a.span.text #Here the name of seller is assigned to identifier "seller"
        stock=soup1.find(id="availability").span.text #Here the Availablity of product will be assigned to "stock" ('In Stock' OR 'Out of Stock')
    except:
        seller="Sponsored Item" # If Item is Sponsored item then it will be assigned to seller
        stock=" " # Empty string will be assigned to "stock"

    stock1=(stock[1:4]+stock[5:7]+stock[8:12]) #Here the string stored in stock will be used to create new string by removing spaces.
    if stock1!="outofstock" and  seller!="Sponsored Item": 
        #If Item  is in stock then seller name and data will be stored in csv file.
        csv_writer.writerow([product_name,price,rating,seller])
    elif seller!="Sponsored Item":
        #if item is out of stock and not a sponsored item then data will be stored without seller name
        csv_writer.writerow([product_name,price,rating,None])

print("File Created.") #Message to know the completion of Process.
csv_file.close() #File is closed.

#END OF PROGRAM
