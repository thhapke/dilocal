
import pandas as pd
import io


def on_input(msg) :

    # Due to input-format PROPOSED transformation into DataFrame
    df = pd.read_csv(io.BytesIO(msg.body))

    # config parameter 
    #api.config.num_files = 'null'    # datatype : number
    #api.config.prefix = None   # datatype : string



    # Due to output-format PROPOSED transformation into message.table
    #df.columns = map(str.upper, df.columns)  # for saving to DB upper case is usual
    columns = []
    for col in df.columns : 
        columns.append({"class": str(df[col].dtype),'name': col})
    att = {'table':{'columns':columns,'name':'TABLE','version':1}}
    out_msg = api.Message(attributes=att, body= df.values.tolist())
    api.send('output',out_msg)    # datatype: message.table

api.set_port_callback('input',on_input)   # datatype: message.file

