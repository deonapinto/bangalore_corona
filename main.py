from flask import Flask, request, jsonify, render_template
import util
import os
import pandas as pd
import threading
import time
from cor import WebScraper
from emails import MailServer
from flask import render_template

app = Flask(__name__)

# http://synthetics.newrelic.com For pinging purposes
state=''

@app.route('/', methods=['GET'])
def home():
    return render_template("app.html") 

@app.route('/get_state_names', methods=['GET'])
def get_state_names():
    response=jsonify({
        'states':util.get_states()
    })
    response.headers.add('Access-Control-Allow-Origin','*')

    return response

@app.route('/load_districts',methods=['GET','POST'])
def get_district_names():
    state = ''
    if request.method == 'POST':
        state=request.form['state']
    response=jsonify({
        'district':util.load_district(state)
    })
    response.headers.add('Access-Control-Allow-Origin','*')
    return response

@app.route('/send_mail',methods=['GET','POST'])
def send_mail():
    if request.method == 'POST':
        district=request.form['district']
        email=request.form['mail']
    response=jsonify({
        'data':util.add_and_get_email(district,email)
    })
    response.headers.add('Access-Control-Allow-Origin','*')
    return response
    
if __name__ == "__main__":
    print("Starting Python Flask Server coronavirus stats...")
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print('Server time :', current_time)
    print('Main thread id :', threading.get_ident())
    util.load_states()
    hst = '127.0.0.1'
    prt = 5000
    if 'PORT' in os.environ:
        hst = '0.0.0.0'
        prt = os.environ['PORT']
    print('Thread creation')
    web_scraper_thread = WebScraper()
    web_scraper_thread.start()
    mail_thread = MailServer(app)
    mail_thread.start()
    print('Thread creation done')
    app.run(host=hst, port=int(prt), debug=False)
    mail_thread.thread_stop = True # Stop mail_server
    web_scraper_thread.thread_stop = True # Stop web_scraper_server
    mail_thread.join()
    web_scraper_thread.join()

