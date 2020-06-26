#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import datetime
from argparse import ArgumentParser

import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate


def get_option():
    argparser = ArgumentParser()
    argparser.add_argument('--from_email', type=str, required=True,
                           help="from email address")
    argparser.add_argument('--password', type=str, required=True,
                           help="password for the from_email address")
    argparser.add_argument('--smtp_addr', type=str, default="smtp.gmail.com",
                           help="smtp server address")
    argparser.add_argument('--smtp_port', type=int, default=465,
                           help="smtp server port")
    argparser.add_argument('--to_email', type=str, required=True,
                           help="to email address")
    argparser.add_argument('--debug', type=bool, default=False,
                           help="true if you don't want to use headless mode of chrome")

    return argparser.parse_args()


def init_chromedriver_local(debug: bool = False) -> webdriver.Chrome:
    options = Options()
    # options.add_experimental_option("debuggerAddress", debugger_address)
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-sandbox")
    if not debug:
        options.add_argument('--headless')
    return webdriver.Chrome(options=options)


def main():
    args = get_option()

    driver = init_chromedriver_local(debug=False)
    driver.get("https://koto-kosodate-portal.jp/smf/mizube/general/refresh_cal.php?center_cd=60")

    tables = driver.find_elements_by_class_name("calendarTable")
    month = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=+9), 'JST')).month

    results = []

    for table in tables:
        print("checking month={}".format(month))
        trs = table.find_elements_by_tag_name("tr")
        for tr in trs:
            tds = tr.find_elements_by_tag_name("td")
            for td in tds:
                s = td.get_attribute("style")
                if s == "text-align: center;":
                    t = td.text.split("\n")
                    # example of t is...:
                    # ['5', '休み']
                    # ['6', 'AM ×', 'PM ×']
                    # ['7', 'AM ×', 'PM ×']
                    # ['8', 'AM ×', 'PM ×']
                    # ['9', 'AM ×', 'PM ×']
                    # ['10', 'AM ×', 'PM ×']
                    # ['11', '休み']
                    day = t[0]
                    if len(t) == 3:
                        if "AM" in t[1]:
                            if t[1] != 'AM ×':
                                results.append("{}月{}日の午前に空きがあります".format(month, day))
                            if t[2] != 'PM ×':
                                results.append("{}月{}日の午後に空きがあります".format(month, day))

                            print("{}月{}日".format(month, day))
        month += 1
    driver.close()

    if len(results) > 0:
        subject = "子ども家庭支援センター 有明みずべ - リフレッシュひととき保育 空き情報"
        # smtp_port = 465
        # smtp_addr = "smtp.gmail.com"

        msg_body = "\n".join(results)
        msg_body += "\n\n https://koto-kosodate-portal.jp/smf/mizube/general/refresh_cal.php?center_cd=60"
        msg = create_message(from_email=args.from_email, to_email=args.to_email, subject=subject,
                             body="\n".join(results))
        send(smtp_addr=args.smtp_addr, smtp_port=int(args.smtp_port), from_email=args.from_email,
             password=args.password,
             to_email=args.to_email, msg=msg)


def create_message(from_email, to_email, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email
    # msg['Bcc'] = bcc_addrs
    msg['Date'] = formatdate()
    return msg


def send(smtp_addr, smtp_port: int, from_email, password, to_email, msg):
    # context = ssl.create_default_context()
    smtpobj = smtplib.SMTP_SSL(smtp_addr, smtp_port, timeout=10)
    smtpobj.login(from_email, password)
    smtpobj.sendmail(from_email, to_email, msg.as_string())
    smtpobj.close()


if __name__ == "__main__":
    main()
