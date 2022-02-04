
import pandas as pd
import copy
import io


def on_input(msg) :

    # Due to input-format PROPOSED transformation into DataFrame
    df = pd.read_csv(io.BytesIO(msg.body))

    # config parameter 
    #api.config.type = '*'    # datatype : string


    ### Custom Code
    df = df[['title', 'type', 'cast', 'release_year']]
    df = df.loc[df['cast'].notna()]
    df['cast'] = df['cast'].apply(lambda x: x.split(','))
    df = df.explode('cast')
    df = df.rename(columns={'cast': 'ACTOR'})
    df['ACTOR'] = df['ACTOR'].str.strip()

    if not api.config.type == '*' and not api.config.type == None:
        df = df.loc[df['type'] == api.config.type]


    # Sending to outport output
    # Due to output-format PROPOSED transformation into message.table
    #df.columns = map(str.upper, df.columns)  # for saving to DB upper case is usual
    columns = []
    for col in df.columns : 
        columns.append({"class": str(df[col].dtype),'name': col})
    att = copy.deepcopy(msg.attributes)
    att['table'] = {'columns':columns,'name':'TABLE','version':1}
    out_msg = api.Message(attributes=att, body= df.values.tolist())
    api.send('output',out_msg)    # datatype: message.table

api.set_port_callback('input',on_input)   # datatype: message.file

