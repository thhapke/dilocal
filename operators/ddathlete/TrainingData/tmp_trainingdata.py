

def log(log_str) :
    api.logger.info(log_str)
    api.send('log',log_str)


def gen():
    
    tables = api.config.tables
    schema = api.config.schema
    
    #just a change
    # loop over tables and years
    
    num_msg = len(tables) * (api.config.to_year -api.config.from_year+1)
    count = 0 
    for i,t in enumerate(tables) : 

        schematable = schema + '.' + t
        lastMessage = False
            
        #top = 'TOP 100000' 
        top = ''
        for year in range(api.config.from_year, api.config.to_year+1) :
            count +=1
            if t == 'CYCLING_OUTDOOR' :
                sql = 'SELECT {} TRAINING_ID, "date" as DATE,"timestamp" as TIMESTAMP, '\
                      '"distance" as DISTANCE, "heart_rate" as HEART_RATE, "cadence" as CADENCE, ' \
                      '"power" as POWER, "temperature" as TEMPERATURE '\
                      'FROM {} WHERE YEAR("timestamp") = {};'.format(top,schematable,year)
            elif t == 'CYCLING_INDOOR' :
                sql = 'SELECT {} TRAINING_ID, "date" as DATE,"timestamp" as TIMESTAMP, '\
                      '"heart_rate" as HEART_RATE, "cadence" as CADENCE, ' \
                      '"power" as POWER, "temperature" as TEMPERATURE '\
                      'FROM {} WHERE YEAR("timestamp") = {};'.format(top,schematable,year)
            elif t == 'RUNNING' :
                sql = 'SELECT {} TRAINING_ID, "date" as DATE,"timestamp" as TIMESTAMP, '\
                      '"distance" as DISTANCE, "heart_rate" as HEART_RATE, "cadence" as CADENCE, ' \
                      '"speed" as POWER, "temperature" as TEMPERATURE '\
                      'FROM {} WHERE YEAR("timestamp") = {};'.format(top,schematable,year)
            elif t in ['SWIMMING_POOL', 'SWIMMING_OPEN_WATER'] :
                sql = 'SELECT {} TRAINING_ID, "date" as DATE,"timestamp" as TIMESTAMP, '\
                      '"distance" as DISTANCE, "heart_rate" as HEART_RATE, "cadence" as CADENCE, ' \
                      '"speed" as POWER '\
                      'FROM {} WHERE YEAR("timestamp") = {};'.format(top,schematable,year)
            else :
                log('Sport type not supported: {}'.format(t))
                continue
            
            lastMessage = False 
            if i == len(tables) - 1 and year == api.config.to_year :
                log('Last message!')
                lastMessage == True 
                                
            att = {'schema':schema,'table_name' : t,'lastMessage':lastMessage, \
                   'index':count,'max_index':num_msg,'year':year,'table':{'name':schematable,'version':1}}
                   
            api.send("sql", api.Message(attributes = att  , body = sql))
            
            log('SQL {}/{} - {} : {}'.format(count,num_msg,att['table_name'],sql))


api.add_generator(gen)

