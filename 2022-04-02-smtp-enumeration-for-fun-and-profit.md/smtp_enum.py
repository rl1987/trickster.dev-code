#!/usr/bin/python3

import smtplib
import sys

import dns.resolver  # requires dnspython


def make_smtp_conn(smtp_hostname):
    conn = smtplib.SMTP(smtp_hostname)

    conn.helo("gmail.com")
    conn.mail("FROM: <a@gmail.com>")

    return conn


def main():
    if len(sys.argv) != 3:
        print("Usage:")
        print("{} <wordlist> <domain>".format(sys.argv[0]))
        return

    domain = sys.argv[-1]

    answers = dns.resolver.resolve(domain, "MX")

    if len(answers) == 0:
        print("Error: no MX records found for {}".format(domain))
        return -1

    in_f = open(sys.argv[1], "r")

    smtp_hostname = str(answers[0].exchange)

    conn = make_smtp_conn(smtp_hostname)

    n = 0

    for line in in_f:
        line = line.strip()

        email_addr = line + "@" + domain

        status, _ = conn.rcpt(email_addr)
        if status == 250:
            print(email_addr)

        n += 1
        if n % 99 == 0:
            conn.quit()
            conn = make_smtp_conn(smtp_hostname)

    conn.quit()


if __name__ == "__main__":
    main()
