import os
import datetime as dt
import socket
from time import sleep
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def get_now():
  return dt.datetime.now().replace(microsecond=0)


def send_mail(body):
  message = Mail(
    from_email=os.environ.get("MAIL_FROM"),
    to_emails=os.environ.get("MAIL_TO"),
    subject="Internet reconnected",
    plain_text_content=body)
  try:
    sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
    sg.send(message)
  except Exception as ex:
    print(f"Could not send email: {ex}")


class Target:

  def __init__(self, name, ip, port):
    self.name = name
    self.ip = ip
    self.port = port
    self.connected = None
    self.connect()

  def connect(self):
    try:
      socket.create_connection((self.ip, self.port), 1).close()
      self.connected = True
    except:
      print(f"Could not connect to {self.name}={self.ip}:{self.port}")
      self.connected = False
    return self.connected

  @classmethod
  def get(cls, name, var):
    targets = []
    for ip_port in os.environ[var].split(","):
      ip = ip_port.split(":")[0]
      port = int(ip_port.split(":")[1])
      targets.append(cls(name, ip, port))
    return targets


class Connection:

  def __init__(self):
    self.modems = Target.get("modem", "MODEMS_IP_PORT")
    # self.dns = Target.get("dns", "DNS_IP_PORT")
    # self.websites = Target.get("website", "WEBSITES_IP_PORT")

    try:
      with open("/opt/module/data/logs.csv", "r") as logs:
        last_row = logs.readlines()[-1].split(";")
        self.start_time = dt.datetime.strptime(last_row[0], "%Y-%m-%d %H:%M:%S")
        self.connected = bool(int(last_row[1]))
    except Exception as ex:
      self.start_time = get_now()
      self.connected = self.check()
      with open("/opt/module/data/logs.csv", "a") as logs:
        logs.write("{};{};".format(self.start_time, "1" if self.connected else "0"))
    print("Internet is {}connected since {}.".format("" if self.connected else "dis", self.start_time))


  def check(self):
    connected = False
    for modem in self.modems:
      connected = connected or modem.connect()
    return connected


  def log(self, now, duration):
    with open("/opt/module/data/logs.csv", "a") as logs:
      logs.write("{};\n{};{};".format(duration, now, "1" if self.connected else "0"))
    if self.connected:
      send_mail("Internet was disconnected for {}".format(duration))


  def monitor(self):
    print("Last know status: {}connected".format("" if self.connected else "dis"))
    while True:
      if self.connected != self.check():
        now = get_now()
        duration = now - self.start_time
        print("Internet was {}connected for {}.".format("" if self.connected else "dis" , duration))
        self.connected = not self.connected
        self.start_time = now
        self.log(now, duration)
      if self.connected:
        sleep(5)
      else:
        sleep(1)


if __name__== "__main__":
  Connection().monitor()
