
#=============================================================================
#=============================================================================
# Importing the necessary packages
import selenium
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import requests
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np

# We will use Selenium as it works best against the dynamica coded web pages

# launching the driver
driver = webdriver.Chrome("C:/Users/piyus/Downloads/chromedriver_win32 (1)/chromedriver.exe")
# 
# Wait for 5 seconds
time.sleep(5)
# 
driver.maximize_window()
# 
# # Load a website
driver.get('https://www.croma.com/televisions-accessories/led-tvs/4k-ultra-hd-tvs/c/999')
#  
# 

# The Page has a view button and as the page is dynamically coded using javascript
#  
while True:
    
    try:
        # Finding the View All button using the Pathe
        element = driver.find_element(By.XPATH,'//button[@class="btn btn-secondary btn-viewmore"]')
        # Clicking the button
        driver.execute_script("arguments[0].click();", element)
    
    # When there are no more products to the view all button will vanish and the we will
    # get this error and break through the group.
    
    except NoSuchElementException:
        break


# Sending the html to beautiful to handle the html 

soup = BeautifulSoup(driver.page_source,'lxml')


#=============================================================================

# The products links and the title is in the class 'product-title plp-prod-title' having tag
# 'h3' 

# Collecting all the links and titles classes
 
products = soup.find_all('h3' , class_ = 'product-title plp-prod-title')
 
# =============================================================================
links = []
title = []

# Extracting the Link and title string. 

for product in products:
    
     link = product.find('a')
     links.append('https://www.croma.com' + link.get('href'))
     b = product.text
     title.append(b)

# Image Url

# Doing the same with the Image URL

img_urls = soup.find_all('div',class_='product-img plp-card-thumbnail')
image_url = []

for img_url in img_urls:
    
    image_url.append(img_url.find('a').get('href'))
    
len(image_url)
# =============================================================================

# MRP

 
mrps = soup.find_all('span',{'class' : 'amount','id' : 'old-price'})
# 
mrp_f = []
for mrp in mrps:
     mrp_price = mrp.text
     mrp_price = mrp_price.split(' ')[1][1:].replace(',','')
     mrp_f.append(float(mrp_price))
   
len(mrp_f)

# =============================================================================


price = []

prices = soup.find_all('span',{'class' : 'amount','data-testid':"new-price"})

for p in prices:
     price_ = p.text
     price_ = price_.strip()[1:].replace(',','')
     price.append(float(price_))
   


# Rate,count of review and count of ratings are in same string

# Some products has rating only and others have both.
# Getting the Rate,count of review and count of ratings

rating_review = soup.find_all('div',{'class':'cp-rating plp-ratings ratings-plp-line'})


rating = []
count_reviews =[]
count_ratings = []
temps = []
count = 0


for rate_review in rating_review:
    count +=1
    
    
    
    temp = rate_review.text
    temp = temp.split()
    temp
    
    
    if len(temp) == 0:
            
            rating.append(np.NAN)
            count_reviews.append(np.NAN)
            count_ratings.append(np.NAN)
    
    
    elif len(temp) > 4:
       
        rate = temp[0].split('(')[0]
        rating.append(float(rate))
        
        count_rating = temp[0].split('(')[1] 
        count_ratings.append(int(count_rating))
    
        
        count_review = temp[3] 
        count_reviews.append(int(count_review))
        
    else:
            
        if len(temp) > 0:
            if 'Rating' in temp[1]:
                rate = temp[0].split('(')[0]              
                rating.append(float(rate))
                
                count_rating = temp[0].split('(')[1] 
                count_ratings.append(int(count_rating))
                
                count_reviews.append(np.NAN)
                
                
            
            elif  'Review' in temp[1]:
                
                rating.append(np.NAN)
                
                count_ratings.append(np.NAN)
    
                
                count_review = temp[0]
               
                count_reviews.append(int(count_review))
                
       
                



# For extracting the brands,we will have to open each prroduct link and go in and get the 
# brand


brands = []

# we have the list of all the links already

for l in links:
    # Getinng one url at a time
    r = requests.get(l)
    
    # Parsing
    soup2 = BeautifulSoup(r.content,'lxml')
    
    #Appending the brand name to brands
    
    brands.append(soup2.find_all('li',{'class':'cp-specification-spec-details'})[4].text)



# =============================================================================
# 
# - Title
# - Brand
# - MRP
# - Price
# - Count of Ratings
# - Count of Reviews
# - Average Rating Score
# - Product URL
# - Image URL
# 
# =============================================================================


listing_position  = np.arange(1,154)
print(listing_position)
print(len(title))
print(len(brands))
print(len(mrp_f))
print(len(price))
print(len(count_ratings))
print(len(rating))
print(len(links))
print(len(image_url))



# Creating a CSV file of the above data.

import pandas as pd

data = {'Listing_Postion' : listing_position,
        'Title'                 : title,
        'Brand'                 : brands,
        'MRP'                   : mrp_f,
        'Price'                 : price,
        'Count_of_Rating'       : count_ratings,
        'Count_of_reviews'      : count_reviews,
        'Average_Rating_Score'  : rating,
        'Product_URL'           : links,
        'Image_URL'             : image_url                                      
        }

df = pd.DataFrame(data)

df

df.to_csv('Croma_Scrapping.csv',index = False)



