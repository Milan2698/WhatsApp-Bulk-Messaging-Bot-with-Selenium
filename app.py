from flask import Flask, request, render_template, redirect, session
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from werkzeug.utils import secure_filename
from flask.json import JSONEncoder
from werkzeug.datastructures import FileStorage
from time import sleep
from urllib.parse import quote
import os
import random

options = Options()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument("--profile-directory=Default")

os.system("")
os.environ["WDM_LOG_LEVEL"] = "0"
app = Flask(__name__)
app.secret_key = 'secret_key'


@app.route('/', methods=["GET","POST"])
def upload():
    if request.method == "POST":
        message = request.form['message']
        csv_file = request.files['csvfile']
        img_file = request.files['imgfile']
        
        df = pd.read_csv(csv_file)
        number_list = df['numbers'].tolist()

        # Save the image file to a temporary directory
        temp_dir = os.path.join(app.root_path, 'temp')
        os.makedirs(temp_dir, exist_ok=True)
        img_path = os.path.join(temp_dir, secure_filename(img_file.filename))
        img_file.save(img_path)
        session['message'] = message
        session['number_list'] = number_list
        session['img_path'] = img_path
        return redirect('wapp')
    return render_template('index.html')

@app.route("/wapp")
def index():
    message = session.get('message', [])
    number_list = session.get('number_list', [])
    img_path = session.get('img_path', [])
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get('https://web.whatsapp.com')
    sleep(25)
    number_list = [9924870676, 7874868634]
    for idx, number in enumerate(number_list):
        t = random.randint(8,15)
        sleep(t)
        if number == "":
            continue
        try:
            url = 'https://web.whatsapp.com/send?phone=' + str(number) + '&text=' + message

            driver.get(url)
            t = random.randint(3,6)
            sleep(t)
            media_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/div')))
            media_btn.click()
            t = random.randint(3,6)
            sleep(t)
            gallery_button = driver.find_element('css selector','button._1CGek input')
            
            gallery_button.send_keys(img_path)
            t = random.randint(3,6)
            sleep(t)
            send_button = driver.find_element('xpath','//*[@id="app"]/div/div/div[3]/div[2]/span/div/span/div/div/div[2]/div/div[2]/div[2]/div/div')
            t = random.randint(5,12)
            sleep(t)
            send_button.click()
                    

        except Exception as e:
            print('Failed to send message to ' + str(number) + str(e))
    driver.close()
    return 'Sent'

if __name__ == '__main__':
   app.run(debug = True)