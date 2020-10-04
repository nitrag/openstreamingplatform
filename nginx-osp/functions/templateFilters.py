from urllib.parse import urlparse
import time
import os
import json

from globals import globalvars

from classes import Sec
from classes import topics

def init(context):
    context.jinja_env.filters['normalize_uuid'] = normalize_uuid
    context.jinja_env.filters['normalize_urlroot'] = normalize_urlroot
    context.jinja_env.filters['normalize_url'] = normalize_url
    context.jinja_env.filters['normalize_date'] = normalize_date
    context.jinja_env.filters['limit_title'] = limit_title
    context.jinja_env.filters['format_kbps'] = format_kbps
    context.jinja_env.filters['hms_format'] = hms_format
    context.jinja_env.filters['get_topicName'] = get_topicName
    context.jinja_env.filters['get_userName'] = get_userName
    context.jinja_env.filters['get_pictureLocation'] = get_pictureLocation
    context.jinja_env.filters['get_diskUsage'] = get_diskUsage
    context.jinja_env.filters['testList'] = testList
    context.jinja_env.filters['get_webhookTrigger'] = get_webhookTrigger
    context.jinja_env.filters['get_logType'] = get_logType
    context.jinja_env.filters['format_clipLength'] = format_clipLength
    context.jinja_env.filters['processClientCount'] = processClientCount


#----------------------------------------------------------------------------#
# Template Filters
#----------------------------------------------------------------------------#

def normalize_uuid(uuidstr):
    return uuidstr.replace("-", "")

def normalize_urlroot(urlString):
    parsedURLRoot = urlparse(urlString)
    URLProtocol = None
    if parsedURLRoot.port == 80:
        URLProtocol = "http"
    elif parsedURLRoot.port == 443:
        URLProtocol = "https"
    else:
        URLProtocol = parsedURLRoot.scheme
    reparsedString = str(URLProtocol) + "://" + str(parsedURLRoot.hostname)
    return str(reparsedString)

def normalize_url(urlString):
    parsedURL = urlparse(urlString)
    if parsedURL.port == 80:
        URLProtocol = "http"
    elif parsedURL.port == 443:
        URLProtocol = "https"
    else:
        URLProtocol = parsedURL.scheme
    reparsedString = str(URLProtocol) + "://" + str(parsedURL.hostname) + str(parsedURL.path)
    return str(reparsedString)

def normalize_date(dateStr):
    return str(dateStr)[:19]

def limit_title(titleStr):
    if len(titleStr) > 40:
        return titleStr[:37] + "..."
    else:
        return titleStr

def format_kbps(bits):
    bits = int(bits)
    return round(bits/1000)

def hms_format(seconds):
    val = "Unknown"
    if seconds is not None:
        seconds = int(seconds)
        val = time.strftime("%H:%M:%S", time.gmtime(seconds))
    return val

def format_clipLength(seconds):
    if int(seconds) == 301:
        return "Infinite"
    else:
        return hms_format(seconds)

def get_topicName(topicID):
    topicID = int(topicID)
    if topicID in globalvars.topicCache:
        return globalvars.topicCache[topicID]
    return "None"

def get_userName(userID):
    userQuery = Sec.User.query.filter_by(id=int(userID)).first()
    if userQuery is None:
        return "Unknown User"
    else:
        return userQuery.username


def get_pictureLocation(userID):
    userQuery = Sec.User.query.filter_by(id=int(userID)).first()
    pictureLocation = None
    if userQuery.pictureLocation is None:
        pictureLocation = '/static/img/user2.png'
    else:
        pictureLocation = '/images/' + userQuery.pictureLocation

    return pictureLocation

def get_diskUsage(channelLocation):
        videos_root = globalvars.videoRoot + 'videos/'
        channelLocation = videos_root + channelLocation

        total_size = 0
        for dirpath, dirnames, filenames in os.walk(channelLocation):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        return "{:,}".format(total_size)

def testList(obj):
    if type(obj) == list:
        return True
    else:
        return False

def processClientCount(data):
    count = 0
    if type(data) == list:
        for client in data:
            if 'flashver' in client:
                if client['flashver'] != 'ngx-local-relay':
                    count = count + 1
    else:
        count = 1
    return count

def get_webhookTrigger(webhookTrigger):

    webhookTrigger = str(webhookTrigger)
    webhookNames = {
        '0': 'Stream Start',
        '1': 'Stream End',
        '2': 'Stream Viewer Join',
        '3': 'Stream Viewer Upvote',
        '4': 'Stream Name Change',
        '5': 'Chat Message',
        '6': 'New Video',
        '7': 'Video Comment',
        '8': 'Video Upvote',
        '9': 'Video Name Change',
        '10': 'Channel Subscription',
        '20': 'New User'
    }
    return webhookNames[webhookTrigger]

def get_logType(logType):

    logType = str(logType)
    logTypeNames = {
        '0': 'System',
        '1': 'Security',
        '2': 'Email',
        '3': 'Channel',
        '4': 'Video',
        '5': 'Stream',
        '6': 'Clip',
        '7': 'API',
        '8': 'Webhook',
        '9': 'Topic',
        '10': 'Hub'
    }
    return logTypeNames[logType]