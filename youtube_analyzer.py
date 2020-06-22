import os
import pandas as pd
import json
from youtube_api import YouTubeDataAPI


API_KEY = "AIzaSyAi82PNeweiFfnumFPu3VULJGl0zTffZtM"
yt = YouTubeDataAPI(API_KEY)

searches = yt.search(q='alexandra acasio-cortez',max_results=5)

print(searches[0])
