import json
import subprocess


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
    if httpMethod == 'HEAD':
        # HEADはPCのみの挙動・・・だったらいいな
        print('Not GET')
        return returnRedirect(url)
    if not ('Android' in ua):
        # QuestのUAはstagefright/1.2 (Linux;Android 10)と予想
        print('Not Quest', ua)
        return returnRedirect(url)
    # TODO: キャッシュから読み込み(URL変わらないよね・・・？)
    b = exec_ytdlp_cmd(url)
    # j = json.loads(b)
    # formats = j['formats']
    # nama_url = ''
    # for f in formats:
    #     if f['ext'] == 'mp4' and f['url'] != '':
    #         print('url->'+f['url'])
    #         nama_url = f['url']
    nama_url = b
    print(nama_url)
    # TODO: キャッシュへ書き込み
    return returnRedirect(nama_url)


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
