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
    column_names = ["base_CPU","base_RAM","CPU_utilization", "RAM_utilization", "CPU_d","RAM_d","elapsed_time"]
    lightExtractionPrfm = pd.DataFrame(columns = column_names)

    ### base metrics
    print("\nSTARTING EXTRACTION...")
    print("RUNNING...")

    extractionTimerStart = time.perf_counter()
    ### Run 30 iterations to collect a df of performance metrics
    iterations = loopIterations
    for sampleNo in range(iterations):
        #script to pull data
        LEsql = sqlscript

        time.sleep(5)
	#Collect base settings
        baseCPU = psutil.cpu_percent()
        baseRAM = psutil.virtual_memory().percent

        #Initiate timer for query
        start = time.perf_counter()

        #insert data into dataFrame
        orderItemJoin = pd.read_sql(sql=LEsql, con=connection)
        sampleCPU = psutil.cpu_percent()
        sampleRAM = psutil.virtual_memory().percent

        #Stop timer  
        stop = time.perf_counter()

        #load df with performance metrics    
        lightExtractionPrfm = lightExtractionPrfm.append(pd.DataFrame({'base_CPU': baseCPU,
                                                         'base_RAM': baseRAM,
                                                         'CPU_utilization': sampleCPU,
                                                         'RAM_utilization':  sampleRAM,
                                                         'CPU_d': sampleCPU-baseCPU,
                                                         'RAM_d': sampleRAM - baseRAM,
                                                         'elapsed_time':stop - start},
                                                          index=[1]), ignore_index=True)
    extractionTimerEnd= time.perf_counter()   

    print("Data frame loading complete.\n")
   
    performance(lightExtractionPrfm,loopIterations,extractionTimerStart,extractionTimerEnd)

    #Export DF to csv
    lightExtractionPrfm.to_csv (exportLocation + exportFilename, index = False, header=True)
    return orderItemJoin


def loading(transformationDf,tablename, loopIterations,exportLocation,exportFilename):
    #Connect to datalake
    from sqlalchemy import create_engine
    dl = create_engine('mysql+mysqlconnector://root:0861137MySQL!@127.0.0.1/datalake', echo=False)

    # Write dataframe to datalake
    #Create df to collect performance metrics
    column_names = ["base_CPU","base_RAM","CPU_utilization", "RAM_utilization", "CPU_d","RAM_d","elapsed_time"]
    lightLoadPrfm = pd.DataFrame(columns = column_names)
    print('STARTING LOAD...')
    print('Load database connection is: ',dl)
    print('RUNNING...')

    #Run 30 iterations to collect loading performance metrics
    loadIter = loopIterations
    loadTimerStart = time.perf_counter()
    for sampleNoTransform in range(loadIter):
        time.sleep(5)
	#Collect base settings
        baseCPU = psutil.cpu_percent()
        baseRAM = psutil.virtual_memory().percent

        # Start Timer and progress tracker
        start = time.perf_counter()
	
        #Working Code
        transformationDf.to_sql(tablename, con=dl, if_exists='replace',index=False)
        sampleCPU = psutil.cpu_percent()
        sampleRAM = psutil.virtual_memory().percent

        #Stop timer  
        stop = time.perf_counter()

        lightLoadPrfm = lightLoadPrfm.append(pd.DataFrame({'base_CPU': baseCPU,
                                                         'base_RAM': baseRAM,
                                                         'CPU_utilization': sampleCPU,
                                                         'RAM_utilization':  sampleRAM,
                                                         'CPU_d': sampleCPU-baseCPU,
                                                         'RAM_d': sampleRAM - baseRAM,
                                                         'elapsed_time':stop - start},
                                                          index=[1]), ignore_index=True) 
    loadTimerEnd = time.perf_counter() 
   

    #load data into datalake for use.

    print("Loading metrics captured loading complete.\n")
    performance(lightLoadPrfm,loopIterations,loadTimerStart,loadTimerEnd)

    #Export DF to csv
    lightLoadPrfm.to_csv (exportLocation+exportFilename, index = False, header=True)

def performance(loadPrfm, iteration, start, stop):
    print("Iterations performed: ", iteration)
    print("TOTAL Process time: ", (stop - start), "s")
    print("Average iteration time: ", loadPrfm.elapsed_time.mean(), "s")
    print("Average BASE CPU: ", loadPrfm.base_CPU.mean())
    print("Average BASE RAM: ", loadPrfm.base_RAM.mean())
    print("Average CPU Performance ", loadPrfm.CPU_d.mean())
    print("Average RAM Performance ", loadPrfm.RAM_d.mean())
    print("Average CPU utilization: ", loadPrfm.CPU_utilization.mean())
    print("Average RAM utilization: ", loadPrfm.RAM_utilization.mean(),"\n\n")

