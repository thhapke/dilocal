
import pandas as pd
import copy
import io


def on_input(msg) :

    # Due to input-format PROPOSED transformation into DataFrame
    df = pd.read_csv(io.BytesIO(msg.body))

    # config parameter 
    #api.config.min_atomic_number = '1'    # datatype : number

    sm = df.sample(n=api.config.min_atomic_number, random_state = 1 )

    # Sending to outport output
    att = copy.deepcopy(msg.attributes)
    out_msg = api.Message(attributes=att,body=sm.values.tolist())
    api.send('output',out_msg)    # datatype: message

api.set_port_callback('input',on_input)   # datatype: message.file

