#

# ____________________________________________________________________________________________________
# imports:


from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# ____________________________________________________________________________________________________

# Constants:

link_to_google_forms="Your Link To Your Google Forms" #in order to fill the prices along with the names and adresses if the home

Zillow_link="https://www.zillow.com/homes/for_rent/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-122.50165022802734%2C%22east%22%3A-122.2901634116211%2C%22south%22%3A37.69139091774614%2C%22north%22%3A37.8243929084194%7D%2C%22mapZoom%22%3A12%2C%22isMapVisible%22%3Afalse%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D"

chrome_driver_path="Your Chrome Driver Path"

# ____________________________________________________________________________________________________

# scrabing the data(links,price,address) using the BS:

response = (requests.get(url=Zillow_link ,headers={ 'User-Agent':'Your Chrome user agent',
                                                   'Accept-Language':'Your Chrome  accept language',
                                                   'Accept-Encoding':'Your Chrome accept encoding'}))

# print(response.raise_for_status())

zillowhtml=response.text


soup=BeautifulSoup(zillowhtml,"html.parser")

# data:

 #1)links

elements_that_contains_links=soup.find_all(name="a",class_="property-card-link")

Links_for_properties=[element.get("href") for element in elements_that_contains_links
]

      #or if you want to add the http to the incomplete versions :
      # all_links = []
      # for link in all_link_elements:
      #     href = link["href"]
      #     print(href)
      #     if "http" not in href:
      #         all_links.append(f"https://www.zillow.com{href}")
      #     else:
      #         all_links.append(href)



 #2)prices:

elements_that_contains_prices=soup.find_all(name="span",class_="PropertyCardWrapper__StyledPriceLine-srp__sc-16e8gqd-1 iMKTKr")

prices=[element.text for element in elements_that_contains_prices
]

splitted_prices=[]

try:
  for price in prices:
   sp=price.split('+')[0]
   splitted_prices.append(sp)
    
except:
  sp=price.split('/')[0]
  splitted_prices.append(sp)




# adresses:

elements_that_contains_addresses=soup.find_all(name="address")

addresses=[element.text for element in elements_that_contains_addresses
]



# ____________________________________________________________________________________________________


#automating the filling of the data in the google form ! 

driver=webdriver.Chrome(executable_path=chrome_driver_path)

#may be there is no need to log in to the account because its a normal form,
#  and any one can get access to fill it and there is no need directly to log in to the account in order to fill it ! 


for address in addresses:

    time.sleep(15)
  
    #opening the new format:
  
    driver.get(link_to_google_forms)

  #filling the adress data:
    
    address_category=driver.find_element_by_xpath('//*[@id="SchemaEditor"]/div/div[2]/div/div[2]/div[3]/div[1]/div/div/div[1]/div[2]/div[3]/div[1]/div[2]/div/div[2]/div/div[2]/input')
    address_category.send_keys(address)

    #filling the price data:

    
    price_category=driver.find_element_by_xpath('//*[@id="SchemaEditor"]/div/div[2]/div/div[2]/div[3]/div[2]/div/div/div[1]/div[2]/div[3]/div[1]/div[2]/div/div[2]/div/div[2]/input')
    price_category.send_keys(splitted_prices[address.index()])

  #filling the link data:

    
    link_category=driver.find_element_by_xpath('//*[@id="SchemaEditor"]/div/div[2]/div/div[2]/div[3]/div[3]/div/div/div[1]/div[2]/div[3]/div[1]/div[2]/div/div[2]/div/div[2]/input')
    link_category.send_keys(Links_for_properties[address.index()])


  #sending the format to convert it later with other formats :

    send_button=driver.find_element_by_xpath('//*[@id="tJHJj"]/div[1]/div[2]/div/div[7]/div')
    send_button.click()


driver.quite()






