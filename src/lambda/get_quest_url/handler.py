import json
import subprocess
import boto3
import os
from datetime import datetime, timedelta

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['VRC_VIDEO_TABLE'])


def main(event, context):
    print('event:', event)
    httpMethod = event.get('httpMethod')
    print('httpMethod:', httpMethod)
    ua = event.get('headers').get('User-Agent', '')
    print('User-Agent:', ua)
    queryStringParameters = event.get('queryStringParameters')
    if queryStringParameters is None:
        return returnBadRequest()
    url = queryStringParameters.get('url')
    if url is None:
        return returnBadRequest()
    # if httpMethod == 'HEAD':
    #     # HEADはPCのみの挙動・・・だったらいいな
    #     print('Not GET')
    #     return returnRedirect(url)
    if not ('Android' in ua):
        # QuestのUAはstagefright/1.2 (Linux;Android 10)と予想
        print('Not Quest', ua)
        return returnRedirect(url)
    quest_url = ddbGetQuestURL(url)
    if quest_url is not None:
        print('use DynamoDB record')
        return returnRedirect(quest_url)
    b = exec_ytdlp_cmd(url)
    quest_url = b.decode()
    print(quest_url)
    ddbRegistQuestURL(url, quest_url)
    return returnRedirect(quest_url)


def returnBadRequest():
    return {
        'headers': {
            "Access-Control-Allow-Origin": "*"
        },
        'statusCode': 400,
        'body': json.dumps(
            {
                'result': 'NG',
                'error': 'bad request [1]'
            }
        )
    }


def returnRedirect(url):
    return {
        'headers': {
            "Content-type": "text/html; charset=utf-8",
            "Access-Control-Allow-Origin": "*",
            "location": url
        },
        'statusCode': 302,
        'body': "",
    }


def exec_ytdlp_cmd(url):
    # yt-dlp -i -q --no-warnings --no-playlist -g https://www.youtube.com/watch?v=xxxxxxxx
    cp = subprocess.run(
        ["/var/task/src/lambda/get_quest_url/yt-dlp", '-i', '-q', '--no-warnings', '--no-playlist', '-f', 'b', '-g', url], capture_output=True)
    print("stdout:", cp.stdout)
    return cp.stdout


# URLがDynamoDBにあるか確認し存在するならURLを返却
def ddbGetQuestURL(url):
    response = table.get_item(
        Key={
            'user_id': 'quest_url',
            'video_id': f'{url}',
        }
    )
    record = response.get('Item')
    if record is None:
        return None
    return record.get('quest_url')


# URLをキーにURLを登録(TTL付き)
def ddbRegistQuestURL(yt_url, quest_url):
    table.put_item(
        Item={
            'user_id': 'quest_url',
            'video_id': yt_url,
            'quest_url': quest_url,
            'TTL': get_ttl()
        }
    )


def get_ttl():
    start = datetime.now()
    expiration_date = start + timedelta(minutes=15)
    return round(expiration_date.timestamp())
