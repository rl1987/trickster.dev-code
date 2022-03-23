#!/usr/bin/python3

import time

import praw

USER_AGENT = "automations"

def try_posting(reddit, username, subject, message):
    try:
        reddit.redditor(username).message(subject, message)
    except praw.exceptions.RedditAPIException as e:
        for subexception in e.items:
            if subexception.error_type == "RATELIMIT":
                error_str = str(subexception)
                print(error_str)

                if 'minute' in error_str:
                    delay = error_str.split('for ')[-1].split(' minute')[0]
                    delay = int(delay) * 60.0
                else:
                    delay = error_str.split('for ')[-1].split(' second')[0]
                    delay = int(delay)

                time.sleep(delay)
            elif subexception.error_type == 'INVALID_USER':
                return True

        return False
    except Exception as e:
        print(e)
        return False

    return True

def main():
    reddit = praw.Reddit("bot", user_agent=USER_AGENT)
    
    subject = input("Subject: ")

    in_f = open("message.txt", "r", encoding="utf-8")
    templ = in_f.read()
    in_f.close()

    in_f = open("users.txt", "r", encoding="utf-8")

    for username in in_f:
        username = username.strip()
        print(username)
        
        message = templ.replace("{{username}}", username)
        
        while True:
            if try_posting(reddit, username, subject, message):
                break
            
        print(reddit.auth.limits)

        if reddit.auth.limits['remaining'] == 0:
            timeout = reddit.auth.limits['reset_timestamp'] - time.time()
            print("Used up requests in current time window - sleeping for {} seconds".format(timeout))
            time.sleep(timeout)

    in_f.close()

if __name__ == "__main__":
    main()

