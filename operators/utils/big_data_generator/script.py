# Mock apis needs to be commented before used within SAP Data Intelligence
from diadmin.dimockapi.mock_api import mock_api
api = mock_api(__file__)

import random
from datetime import datetime, timezone
import string

import pandas as pd
import numpy as np

counter = 0

def new_df():

    num_rows = api.config.num_rows
    alphabeth = string.ascii_lowercase
    len_str = 5
    df = pd.DataFrame(index=range(num_rows),columns=['id','timestamp','string_value','float_value'])
    df['id'] = df.index
    df['timestamp'] = datetime.now(timezone.utc)
    df['string_value'] = df['string_value'].apply(lambda x: np.random.choice(alphabeth, size=len_str))
    df['float_value'] =  np.random.uniform(low=0., high=1000, size=(num_rows,))

    return df

def gen():

    global counter
    api.outputs.log.publish(f"New DataFrame created: {str(counter)} - Next in {api.config.periodicy}s")
    #df = new_df()
    counter += 1
    #return float(api.config.periodicy)
    return 0.5



api.add_timer(gen)