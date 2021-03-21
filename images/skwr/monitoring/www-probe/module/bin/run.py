#!/usr/bin/env python3

import datetime as dt
import logging
import os
import socket
from time import sleep

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def get_now(microsecond=False):
    now = dt.datetime.now()
    if not microsecond:
        now = now.replace(microsecond=0)
    return now


def send_mail(body):
    message = Mail(
        from_email=os.environ.get("MAIL_FROM"),
        to_emails=os.environ.get("MAIL_TO"),
        subject="Internet reconnected",
        plain_text_content=body,
    )
    try:
        sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
        sg.send(message)
    except Exception as ex:
        logging.error(f"Could not send email: {ex}")


class Target:
    def __init__(self, name, ip, port):
        self.name = name
        self.ip = ip
        self.port = port
        self.connected = None
        self.connect()

    def connect(self):
        logging.debug(f"Checking connection to {self.ip}:{self.port}")
        try:
            socket.create_connection((self.ip, self.port), 1).close()
            self.connected = True
        except:
            if self.connected:
                logging.warning(
                    f"Could not connect to {self.name}={self.ip}:{self.port}"
                )
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
                connected = "1" if self.connected else "0"
                logs.write(f"{self.start_time};{connected};")
        connected = "connected" if self.connected else "disconnected"
        logging.info(f"Internet is {connected} since {self.start_time}.")

    def check(self):
        connected = False
        for modem in self.modems:
            connected = connected or modem.connect()
        return connected

    def log(self, now, duration):
        message = "Internet was {}connected for {}.".format(
            "" if self.connected else "dis", duration
        )
        logging.info(message)

        if not self.connected:
            send_mail(message)

        with open("/opt/module/data/logs.csv", "a") as logs:
            logs.write(
                "{};\n{};{};".format(duration, now, "1" if self.connected else "0")
            )

    def monitor(self):
        interval = int(os.environ.get("INTERVAL", "5"))
        logging.info(f"Polling interval: {interval}s")
        logging.info(
            "Last know status: {}connected".format("" if self.connected else "dis")
        )
        while True:
            if self.connected:
                # Try to prevent clock skew
                now = get_now(microsecond=True)
                sleep(
                    interval - ((now.second + (now.microsecond / 10 ** 6)) % interval)
                )
            else:
                sleep(1)

            if self.connected != self.check():
                now = get_now()
                duration = now - self.start_time
                self.log(now, duration)
                self.connected = not self.connected
                self.start_time = now


if __name__ == "__main__":
    log_level = logging.INFO
    if os.environ.get("DEBUG", "0") != "0":
        log_level = logging.DEBUG
    logging.basicConfig(
        datefmt="%Y/%m/%d %H:%M:%S",
        format="%(asctime)s\t%(levelname)s\t%(message)s",
        level=log_level,
    )

    Connection().monitor()
