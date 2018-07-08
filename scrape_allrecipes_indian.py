# Scraping file combs allrecipes.com for information on: recipe title, # people to make the 
# recipe, # of reviews, star rating, time to completion, ingredients, steps, and category. 

import os, re, time, string
import numpy as np
from selenium import webdriver

_start_time = time.time()

def tic():
    global _start_time 
    _start_time = time.time()

def toc():
    t_sec = round(time.time() - _start_time)
    (t_min, t_sec) = divmod(t_sec, 60)
    (t_hour,t_min) = divmod(t_min, 60) 
    print('Time passed: {}hour:{}min:{}sec'.format(t_hour, t_min, t_sec))

tic()

chromedriver = '/usr/local/bin/chromedriver'
os.environ['webdriver.chrome.driver'] = chromedriver
driver = webdriver.Chrome(chromedriver)

pages = ['https://www.allrecipes.com/recipes/233/world-cuisine/asian/indian/?page=' + str(p) for p in range(1,31)]

for j in pages:

    driver.get(str(j))

    fav = driver.find_elements_by_class_name('favorite')
    ids = []
    names = []
    urls = []
    for x in np.arange(len(fav)):
        ids.append(str(fav[x].get_attribute('data-id')))
        names.append(str(fav[x].get_attribute('data-name')))
    urls = ['https://allrecipes.com/recipe/' + id for id in ids]   
    #print(urls)
    #print(len(urls))

    for i in urls: 
        
        try:
            driver.get(str(i))

            recipetitle = driver.find_element_by_class_name('recipe-summary__h1').text

            madeitcount = driver.find_element_by_class_name('made-it-count').text

            reviewcount = driver.find_element_by_class_name('review-count').text
            reviewcount = str(re.findall('(\w+) reviews', reviewcount)[0])

            starrating = driver.find_element_by_class_name('rating-stars').get_attribute('data-ratingstars')

            readyintime = driver.find_element_by_class_name('ready-in-time').text

            ingred = driver.find_elements_by_class_name('checkList__item')
            ingredients = []
            for x in np.arange(len(ingred)-1):
                ingredients.append(str(ingred[x].text))

            step = driver.find_elements_by_class_name('recipe-directions__list--item')
            steps = []
            for x in np.arange(len(step)-1):
                steps.append(str(step[x].text))

            cat = driver.find_elements_by_class_name('toggle-similar__title')
            categories = []
            for x in np.arange(len(cat)):
                categories.append(str(cat[x].text))
        
            print(recipetitle + ' | ' + madeitcount + ' | ' + reviewcount + ' | ' + starrating + ' | ' + readyintime + ' | ' + '; '.join(ingredients) + ' | ' + '; '.join(steps) + ' | ' + '; '.join(categories))

        except:
            continue

driver.quit()

toc()




