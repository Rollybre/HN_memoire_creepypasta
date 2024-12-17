import httpx
import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import time


API_KEY= 'AIzaSyDckNaLzMik92n5eVnYFmjwKqCL8HBSxEc '
id_se='02bcb702ebe6f46d7'
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]


def google_search(q): 
    base_url = 'https://www.googleapis.com/customsearch/v1?'
    params={
        'key': API_KEY,
        'cx':id_se,
        'q': q
    }
    response = httpx.get(base_url,params=params)
    response.raise_for_status()
    time.sleep(1)
    return response.json()



def get_number_result(q:str) -> int: 
    """
    donne le nombre de résultat d'une recherche google
    """
    res=google_search(q)
    return res['searchInformation']['totalResults']



# API client library
import googleapiclient.discovery

def youtube_info_request(kw:str) :
    # API information
    api_service_name = "youtube"
    api_version = "v3"


    youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey = API_KEY)
    # 'request' variable is the only thing you must change
    # depending on the resource and method you need to use
    # in your query
    request = youtube.search().list(
        part='id,snippet',
        type='video',
        q=kw,
        maxResults=20,
        order="viewCount",
        fields="pageInfo,items(id(videoId),snippet(publishedAt,channelId,channelTitle,title,description))"
    )
    # Query execution
    response = request.execute()
    return response

def youtube_stats_info(id) : 
    # API information
    api_service_name = "youtube"
    api_version = "v3"
    youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey = API_KEY)

    r = youtube.videos().list(
        part="snippet,statistics,contentDetails",
        id=id,
        fields="items(snippet(title)," + \
                    "statistics," + \
                     "contentDetails(duration))").execute()
    return r


if __name__ == '__main__': 
    #res=google_search('scp 173')
    #print(res)
    print(youtube_info_request('skibidi'))