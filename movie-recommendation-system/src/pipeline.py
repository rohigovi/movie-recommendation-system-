'''
1) Fetch data from kafka and store into csv file
2) Read that file for cleaning and store the file csv
3) Perform hit_rate and latency evaluation
4) Perform training on all files 
5) Generate model and store pickle file
'''
import argparse
from datetime import datetime,timedelta
import data_fetch as dataFetch
import data_clean as dataClean
import hit_rate as hitRate
import Modelling as modelFile
# import Modelling as modelFile

KAFKA_LOG_DIR = "logs/"
KAFKA_LOG_NAME = "kafka_data"
TIMESTAMP_FILE = "pipeline_timestamp.txt"

def getPrevTimestamp(filename):
    try:
        f = open(filename, "r")
    except:
        return -1
    lines = f.readlines()
    if len(lines) != 1 :
        return -1
    time_stamp =float(lines[0])
    date_time = datetime.fromtimestamp((time_stamp))
    f.close()
    return date_time
    
def saveTimestamp(currentTime, filename):
    timestamp = datetime.timestamp(currentTime)
    try:
        f = open(filename, "w")
    except:
        return -1
    f.write(str(timestamp))
    f.close()

def pipeline_data_collection():
        prevTimeStamp = getPrevTimestamp(TIMESTAMP_FILE)
        if prevTimeStamp == -1:
            exit()
        curTimeStamp = datetime.now()
        diffSeconds = abs(curTimeStamp - prevTimeStamp).seconds
        kafkaLog = KAFKA_LOG_DIR + KAFKA_LOG_NAME + "_" + str(curTimeStamp.date()) + ".log"
        print(diffSeconds, " ", kafkaLog)
        
        # Data fetch step 
        retKafka = dataFetch.fetchDataKafka(kafkaLog, "latest", diffSeconds)
        if retKafka == False:
            exit()

        # Data clean step
        success_count, error_count, watched_path, recs_path = dataClean.data_clean(kafkaLog)

        # Telemetry collection
        hitRate.calculateMetrics(watched_path, recs_path)
        saveTimestamp(curTimeStamp,TIMESTAMP_FILE)
def pipeline_modelling():
    modelFile.main()

def main():
    parser = argparse.ArgumentParser(description='Pipeline')
    parser.add_argument("--data_collection", help="Run Data collection and telemetry", action="store_true")
    parser.add_argument("--train", help="Run model training and creation.", action="store_true")
    parser.add_argument("--full_pipeline", help="Run complete pipeline.", action="store_true")
    args = parser.parse_args()

    if args.full_pipeline:
        pipeline_data_collection()
        pipeline_modelling()

    if args.data_collection:
        pipeline_data_collection()

    if args.train:
        pipeline_modelling()

if __name__ == "__main__":
    main()