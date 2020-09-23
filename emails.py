import csv
from threading import Thread
import threading
import schedule
import time
from flask import Flask, request, jsonify, render_template
from flask_mail import Mail, Message
import smtplib 
import os.path
from os import path
import pandas as pd

class MailServer(Thread):
    thread_stop = False

    def __init__(self, app_input):
        super(MailServer, self).__init__()
        print('MailServer -> init')
        self.scheduler = schedule.Scheduler()
        self.app = app_input
        self.app.config.update(
            DEBUG=True,
            #EMAIL SETTINGS
            MAIL_SERVER='smtp.gmail.com',
            MAIL_PORT=465,
            MAIL_USE_SSL=True,
            MAIL_USERNAME = 'dshrishikesh@gmail.com',
            MAIL_PASSWORD = 'ltzehzwzbwqklfbs',
            MAIL_DEFAULT_SENDER='dshrishikesh@gmail.com',
        )
        self.mail=Mail(self.app)

    def send_email(self):
        if path.exists("userID.csv"):
            df=pd.read_csv("userID.csv", names=['state','district', 'case', 'cured', 'active', 'death', 'email'])
            __email=df['email'].tolist()
            __state=df['state'].tolist()
            __district=df['district'].tolist()
            __case=df['case'].tolist()
            __cured=df['cured'].tolist()
            __active=df['active'].tolist()
            __death=df['death'].tolist()
        else:
            __email = []
        print("send_email -> call", threading.get_ident())
        with self.app.app_context():
            print('length of emails list :', len(__email))
            for id in range(len(__email)):
                msg=Message("COVID-19 Stats",
                    sender="dshrishikesh@gmail.com",
                    recipients=[__email[id]])
                
                msg.body="State: {} \nDistrict: {} \nCases: {} \nCured: {} \nActive: {} \nDeath: {} \n".format(__state[id],__district[id], __case[id], __cured[id], __active[id], __death[id])
                self.mail.send(msg)

    def run(self):
        print("mail_server -> started", threading.get_ident())
        # self.scheduler.every().day.at("15:30").do(self.send_email)
        self.scheduler.every(1).minutes.do(self.send_email)
        # self.send_email()
        while not self.thread_stop:
            self.scheduler.run_pending() 
            time.sleep(1) 