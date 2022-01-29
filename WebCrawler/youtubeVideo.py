import csv
import os
import pafy
import pandas as pd
from tqdm import tqdm

def get_video(df):
    for index, row in tqdm(df.iterrows(), total = df.shape[0]):
        try:
            v = pafy.new(row['url'])
            s = v.getbest()
            video_file = s.download()
            os.rename(v.title + '.mp4', str(row['id']) + '.mp4')
        except:
            pass

#list of unavailable videos 
def get_na_list(df):
    id_list = df['id']
    id_list = (id_list.apply(lambda x: str(x) + '.mp4'))
    id_list = id_list.to_list()
    youtube_videos = os.listdir()
    na_list = [i for i in video_pk_list if i not in youtube_videos]
    return na_list
  
def main():  
    df = pd.read_csv('youtube_url.csv')
    get_video(df)
    print(get_na_list(df))
