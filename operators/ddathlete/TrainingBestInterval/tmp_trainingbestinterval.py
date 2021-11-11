
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')



def log(log_str) :
    api.logger.info(log_str)
    api.send('log',log_str)

table_dict = {"columns": [
        {"name": "TRAINING_ID", "nullable": False,"type": {"hana": "BIGINT"}},
        {"name": "DATE", "nullable": True,"type": {"hana": "DAYDATE"}},
        {"name": "SPORT_TYPE", "nullable": False,"size": 25, "type": {"hana": "NVARCHAR"}},
        {"name": "INTERVAL_WIDTH", "nullable": True,"type": {"hana": "INTEGER"}},
        {"name": "TIMESTAMP_START","nullable": True, "type": {"hana": "LONGDATE"}},
        {"name": "TIMESTAMP_END", "nullable": True,"type": {"hana": "LONGDATE"}},
        {"name": "POWER_MIN", "nullable": True,"type": {"hana": "DOUBLE"}},
        {"name": "POWER_MAX", "nullable": True,"type": {"hana": "DOUBLE"}},
        {"name": "POWER_MEAN", "nullable": True,"type": {"hana": "DOUBLE"}},
        {"name": "HEARTRATE_MIN","nullable": True, "type": {"hana": "INTEGER"}},
        {"name": "HEARTRATE_MAX","nullable": True, "type": {"hana": "INTEGER"}},
        {"name": "HEARTRATE_MEAN","nullable": True, "type": {"hana": "INTEGER"}},
        {"name": "CADENCE_MIN", "nullable": True,"type": {"hana": "DOUBLE"}},
        {"name": "CADENCE_MAX", "nullable": True,"type": {"hana": "DOUBLE"}},
        {"name": "CADENCE_MEAN","nullable": True, "type": {"hana": "DOUBLE"}}], "name": "BEST_INTERVAL", "version": 1}

