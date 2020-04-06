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

    extractionTimerStart = time.perf_counter()
    ### Run 30 iterations to collect a df of performance metrics
    ### light extraction performance metrics
    column_names = ["base_CPU","base_RAM","CPU_utilization", "RAM_utilization", "CPU_d","RAM_d","elapsed_time"]
    lightExtractionPrfm = pd.DataFrame(columns = column_names)

    ### base metrics
    print("STARTING EXTRACTION...")
    print("RUNNING...")

    ### Run n iterations to collect a df of performance metrics
    for sampleNo in range(iterations):

        time.sleep(5)
	#Collect base settings
        baseCPU = psutil.cpu_percent()
        baseRAM = psutil.virtual_memory().percent

        #Initiate timer for query
        start = time.perf_counter()
    
        #insert data into dataFrame
        Extraction = pd.DataFrame(list(item.find()))
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
    performance(lightExtractionPrfm,iterations,extractionTimerStart,extractionTimerEnd)
    
    #Export DF to csv
    lightExtractionPrfm.to_csv (exportLocation+exportFilename, index = False, header=True)
    return Extraction


def loading(client, table, transformationDf, iterations,exportLocation,exportFilename):
    #Connect to datalake
    from pymongo import MongoClient
    db = client['datalake']

    # Write dataframe to datalake
    #Create df to collect performance metrics
    column_names = ["base_CPU","base_RAM","CPU_utilization", "RAM_utilization", "CPU_d","RAM_d","elapsed_time"]
    lightLoadPrfm = pd.DataFrame(columns = column_names)
    print('STARTING LOAD...')
    print('RUNNING...')

    #Run 30 iterations to collect loading performance metrics
    loadTimerStart = time.perf_counter()

    transformationDf.reset_index(inplace=True)
    data_dict = transformationDf.to_dict("records")# Insert collection
    for sampleNoTransform in range(iterations):

        time.sleep(5)
	#Collect base settings
        baseCPU = psutil.cpu_percent()
        baseRAM = psutil.virtual_memory().percent

        # Start Timer and progress tracker
        start = time.perf_counter()
        collection = db[table]

        #Working Code
        collection.insert_many(data_dict)
        sampleCPU = psutil.cpu_percent()
        sampleRAM = psutil.virtual_memory().percent

        #Stop timer  
        stop = time.perf_counter()
        db.drop_collection(collection)

        lightLoadPrfm = lightLoadPrfm.append(pd.DataFrame({'base_CPU': baseCPU,
                                                         'base_RAM': baseRAM,
                                                         'CPU_utilization': sampleCPU,
                                                         'RAM_utilization':  sampleRAM,
                                                         'CPU_d': sampleCPU-baseCPU,
                                                         'RAM_d': sampleRAM - baseRAM,
                                                         'elapsed_time':stop - start},
                                                          index=[1]), ignore_index=True) 
    loadTimerEnd = time.perf_counter() 
    collection = db[table]
    collection.insert_many(data_dict)

    #load data into datalake for use.

    print("Loading metrics captured loading complete.\n")
    performance(lightLoadPrfm,iterations,loadTimerStart,loadTimerEnd)

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
