from googleapiclient.discovery import build

# Your YouTube API key (get it from Google Cloud Console -> Enable YouTube Data API v3)
API_KEY = "AIzaSyDi-6CMf-osZl_XdD1HEJ0oM__ODQNJMjo"

# Build the YouTube API client
youtube = build("youtube", "v3", developerKey=API_KEY)

def get_youtube_links(topics, level, max_results=5):
    query = f"{topics} {level}"

    # Perform YouTube search
    request = youtube.search().list(
        part="snippet",
        q=query,
        type="video",
        maxResults=max_results
    )
    response = request.execute()

    # Extract video links
    video_links = []
    for item in response.get("items", []):
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        link = f"https://www.youtube.com/watch?v={video_id}"
        video_links.append((title, link))

    return video_links
