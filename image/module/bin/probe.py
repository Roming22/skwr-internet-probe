import datetime as dt
import http.client as http
from time import sleep


def get_now():
  return dt.datetime.now().replace(microsecond=0)


def check_connection():
  connected = True
  conn = http.HTTPConnection("www.google.com", timeout=5)
  try:
    conn.request("HEAD", "/")
    conn.close()
  except:
    connected = False
  conn.close()
  return connected


class Connection():
  def __init__(self):
    try:
      with open("/opt/module/data/logs.csv", "r") as logs:
        last_row = logs.readlines()[-1].split(";")
        self.start_time = dt.datetime.strptime(last_row[0], "%Y-%m-%d %H:%M:%S")
        self.connected = bool(last_row[1])
    except:
      self.start_time = get_now()
      self.connected = check_connection()
      with open("/opt/module/data/logs.csv", "a") as logs:
        logs.write("{};{};".format(self.start_time, "1" if self.connected else "0"))
    print("Internet is {}connected since {}.".format("" if self.connected else "dis", self.start_time))


  def log(self, now, duration):
    with open("/opt/module/data/logs.csv", "a") as logs:
      logs.write("{};\n{};{};".format(duration, now, "1" if self.connected else "0"))


  def monitor(self):
    while True:
      now = get_now()
      if self.connected != check_connection():
        duration = now - self.start_time
        print("Internet was {}connected for {}.".format("" if self.connected else "dis" , duration))
        self.start_time = now
        self.connected = not self.connected
        self.log(now, duration)
      if self.connected:
        sleep(10)
      else:
        sleep(1)


if __name__== "__main__":
  Connection().monitor()
