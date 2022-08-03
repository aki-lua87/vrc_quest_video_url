import json
import subprocess


def main(event, context):
    print('event:', event)
    httpMethod = event.get('httpMethod')
    print('httpMethod:', httpMethod)
    queryStringParameters = event.get('queryStringParameters')
    if queryStringParameters is None:
        return returnBadRequest()
    url = queryStringParameters.get('url')
    if url is None:
        return returnBadRequest()
    b = exec_ytdlp_cmd(url)
    j = json.loads(b)
    id = j['id']
    print(id)
    formats = j['formats']
    aaa = ''
    for f in formats:
        print(f['url'])
        aaa = f['url']
    return {
        'headers': {
            "Content-type": "text/html; charset=utf-8",
            "Access-Control-Allow-Origin": "*",
            "location": aaa
        },
        'statusCode': 302,
        'body': "",
    }


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


def exec_ytdlp_cmd(url):
    cp = subprocess.run(
        ["/var/task/src/lambda/get_quest_url/yt-dlp", "-J", url], capture_output=True)
    print("stdout:", cp.stdout)
    return cp.stdout
