import csv
from email import header
from datetime import datetime as dt
comments = []
today = dt.today().strftime('%d-%m-%Y')


def process_comments(response_items, csv_output=False):

    for res in response_items:
        # handle replies : 리플라이가 있을 때 
        if 'replies' in res.keys():
            for reply in res['replies']['comments']:
                comment = reply['snippet']
                comment['commentId'] = reply['id']
                comments.append(comment)

        # handle non replies : 리플라이가 없을 때 
        else:
            comment={}
            comment['snippet']= res['snippet']['topLevelComment']['snippet']
            comment['snippet']['parentId'] = None
            comment['snippet']['commentId'] = res['snippet']['topLevelComment']['id']
            
            comments.append(comment['snippet'])

    if csv_output:
        make_csv(comments)
    print(f"finish processing, {len(comments)}. comments")
    # print(comments)
    return(comments)

def make_csv(comments, channelID= None):
    header = comments[0].keys()

    if channelID:
        filename = f'comments_{channelID}_{today}.csv'
    else:
        filename = f'comments_{today}.csv'

    with open(filename, 'w', encoding='utf-8', newline='')as f:
        writer = csv.DictWriter(f, fieldnames=header, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(comments)
    
    # f.close() 이렇게 닫으면 아마 계속 이어지게 쓰는게 아니라 비디오 별로 끊겨서 씨에스비 만들지 않을까?