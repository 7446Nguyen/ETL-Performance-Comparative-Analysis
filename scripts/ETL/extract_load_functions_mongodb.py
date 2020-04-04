# Import packages for use
import pandas as pd
import mysql.connector
import time
import psutil
import cudf


def extraction(item, iterations, exportLocation,exportFilename):
    # LIGHT EXTRACTION #
    ###################################################################################################################
    ### Pull item table and capture CPU, RAM and elapsed time to perform operations

    ### light extraction performance metrics
    column_names = ["CPU_utilization", "RAM_utilization", "elapsed_time"]
    lightExtractionPrfm = pd.DataFrame(columns = column_names)

    extractionTimerStart = time.perf_counter()
    ### Run 30 iterations to collect a df of performance metrics
    ### light extraction performance metrics
    column_names = ["CPU_utilization", "RAM_utilization", "elapsed_time"]
    lightExtractionPrfm = pd.DataFrame(columns = column_names)

    ### base metrics
    print("STARTING EXTRACTION...")
    print("Base CPU utilization: ", psutil.cpu_percent())
    print("Base RAM utilization: ", psutil.virtual_memory().percent)
    print("RUNNING...")

    ### Run n iterations to collect a df of performance metrics
    for sampleNo in range(iterations):

        #Initiate timer for query
        start = time.perf_counter()
    
        #insert data into dataFrame
        Extraction = pd.DataFrame(list(item.find()))
    
        #Stop timer  
        stop = time.perf_counter()
    
        #load df with performance metrics    
        lightExtractionPrfm = lightExtractionPrfm.append(pd.DataFrame({'CPU_utilization': psutil.cpu_percent(),
                                                                       'RAM_utilization':  psutil.virtual_memory().percent,
                                                                       'elapsed_time': stop - start}, 
                                                                       index=[1]), ignore_index=True)
        time.sleep(2)
    extractionTimerEnd= time.perf_counter()   

    print("Data frame loading complete.\n")
    print("Total EXTRACTION time: ", extractionTimerEnd - extractionTimerStart, "s")
    print("Iterations performed: ", iterations)
    print("Average EXTRACTION iteration time: ", lightExtractionPrfm.elapsed_time.mean(), "s")
    print("Average CPU utilization: ", lightExtractionPrfm.CPU_utilization.mean())
    print("Average RAM utilization: ", lightExtractionPrfm.RAM_utilization.mean(),"\n\n")
    
    #Export DF to csv
    lightExtractionPrfm.to_csv (exportLocation+exportFilename, index = False, header=True)
    return Extraction


def loading(client, table, transformationDf, loopIterations,exportLocation,exportFilename):
    #Connect to datalake
    from pymongo import MongoClient
    db = client['datalake']


    # Write dataframe to datalake
    #Create df to collect performance metrics
    column_names = ["CPU_utilization", "RAM_utilization", "elapsed_time"]
    lightLoadPrfm = pd.DataFrame(columns = column_names)
    print('STARTING LOAD...')
    print("Base CPU utilization: ", psutil.cpu_percent())
    print("Base RAM utilization: ", psutil.virtual_memory().percent)
    print('RUNNING...')

    #Run 30 iterations to collect loading performance metrics
    loadIter = loopIterations
    loadTimerStart = time.perf_counter()

    transformationDf.reset_index(inplace=True)
    data_dict = transformationDf.to_dict("records")# Insert collection
    for sampleNoTransform in range(loadIter):

        # Start Timer and progress tracker
        start = time.perf_counter()
        collection = db[table]

        #Working Code

        collection.insert_many(data_dict)

        #Stop timer  
        stop = time.perf_counter()
        db.drop_collection(collection)

        lightLoadPrfm = lightLoadPrfm.append(pd.DataFrame({'CPU_utilization': psutil.cpu_percent(),
                                                           'RAM_utilization':  psutil.virtual_memory().percent,
                                                           'elapsed_time':stop - start},
                                                           index=[1]), ignore_index=True)

        time.sleep(2)
    loadTimerEnd = time.perf_counter() 
    collection = db[table]
    collection.insert_many(data_dict)

    #load data into datalake for use.

    print("Loading metrics captured loading complete.\n")
    print("Total LOADING time: ", loadTimerEnd - loadTimerStart, "s")
    print("Iterations performed: ", loadIter)
    print("Average LOADING iteration time: ", lightLoadPrfm.elapsed_time.mean(), "s")
    print("Average LOADING CPU utilization: ", lightLoadPrfm.CPU_utilization.mean())
    print("Average LOADING RAM utilization: ", lightLoadPrfm.RAM_utilization.mean(),"\n\n")

    #Export DF to csv
    lightLoadPrfm.to_csv (exportLocation+exportFilename, index = False, header=True)
