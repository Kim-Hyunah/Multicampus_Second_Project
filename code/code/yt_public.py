import sys
# print("--sys.version—")
# print(sys.version)

import pandas
from googleapiclient.discovery import build

import warnings

warnings.filterwarnings('ignore')

from googleapiclient.errors import HttpError

import csv
from datetime import datetime as dt

import os
from dotenv import load_dotenv

from utils.comments import make_csv, process_comments

from iteration_utilities import unique_everseen

load_dotenv()
API_KEY = os.getenv("myServiceKey")

YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
DEVELOPER_KEY = API_KEY

youtube = build('youtube', 'v3', developerKey = API_KEY)

def comment_threads(channelID, to_csv=False):
    # comments=[] 이렇게 하면 혹시 중복해서 계속 더해지는거 해결될까...?
    comments_list=[]

    request = youtube.commentThreads().list( 
        part = 'id,replies,snippet',
        # order='relevance',
        videoId = channelID,
        # maxResults=2

    )

    response = request.execute()
    print(response)

    comments_list.extend(process_comments(response['items']))
    
    #print(len(response['items']))
    #print(comments_list)

    while response.get('nextPageToken', None):    # 아직 다음 페이지 있을 때 
        request = youtube.commentThreads().list( 
            part = 'id,replies,snippet',
            videoId = channelID,
            pageToken=response['nextPageToken']
        )

        response = request.execute()
        comments_list.extend(process_comments(response['items']))
    comments_list = list(unique_everseen(comments_list))
    print(f"finished fetching comments for {channelID}. {len(comments_list)} comments found")

    if to_csv:
        make_csv(comments_list, channelID)

    return comments_list

def main():
    comment_threads('eHX82A3JC88', to_csv=True)

if __name__ == "__main__":
    main()

# if __name__ == "__main__"을 사용하면 C:\doit>python mod1.py처럼 직접 이 파일을 실행했을 때는 __name__ == "__main__"이 참이 되어 if문 다음 문장이 수행된다. 반대로 대화형 인터프리터나 다른 파일에서 이 모듈을 불러서 사용할 때는 __name__ == "__main__"이 거짓이 되어 if문 다음 문장이 수행되지 않는다.
#__name__ 변수란? 파이썬의 __name__ 변수는 파이썬이 내부적으로 사용하는 특별한 변수 이름이다. 만약 C:\doit>python mod1.py처럼 직접 mod1.py 파일을 실행할 경우 mod1.py의 __name__ 변수에는 __main__ 값이 저장된다. 하지만 파이썬 셸이나 다른 파이썬 모듈에서 mod1을 import 할 경우에는 mod1.py의 __name__ 변수에는 mod1.py의 모듈 이름 값 mod1이 저장된다.
