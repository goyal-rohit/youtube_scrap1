from flask import Flask, render_template, request
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import logging
import time
logging.basicConfig(filename="you_scrap.log" , level=logging.INFO)

app = Flask(__name__)

@app.route("/", methods = ['GET'])
def homepage():
    return render_template("index.html")

@app.route("/review" , methods = ['POST' , 'GET'])
def index():
    if request.method == 'POST':
                try:
                    url = request.form['content'].replace(" ","")
                    result = 5
                            # fake user agent to avoid getting blocked by Google
                    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}
                    driver = webdriver.Chrome('chromedriver.exe')
                    driver.get(url+'/videos')
                    # link = []
                    # img_link = []
                    # title = []
                    # view_list = []
                    # date_list = []
                    reviews = []
                    

                    wait = WebDriverWait(driver, 20)

                    body_elem = driver.find_element(By.TAG_NAME, 'body')
                    for i in range(5):
                        body_elem.send_keys(Keys.PAGE_DOWN)
                        time.sleep(2)

                    vid_url = driver.find_elements(By.XPATH, "//a[@id='video-title-link']")

                    view = driver.find_elements(By.XPATH,'//*[@id="metadata-line"]/span[1]' )

                    date = driver.find_elements(By.XPATH,'//*[@id="metadata-line"]/span[2]' )

                    image_links = driver.find_elements(By.XPATH, "//a[@id='thumbnail']/yt-image/img")

                    for i in range(result+1):
                        # link.append(vid_url[i].get_attribute('href'))
                        # view_list.append(view[i].text)
                        # date_list.append(date[i].text)
                        # title.append(vid_url[i].text)
                        # img_link.append(image_links[i].get_attribute('src'))

                        link = vid_url[i].get_attribute('href')
                        view_list = view[i].text
                        date_list = date[i].text
                        title = vid_url[i].text
                        img_link = image_links[i].get_attribute('src')
                        mydict = {'Web URLs': link,  'Image Link':img_link , 'Video Title': title, 'Video Views': view_list, 'Video Date':date_list}
                        reviews.append(mydict)
                
                    logging.info("log my final result {}".format(reviews))
                    return render_template('result.html', reviews=reviews[0:(len(reviews)-1)])
                


                except Exception as e:
                    logging.info(e)
                    return 'something is wrong'
            # return render_template('results.html')

    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
