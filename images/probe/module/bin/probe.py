import os
import datetime as dt
import http.client as http
from time import sleep
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

URLS = ["www.google.com", "en.wikipedia.org", "www.amazon.com", "www.twitter.com"]

def get_now():
  return dt.datetime.now().replace(microsecond=0)


def check_connection():
  connected = False
  for url in URLS:
    conn = http.HTTPConnection(url, timeout=1)
    try:
      conn.request("HEAD", "/")
      connected = True
    except:
      print("Could not connect to {}".format(url))
    conn.close()
    if connected:
      break
  return connected

def send_mail(body):
  message = Mail(
    from_email=os.environ.get("MAIL_FROM"),
    to_emails=os.environ.get("MAIL_TO"),
    subject="Internet reconnected",
    plain_text_content=body)
  try:
    sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
    sg.send(message)
  except Exception as e:
    print(e.message)

class Connection():
  def __init__(self):
    try:
      with open("/opt/module/data/logs.csv", "r") as logs:
        last_row = logs.readlines()[-1].split(";")
        self.start_time = dt.datetime.strptime(last_row[0], "%Y-%m-%d %H:%M:%S")
        self.connected = bool(int(last_row[1]))
    except Exception as ex:
      self.start_time = get_now()
      self.connected = check_connection()
      with open("/opt/module/data/logs.csv", "a") as logs:
        logs.write("{};{};".format(self.start_time, "1" if self.connected else "0"))
    print("Internet is {}connected since {}.".format("" if self.connected else "dis", self.start_time))


  def log(self, now, duration):
    with open("/opt/module/data/logs.csv", "a") as logs:
      logs.write("{};\n{};{};".format(duration, now, "1" if self.connected else "0"))
    if self.connected:
      send_mail("Internet was disconnected for {}".format(duration))


  def monitor(self):
    print("Last know status: {}connected".format("" if self.connected else "dis"))
    while True:
      now = get_now()
      if self.connected != check_connection():
        duration = now - self.start_time
        print("Internet was {}connected for {}.".format("" if self.connected else "dis" , duration))
        self.connected = not self.connected
        self.start_time = now
        self.log(now, duration)
      if self.connected:
        sleep(10)
      else:
        sleep(1)


if __name__== "__main__":
  Connection().monitor()
