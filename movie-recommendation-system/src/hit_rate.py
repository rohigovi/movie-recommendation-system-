from datetime import datetime,timedelta
import pandas as pd

def getFileToDf(input_file):
    df = pd.read_csv(input_file)
    return df

def updateWatchDate(movie_df_csv, hit_rate_data):
    movie_df_csv = movie_df_csv.head(10)
    for index, row in movie_df_csv.iterrows():
        timestamp = datetime.strptime(row['date_watch'], '%Y-%m-%d')
        isEntry = hit_rate_data.loc[(hit_rate_data['userid'] == row['userid']) & (hit_rate_data['movieid'] == row['movieid']) & (hit_rate_data['time'] <= timestamp)]
        # Entry found
        if isEntry.empty == False:
            hit_rate_data.loc[(hit_rate_data['userid'] == row['userid']) & (hit_rate_data['movieid'] == row['movieid']) & (hit_rate_data['time'] <= timestamp),'watched'] = True
    hit_rate_data['time']= pd.to_datetime(hit_rate_data['time'], format="%Y-%m-%d")
    return hit_rate_data

def getRecoRow(row, movie):
    new_row = {'userid':row['userid'], 'movieid':str(movie),'time':row['date'],'watched':False}
    return new_row

def updateRecoData(hit_rate_data, newRecos):
    for index, row in newRecos.iterrows():
        recoMovies = row['movielist'].strip().split(',')
        for movie in recoMovies:
            movie = movie.strip()      
            isEntry = hit_rate_data.loc[(hit_rate_data['userid'] == row['userid']) & (hit_rate_data['movieid'] == movie)]
            if isEntry.empty:
                new_row = getRecoRow(row, movie)
                #append row to the dataframe
                new_row = pd.DataFrame([new_row])
                hit_rate_data = pd.concat([hit_rate_data, new_row], ignore_index=True)
                # hit_rate_data = hit_rate_data.append(new_row, ignore_index = True)
    hit_rate_data['time']= pd.to_datetime(hit_rate_data['time'], format="%Y-%m-%d")
    return hit_rate_data

def getHitMetric(hit_rate_data):
    totalSize = len(hit_rate_data)
    res = hit_rate_data['watched'].value_counts()
    # res = hit_rate_data.groupby('watched').count()
    return dict(res)

def getLatencyMetric(newRecos):
    cnt = 0
    lat = 0
    for index, row in newRecos.iterrows():
        lat += row['latency']
        cnt+=1
    return (lat/cnt)


    
