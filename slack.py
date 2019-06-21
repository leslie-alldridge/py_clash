import requests
from env import token

def sendSlack(file_name, url):
    print('sending to slack..')
    my_file = {
        'file' : ('./' + file_name, open('./' + file_name, 'rb'), 'png')
    }

    payload={
        "filename": file_name, 
        "token": token, 
        "channels":['#hi'], 
        "initial_comment": 'Lauren just replied on a thread: ' + url
    }

    r = requests.post("https://slack.com/api/files.upload", params=payload, files=my_file)
    if r.status_code == 200:
        print('Post to Slack successful')
    else:
        print('Failed to post to Slack')
