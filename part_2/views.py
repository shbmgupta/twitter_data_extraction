# # -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import pandas as pd
from part_1.models import AppKeys
import tweepy
from twython import Twython
import json
import pprint
from datetime import datetime
from tweepy.parsers import RawParser
import time

appKeys = AppKeys.objects.all().order_by('-id')[0]
consumer_key = appKeys.CustomerKey
consumer_secret = appKeys.CustomerSecretKey
access_token = appKeys.AccessTokenKey
access_token_secret = appKeys.AccessTokenSecret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_count=3, retry_delay=60)
RawParser = RawParser()

def read_username(filename):        #give the filename of the users who u want to follow

    username = []
    with open (filename) as f:
        for line in f:
            line = line.strip()
            username.append(line)
    return username

def send_direct_message(dest, msg):
        event = {
            "event": {
                "type": "message_create",
                "message_create": {
                    "target": {
                        "recipient_id": dest
                    },
                    "message_data": {
                        "text": msg
                    }
                }
            }
        }
        api.send_direct_message_new(event)


def send_messages(list1, usernames, msg):
    twitter = Twython(consumer_key, consumer_secret, access_token, access_token_secret)
    for username in usernames:
        print (username)
        try:
            if len(username) > 0:
                try:
                    # output = twitter.lookup_user(screen_name=username)
                    # userid =  output[0]["id_str"]
                    userid = int(username)
                    list1.append(username)
                    # userid = int(userid)
                    send_direct_message(dest = userid, msg = msg)
                    print ("message sent")
                except:
                    print ("message not sent for 1")
            else:
                continue
        except tweepy.TweepError as e:
            print (e)
            list2.append(username)
            print ("User not your friend")
            continue


def comment_on_profile(list1, usernames, comment):
    twitter = Twython(consumer_key, consumer_secret, access_token, access_token_secret)
    for username in usernames:
        if len(username) > 0:
            list1.append(username)
            print (username)
            m = "@%s " %(username)
            m = m + comment
            s= api.update_status(m)
    return

def reply_to_tweet(userid, count, messages):
    tweet_ids = []
    user = api.get_user(userid)
    user_name = user.screen_name
    user_name = str(user_name)
    print (userid)
    status_list = api.user_timeline(user_id = userid, count = count)
    for status in status_list:
        tweet_ids.append(status.id_str)

    for i in range(len(tweet_ids)):
        print (tweet_ids[i])
        reply_status = "@%s %s" % (user_name, messages[i])
        api.update_status(reply_status, tweet_ids[i])

def sendMessage(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save('media/document/'+ myfile.name, myfile)
        usernames = read_username(filename)
        list1 = []
        list2 = []
        message = request.POST.get('message')
        send_messages(list1, usernames = usernames, msg = message)
        return render(request, 'part_2/sentMessage.html', {
        'message': message,
        'list1': list1,
        'list2': list2
        })
    else:
        return render(request, 'part_2/sendMessage.html')

def sendComment(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save('media/document/'+ myfile.name, myfile)
        usernames = read_username(filename)
        list1 = []
        comment = request.POST.get('message')
        comment_on_profile(list1, usernames, comment)
        return render(request, 'part_2/sentComment.html', {
        'message': comment,
        'list1': list1
        })
    else:
        return render(request, 'part_2/sendMessage.html')

def sendCommentTopFive(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save('media/document/'+ myfile.name, myfile)
        usernames = read_username(filename)
        list1 = []
        reply1 = request.POST.get('message1')
        reply2 = request.POST.get('message2')
        reply3 = request.POST.get('message3')
        reply4 = request.POST.get('message4')
        reply5 = request.POST.get('message5')
        sleep = request.POST.get('sleep')
        reply_list = [reply1, reply2, reply3, reply4, reply5]
        for username in usernames:
            reply_to_tweet(username, 5, reply_list)
            time.sleep(int(sleep))
        return render(request, 'part_2/sentComment5.html', {
        'usernames': usernames,
        })
    else:
        return render(request, 'part_2/sendMessage.html')
