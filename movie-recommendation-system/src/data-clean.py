import re
import pandas as pd
from collections import defaultdict
import timeit
from schema import Schema
import datetime


# <time>,<userid>,recommendation request <server>, status <200 for success>, result: <recommendations>, <responsetime>
# <time>,<userid>,GET /data/m/<movieid>/<minute>.mpg
# <time>,<userid>,GET /rate/<movieid>=<rating>
def validate_date(date_text):
    """ Returns True is date is a valid date """
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%dT%H:%M:%S')
        return True
    except ValueError:
        return False

def validate_integer(user_id_text):
    """ Returns True is string is a number > 0 """
    return user_id_text.isdigit()

def validate_request(request_text):
    if 'GET /data/m/' in request_text:

        try :
            parsed = re.split("\/(.*)\/(.*)\/(.*)\.",request_text)
            
            # Check if movie watched minute is an integer > 0
            if validate_integer(parsed[3]):
                return True
            else: 
                return False  

        except:
            return False


    elif 'GET /rate/' in request_text:
        
        try :
            parsed = re.split("=",re.split("\/",request_text)[2])
            
            # Check if rating is an integer
            if validate_integer(parsed[1]) and 0<int(parsed[1])<=5:
                return True
            else: 
                return False 

        except:
            return False 

    else:
        return False            

def data_quality_check(line):
    # Number of data cols in the line
    line_data = line.strip().split(",")
    
    if len(line_data) == 3:
        
        if validate_date(line_data[0]) and validate_integer(line_data[1]) \
        and validate_request(line_data[2]):
            return True
        else: 
            return False    
        
    
    elif len(line_data) == 3:
        schema2 = Schema([{'timestamp': str,
            'userid': str, 
            'rec_request': str,
            'status': str,
            'result': str}]) 
    
    else:
        return False        
    
    

    # Check the data type for each col
    # 
    #  


def data_clean(file_name):

    start = timeit.default_timer()
    dct1,dct2,idx = defaultdict(),{},0
    
    error_count = 0

    watch_cols = ["userid","movieid","date","time","minutes"]
    rate_cols = ["userid","movieid","date","time","rating"]
    
    # Open kafka consumer file in read mode
    with open(file_name, 'r') as fp:
        for line in fp:
            
            # Quality check
            if data_quality_check(line) == False:
                error_count+=1
                continue

            # watching
            if 'GET /data/m/' in line:
                # Simple parsing: date, time, userid
                ts,user,log = line.strip().split(",")
                day,time = ts.split("T")

                # parse system log to get <movieid> & <watching_minute>
                parsed = re.split("\/(.*)\/(.*)\/(.*)\.",log)
                print(parsed)
                movie,minutes = parsed[2],parsed[3]

                # (1) if we want to get all movie logs
                # lst = [d,t,user,movieid,minutes]
                # row_dict = dict(zip(watch_cols, lst))

                # (2) if we want to keep only one record for each watching
                ks = ','.join([user,movie,day])
                vs = ','.join([time,minutes])

                if ks not in dct1:
                    dct1[ks] = vs
                else:
                    # get the duration of watching: keep the maximum number of minutes here
                    if minutes > dct1.get(ks):
                        dct1[ks] = vs
            # rating
            if 'GET /rate/' in line:
                # Simple parsing: date, time, userid
                ts,user,log = line.strip().split(",")
                day,time = ts.split("T")

                # parse system log to get <movieid> & <rating>
                parsed = re.split("=",re.split("\/",log)[2])
                movieid,rating = parsed[0],parsed[1]

                # append result to the dictionary
                lst = [user,movieid,day,time,rating]
                row_dict = dict(zip(rate_cols, lst))
                dct2[idx] = row_dict
                idx += 1

    values = [('{},{}'.format(key, value)).split(",") for key, value in dct1.items()]
    watch_df = pd.DataFrame(values, columns = watch_cols)
    rate_df = pd.DataFrame.from_dict(dct2, orient='index')

    # inner join two tables for user BOTH watched AND rated the movie
    both_df = pd.merge(
                    watch_df, 
                    rate_df, 
                    how="inner", 
                    on=["userid", "movieid"],
                    suffixes=('_watch','_rate'))

    # output to file
    watch_df.to_csv("watched.csv",sep=",",index=False)
    rate_df.to_csv("rated.csv",sep=",",index=False)
    both_df.to_csv("watched_rated_df.csv",sep=",",index=False)

    stop = timeit.default_timer()
    print('Time: ', stop - start)  