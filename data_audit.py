from datetime import datetime

from poolAPI import get_workers
import utils
import gspread

CREDS_FILE = 'data_auditor_netbox_vs_pool.json'
YANDEX_TOKEN = 'AQAAAAA6Is1QAAfoLy9DtZNzEkbZkFoXgCqDQK8'
CONFIG_PATH = 'pools_name.ini'


def pool_data_audit_binance(pool_name):
    
    df_workers = get_workers(pool_name=pool_name,
                                dataframe=True,
                                splitworkers=True
    )

    df_workers_not_nb = df_workers[df_workers['foundInNetbox'] == False]
    df_workers_not_nb = df_workers_not_nb[df_workers_not_nb['foundInStock'] == True]
    df_workers_not_nb.drop(['foundInNetbox', 'foundInStock', 'netboxDeviceId'], axis=1, inplace=True)

    df_workers_not_pool = df_workers[df_workers['foundInNetbox'] == True]
    df_workers_not_pool = df_workers_not_pool[df_workers_not_pool['foundInStock'] == False]
    df_workers_not_pool.drop(['foundInNetbox', 'foundInStock'], axis=1, inplace=True)

    gc = gspread.service_account(filename=CREDS_FILE)
    SpreadSheet = gc.open("Сверка пулов между асиком и нетбоксом")

    try:
        WorkSheet = SpreadSheet.worksheet('da_worker_netbox_vs_pool')
    except:
        WorkSheet = SpreadSheet.add_worksheet('da_worker_netbox_vs_pool', rows='10', cols='20')

    WorkSheet.clear()

    head = WorkSheet.range('A2:B2')
    head[0].value = 'pool_name'
    head[1].value = 'worker Name'
    
    head1 = WorkSheet.range('E2:G2')
    head1[0].value = 'pool_name'
    head1[1].value = 'worker Name'
    head1[2].value = 'netbox id'

    utils.update_df_in_google_sheet(df=df_workers_not_nb,
                                    worksheet=WorkSheet,
                                    cell='A3'
    )

    utils.update_df_in_google_sheet(df=df_workers_not_pool,
                                    worksheet=WorkSheet,
                                    cell='E3'
    )

    WorkSheet.update('A1', 'not in the netbox')
    WorkSheet.update('E1', 'not in the pool')
    WorkSheet.update_cells(head)
    WorkSheet.update_cells(head1)
    
    current_time = datetime.now()
    time_cell = "{}:{} {}.{}.{}".format(current_time.hour, 
                                    current_time.minute, 
                                    current_time.day, 
                                    current_time.month, 
                                    current_time.year)

    WorkSheet.update('I2', time_cell)
    

def main():

    config = utils.get_config(CONFIG_PATH)

    for sourse_name in config.sections():
        for pool_name in config.items(sourse_name):
            if pool_name[1] == 'mnrybn':
                pool_data_audit_binance(pool_name[1])
            
    
if __name__ == "__main__":
    #gspread 
    main()
