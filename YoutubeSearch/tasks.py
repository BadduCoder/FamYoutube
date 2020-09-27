from googleapiclient.discovery import build
from datetime import datetime, timedelta
from .models import VideoData, Thumbnails


def insert_video(videoId, rowData):
    """
    Function receives videoId, and other video details,
    Inserts them into the database.
    Returns the instance created in database.
    """
    videoData = VideoData(
        id = videoId,
        title = rowData['title'],
        description = rowData['description'],
        channelTitle = rowData['channelTitle'],
        publishedAt = rowData['publishedAt'],
    )
    videoData.save()

    return videoData


def insert_thumbnail(thumbnail, thumbnail_type, video):
    """
    Function receives thumbnail data, thumbnail type and instance of parent video,
    It inserts them into database and links the item to it's parent video.
    """
    thumbnail = Thumbnails(
        thumbnail_type = thumbnail_type,
        video = video,
        height = thumbnail['height'],
        width = thumbnail['width'],
        url = thumbnail['url']
    )

    thumbnail.save()


def populate_data(itemsData):
    """
        Input: List of video data response from youtube
        This function receives list of video data and inserts them into the database 
    """
    for item in itemsData:
        #Insert video data into database
        video = insert_video(item['id']['videoId'], item['snippet'])
        
        #If video has been inserted, insert it's thumbnails
        if video is False:
            return False
        else:    
            thumbnail = insert_thumbnail(item['snippet']['thumbnails']['default'], 'DE', video)
            thumbnail = insert_thumbnail(item['snippet']['thumbnails']['medium'], 'ME', video)
            thumbnail = insert_thumbnail(item['snippet']['thumbnails']['high'], 'HI', video)
    return True    


def fetch_data(request):
    """
        Input: None
        This function fetches all the videos published with specific term in there title/description
        for every 10 seconds in background.
    """
    #Get current datetime, convert it to timestamp of 10 seconds before.
    now = datetime.now() - timedelta(seconds=10)
    timestamp = now.strftime('%Y-%m-%dT%H:%M:%SZ')
    
    #create the object, fetch collection and execute
    service = build('youtube','v3',developerKey='insert-key-here')
    collection = service.search().list(part=['id','snippet'],q='prank', type='video', order='date', publishedAfter=timestamp)
    response = collection.execute()
    
    #If list contains items, populate database
    if len(response['items']) > 0:
        return populate_data(response['items'])

    return False
