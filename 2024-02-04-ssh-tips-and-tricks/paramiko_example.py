#!/usr/bin/python3

import sys

import paramiko


def main():
    if len(sys.argv) != 5:
        print("{} <hostname> <username> <password> <command>".format(sys.argv[0]))
        return

    hostname = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]
    command = sys.argv[4]

    client = paramiko.client.SSHClient()

    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, username=username, password=password)

    _, stdout, _ = client.exec_command(command)

    output = stdout.read().decode("utf-8")

    print(output)


if __name__ == "__main__":
    main()