def on_input(msg):
    
    att = dict(msg.attributes)
    interval_width = api.config.interval_width * 60
    
    header = [c["name"] for c in msg.attributes['table']['columns']]
    df = pd.DataFrame(msg.body, columns=header)
    #log('Process {} of {} - records:{}'.format(att['table_name'],att['year'],df.shape[0] ))
    if df.shape[0] == 0 : 
        log('Warning: NO RECORDS')
        api.send("nodata", api.Message(attributes = att,body = 'NODATA'))
        return 0 
    
    # Time Series Index
    df['TIMESTAMP'] = pd.to_datetime(df.TIMESTAMP)
    df['INDEX'] = df['TIMESTAMP']
    df = df.set_index('INDEX').sort_index()

    #df.tz_localize('utc')
    df = df.tz_convert(None)
    
    # Rolling average over Power and find max power
    #df['POWER_RM'] = df.groupby(['TRAINING_ID'])['POWER'].rolling(interval_width).mean().droplevel(0)
    #api.config.min_periods = 100
    df['POWER_RM'] = df.groupby(['TRAINING_ID'])['POWER'].rolling(interval_width, min_periods=api.config.min_periods).mean().droplevel(0)
    print('Number skipped windows: {}'.format(df['POWER_RM'].isna().sum()))

    df['POWER_MAX'] = df.groupby(['TRAINING_ID'])['POWER_RM'].transform(max)
    
    # Timeindex of max power and get time intervals
    max_best = df[(df['POWER_RM'] == df['POWER_MAX']) & (df['POWER_MAX']>0)].index.values
    best_i = np.vstack((max_best - np.timedelta64(interval_width, 's'), max_best)).T
    
    num_trainings = len(df['TRAINING_ID'].unique())
    
    log('# best intervals: {}  Number of trainings: {}'.format(len(best_i),num_trainings))
    
    best_list = list()
    milestone_counter = len(best_i) // 30
    for counter, bi in enumerate(best_i):
        dfi = df[(df.index > bi[0]) & (df.index <= bi[1])]
        best_list.append(dfi)
        if milestone_counter > 0 and counter % milestone_counter == 0 :
            log('Processed: {}/{}'.format(counter,len(best_i)))
        
    tdf = pd.concat(best_list)
    
    log('#Records with best intervals only: {}'.format(tdf.shape[0]))
    
    aggreg = {'DATE': 'first', 'TIMESTAMP': ['min', 'max'],  \
             'POWER': ['min', 'max', 'mean'], 'HEART_RATE': ['min', 'max', 'mean'], 'CADENCE': ['min', 'max', 'mean']}

    tdf = tdf.groupby('TRAINING_ID').agg(aggreg).reset_index()
    tdf.columns = ['_'.join(col).upper() for col in tdf.columns]

    tdf['SPORT_TYPE'] = att['table_name']
    tdf.rename(columns={"TRAINING_ID_": "TRAINING_ID", "DATE_FIRST": "DATE"}, inplace=True)

    tdf = tdf.loc[tdf['HEART_RATE_MAX'] > 0 ]

    ## BEGIN ANALYSIS
    #fig,axs = plt.subplots(3,sharex=True)
    #axs[0].plot(tdf['DATE'],tdf['POWER_MAX'])
    #axs[0].set_title('POWER_MAX')
    #axs[1].plot(tdf['DATE'],tdf['CADENCE_MAX'])
    #axs[1].set_title('CADENCE_MAX')
    #axs[2].plot(tdf['DATE'],tdf['HEART_RATE_MAX'])
    #axs[2].set_title('HEART_RATE_MAX')
    #plt.savefig('powerinterval.png')
    #plt.show()
    ## END ANALYSIS
    
    tdf['TIMESTAMP_START'] = tdf['TIMESTAMP_MIN'].dt.strftime('%Y-%m-%d %H:%M:%S')
    tdf['TIMESTAMP_END'] = tdf['TIMESTAMP_MAX'].dt.strftime('%Y-%m-%d %H:%M:%S')
    tdf['INTERVAL_WIDTH'] = interval_width
    
    # cast
    tdf['HEART_RATE_MIN'] = tdf['HEART_RATE_MIN'].astype('int')
    tdf['HEART_RATE_MAX'] = tdf['HEART_RATE_MAX'].astype('int')
    tdf['HEART_RATE_MEAN'] = tdf['HEART_RATE_MEAN'].astype('int')
    tdf['CADENCE_MIN'] = tdf['CADENCE_MIN'].astype('float')
    tdf['CADENCE_MAX'] = tdf['CADENCE_MAX'].astype('float')
    tdf['CADENCE_MEAN'] = tdf['CADENCE_MEAN'].astype('float')
    tdf['POWER_MIN'] = tdf['POWER_MIN'].astype('float')
    tdf['POWER_MAX'] = tdf['POWER_MAX'].astype('float')
    tdf['POWER_MEAN'] = tdf['POWER_MEAN'].astype('float')
    tdf['INTERVAL_WIDTH'] = tdf['INTERVAL_WIDTH'].astype('int')
    
    
    # sort dataframe according to target table
    tdf = tdf[['TRAINING_ID', 'DATE', 'SPORT_TYPE', 'INTERVAL_WIDTH','TIMESTAMP_START', 'TIMESTAMP_END', \
               'POWER_MIN', 'POWER_MAX', 'POWER_MEAN', 'HEART_RATE_MIN', 'HEART_RATE_MAX', \
               'HEART_RATE_MEAN', 'CADENCE_MIN', 'CADENCE_MAX', 'CADENCE_MEAN']]

    att["table"] = dict(table_dict)
    for i, col in enumerate(tdf.columns) :
        att['table']['columns'][i]['class'] = str(tdf[col].dtype)
        att['table']['columns'][i]['tdf_name'] = col

    data = tdf.values.tolist()
    api.send("output", api.Message(attributes = att,body = data))
    

api.set_port_callback("input", on_input)
