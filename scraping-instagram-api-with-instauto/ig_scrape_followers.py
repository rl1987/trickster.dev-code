#!/usr/bin/python3

import csv
import sys
import os
from pprint import pprint

import instauto.api.actions.structs.friendships as fs
from instauto.api.client import ApiClient
from instauto.helpers.friendships import get_followers
from instauto.helpers.search import search_username, get_user_id_from_username

def main():
    if len(sys.argv) != 2:
        print("Usage:")
        print("{} <target_username>".format(sys.argv[0]))
        return

    target_username = sys.argv[1]
    target_username = target_username.replace("@", "")

    if os.path.isfile("savefile.instauto"):
        client = ApiClient.initiate_from_file("savefile.instauto")
    else:
        username = input("Username: ")
        password = input("Password: ")
        client = ApiClient(username=username, password=password)
        client.log_in()
        client.save_to_disk('savefile.instauto')

    print(client)

    user_id = get_user_id_from_username(client, target_username)
    
    #followers = get_followers(client, user_id, 100)
    #print(followers)

    # Based on:
    # https://github.com/stanvanrooy/instauto/blob/master/examples/api/friendships/get_followers.py
    obj = fs.GetFollowers(user_id)
    
    obj, response = client.followers_get(obj)

    followers = response.json()['users']
    print("Got {} followers".format(len(followers)))

    while True:
        obj, response = client.followers_get(obj)
        if not response:
            break

        new_followers = response.json()['users']
        print("Got {} followers".format(len(new_followers)))
        followers.extend(new_followers)

    if len(followers) == 0:
        return

    out_f = open("followers.csv", "w", encoding="utf-8")

    csv_writer = csv.DictWriter(out_f, fieldnames=list(followers[0].keys()), lineterminator="\n")
    csv_writer.writeheader()

    for f in followers:
        pprint(f)
        if f.get("linked_fb_info") is not None:
            del f['linked_fb_info']
        csv_writer.writerow(f)

    out_f.close()

if __name__ == "__main__":
    main()
