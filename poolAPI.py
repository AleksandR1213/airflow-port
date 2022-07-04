import pandas as pd
import requests 

def get_workers(pool_name, dataframe=False, splitworkers=False):
    
    req = f'https://mem.minery.io/iapi/v1/audit/pools/{pool_name}/devices'

    response = requests.get(req)

    if response.status_code != 200:
        return None

    if dataframe:
        df = pd.DataFrame.from_dict(response.json()['data']['items'])
        df.sort_values(by='netboxDeviceId', inplace=True)
        df.reset_index(inplace=True, drop=True)
        df['netboxDeviceId'] = pd.to_numeric(df['netboxDeviceId'], errors='coerce').fillna(0).astype(int)
        
        if splitworkers:
            df_split_workers = df['workerName'].str.split('.', expand=True)
            df.drop('workerName', axis=1, inplace=True)
            df_split_workers.columns=['pool_name', 'workerName']
            # df_split_workers.drop('lol', axis=1, inplace=True)
            df = pd.concat([df, df_split_workers], axis=1)
            df = df.reindex(columns=['pool_name',
                                    'workerName', 
                                    'netboxDeviceId', 
                                    'foundInNetbox', 
                                    'foundInStock'])
        return df

    return response.json()['data']['items']