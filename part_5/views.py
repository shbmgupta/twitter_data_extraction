from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from part_1.forms import DocumentForm, AppKeysForm
import pandas as pd
from part_1.models import AppKeys
import tweepy
from twython import Twython


def get_followers_ids(user_id, consumer_key, consumer_secret, access_token, access_token_secret, api):
    ids = []
    page_count = 0
    for page in tweepy.Cursor(api.friends_ids, id=user_id, count=5000).pages():
        page_count += 1
        print ('Getting page {} for followers ids'.format(page_count))
        ids.extend(page)
        if len(ids) > 200 :
            break
        print ("0")
        if len(ids) == 0:
            break

        if page_count > 3:
            break

    return ids[:200]






def read_username(filename):
    username = []
    with open (filename) as f:
        for line in f:
            line = line.strip()
            username.append(line)
    return username

def simple_upload2(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        username = fs.save('media/document/'+ myfile.name, myfile)
        # print(username)
        uploaded_file_url = fs.url(username)
        usernames = read_username(username)
        #user = api.get_user(screen_name = username)
        #print (user)
        # namelist = []
        dictio = {}
        appKeys = AppKeys.objects.all().order_by('-id')[0]
        consumer_key = appKeys.CustomerKey
        consumer_secret = appKeys.CustomerSecretKey
        access_token = appKeys.AccessTokenKey
        access_token_secret = appKeys.AccessTokenSecret
        #AppKeys.objects.all().delete()

        # consumer_key = "c8y3bCLMg7a0YHdu9COojWHuV"
        #
        # consumer_secret = "mqQAcex01SdYsghMEpCASik9xt7CDgQsaJekLzQ9j7Sf6kEJlA"
        #
        # access_token = "746216532242399232-80x2w2prAxnZQ5UM1nc14zWsTpibAUc"
        #
        # access_token_secret = "41GS8NMnAKkINhyZq2cBX35ueAcS5ys82QiVxea6CL09A"

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_count=3, retry_delay=60)
        file_url = []
        list1 = []
        dictio = {}
        for username in usernames:
            if len(username) != 0:
                print (username)
                file_url.append(fs.url('media/document/'+username+ "_following" + ".txt"))
                print('hi')
                print(file_url)
                print('bye')
                # twitter = Twython(consumer_key, consumer_secret, access_token, access_token_secret)
                # output = twitter.lookup_user(screen_name=username)
                # userid =  output[0]["id_str"]
                # userid = int(userid)
                name_of_user = api.get_user(int(username))
                name_of_user = name_of_user.screen_name
                print (name_of_user)
                userid = int(username)
                ids = get_followers_ids(userid, consumer_key, consumer_secret, access_token, access_token_secret,api)
                list2=[]
                file_to_write = 'media/document/'+ username + "_following" + ".txt"
                print(file_to_write)
                # list10.append(file_to_write)
                # if len(ids)  > 0:
                with open (file_to_write, 'w') as f:
                    for id in ids:
                        try:
                            # id = api.get_user(id)
                            # id = id.screen_name
                            list2.append(str(id))
                            str_to_write = str(id) + "\n"
                            f.write(str_to_write)
                        except:
                            pass
            print ("Number of users found: " + str(len(ids)))
            list1.append(list2)
        dictio = dict(zip(file_url, list1))
        print(dictio)
        #print(uploaded_file_url)
        # return render(request, 'part_1/index.html', {
        #     'uploaded_file_url': uploaded_file_url
        #     })
        return render(request, 'part_5/followers.html', {
            'followers': dictio
            })
    return render(request, 'part_5/index.html')
