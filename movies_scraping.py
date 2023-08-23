#import libraries
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd

driver=webdriver.Chrome(service=ChromeService())

#url
imbd_url="https://imdb.com"
driver.get(imbd_url)

#For window maximize
driver.maximize_window()

# select All
dropdown=driver.find_element(By.XPATH, '//div[@class="sc-dIfARi gHSGHl navbar__flyout--breakpoint-m navbar__flyout--positionLeft"]')
dropdown.click()

#Advance search
advance_search = driver.find_element(By.LINK_TEXT, value='Advanced Search')
advance_search.click()

# Advance_title
advance_title=driver.find_element(By.XPATH, '//a[@href="/search/title"]' )
advance_title.click()

# feature_film
feature=driver.find_element(By.XPATH, '//input[@id="title_type-1"]' )
feature.click()

# Tv_film
Tv=driver.find_element(By.XPATH, '//input[@id="title_type-2"]' )
Tv.click()

# from_date :
from_date = driver.find_element(By.NAME, 'release_date-min')
from_date.click()
from_date.send_keys('1999')

# till_date
till_date=driver.find_element(By.NAME, 'release_date-max')
till_date.click()
till_date.send_keys('2023')

# minimum rating
min_rat=driver.find_element(By.NAME, 'user_rating-min')
min_rat.click()
min_rat.send_keys('1.0')

# maximum rating
min_rat=driver.find_element(By.NAME, 'user_rating-max')
min_rat.click()
min_rat.send_keys('10.0')

# oscar nominated
nominated=driver.find_element(By.XPATH, '//input[@id="groups-7"]' )
nominated.click()

# colored
color=driver.find_element(By.XPATH, '//input[@id="colors-1"]' )
color.click()

# Which language of movie
language = driver.find_element(By.NAME, 'languages')
dropdown_4 = Select(language)
dropdown_4.select_by_visible_text('English')

# In which order u want to see movie details
sort = driver.find_element(By.NAME, 'sort')
drop= Select(sort)
drop.select_by_visible_text('A-Z Ascending')

# How many movies u want on a page
per_page = driver.find_element(By.NAME, 'count')
drop= Select(per_page)
drop.select_by_visible_text('250 per page')

# search button
submit=driver.find_element(By.XPATH, '//button[@class="primary"]' )
submit.click()

# scrape the current page
def scrape_page():
    # find movies name
    list_items = driver.find_elements(By.XPATH, '//h3[@class="lister-item-header"]')
    names = []
    # year of movie
    year = driver.find_elements(By.XPATH, '//span[@class="lister-item-year text-muted unbold"]')
    years = []
    # metascore of movie
    mata = driver.find_elements(By.XPATH, '//div[@class="inline-block ratings-metascore"]')
    metascore = []
    # genre
    genre = driver.find_elements(By.XPATH, '//span[@class="genre"]')
    genres = []
    # Director names
    director = driver.find_elements(By.XPATH, '//p[@class=""]')
    directors = []
    #Earning
    earn = driver.find_elements(By.XPATH, '//p[@class="sort-num_votes-visible"]/span[5]')
    earns = []

    for item,yea,mat,gen,er,di in zip(list_items,year,mata,genre,earn,director):
        title = item.find_element(By.TAG_NAME, 'a').text
        names.append(title)
        years.append(yea.text.replace('(', '').replace(')', ''))
        metascore.append(mat.text)
        genres.append(gen.text.strip())
        d = di.find_element(By.TAG_NAME, 'a').text
        directors.append(d)
        earns.append(er.text)

#convert scrap iteam in csv file
    df = pd.DataFrame({'movies': names, 'Releasing Year':years , 'Metascores': metascore, 'Directors':directors, 'Earning':earns })
    df.to_csv('movie.csv', mode='a', header=False, index=False)

#how many pages to scrap
num_pages_to_scrape = 4

for page in range(num_pages_to_scrape):
    # Scraping logic for the current page
    scrape_page()

#scraping for next page
    try:
        next_page_button = driver.find_element(By.XPATH, '//a[@class="lister-page-next next-page"]')
        if next_page_button.is_enabled():
            next_page_button.click()
        else:
            print("No more pages to scrape.")
            break
    except:
        print('No more page')

time.sleep(10)

#close the browser
driver.quit()


