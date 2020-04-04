# Import packages for use
import pandas as pd
import mysql.connector
import time
import psutil
import cudf


def extraction(connection, sqlscript, loopIterations, exportLocation,exportFilename):
    # LIGHT EXTRACTION #
    ###################################################################################################################
    ### Pull item table and capture CPU, RAM and elapsed time to perform operations

    ### light extraction performance metrics
    column_names = ["CPU_utilization", "RAM_utilization", "elapsed_time"]
    lightExtractionPrfm = pd.DataFrame(columns = column_names)

    ### base metrics
    print("\nSTARTING EXTRACTION...")
    print("Base EXTRACTION CPU utilization: ", psutil.cpu_percent())
    print("Base EXTRACTION RAM utilization: ", psutil.virtual_memory().percent)
    print("RUNNING...")

    extractionTimerStart = time.perf_counter()
    ### Run 30 iterations to collect a df of performance metrics
    iterations = loopIterations
    for sampleNo in range(iterations):
        #script to pull data
        LEsql = sqlscript

        #Initiate timer for query
        start = time.perf_counter()

        #insert data into dataFrame
        orderItemJoin = pd.read_sql(sql=LEsql, con=connection)

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
    lightExtractionPrfm.to_csv (exportLocation + exportFilename, index = False, header=True)
    return orderItemJoin


def loading(transformationDf,tablename, loopIterations,exportLocation,exportFilename):
    #Connect to datalake
    from sqlalchemy import create_engine
    dl = create_engine('mysql+mysqlconnector://root:0861137MySQL!@127.0.0.1/datalake', echo=False)

    # Write dataframe to datalake
    #Create df to collect performance metrics
    column_names = ["CPU_utilization", "RAM_utilization", "elapsed_time"]
    lightLoadPrfm = pd.DataFrame(columns = column_names)
    print('STARTING LOAD...')
    print('Load database connection is: ',dl)
    print("Base CPU utilization: ", psutil.cpu_percent())
    print("Base RAM utilization: ", psutil.virtual_memory().percent)
    print('RUNNING...')

    #Run 30 iterations to collect loading performance metrics
    loadIter = loopIterations
    loadTimerStart = time.perf_counter()
    for sampleNoTransform in range(loadIter):

        # Start Timer and progress tracker
        start = time.perf_counter()

        #Working Code
        transformationDf.to_sql(tablename, con=dl, if_exists='replace',index=False)

        #Stop timer  
        stop = time.perf_counter()

        lightLoadPrfm = lightLoadPrfm.append(pd.DataFrame({'CPU_utilization': psutil.cpu_percent(),
                                                           'RAM_utilization':  psutil.virtual_memory().percent,
                                                           'elapsed_time':stop - start},
                                                           index=[1]), ignore_index=True)

        time.sleep(2)
    loadTimerEnd = time.perf_counter() 
   

    #load data into datalake for use.
    print("Loading complete.")

    print("Loading metrics captured loading complete.\n")
    print("Total LOADING time: ", loadTimerEnd - loadTimerStart, "s")
    print("Iterations performed: ", loadIter)
    print("Average LOADING iteration time: ", lightLoadPrfm.elapsed_time.mean(), "s")
    print("Average LOADING CPU utilization: ", lightLoadPrfm.CPU_utilization.mean())
    print("Average LOADING RAM utilization: ", lightLoadPrfm.RAM_utilization.mean(),"\n\n")

    #Export DF to csv
    lightLoadPrfm.to_csv (exportLocation+exportFilename, index = False, header=True)
