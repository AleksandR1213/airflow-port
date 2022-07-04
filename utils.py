import configparser

import os

def create_config(path):
    #create a Config file and excel heatmap
    config = configparser.ConfigParser()

    config.add_section("binance")
    config.set("binance", "pool_name_1", "mnrybn")
    config.set("binance", "pool_name_2", "pbblck")
    config.set("binance", "pool_name_3", "pbdfngesk")

    config.add_section("antpool")
    config.set("antpool", "pool_name_1", "pbtym")

    with open(path, "w") as config_file:
        config.write(config_file)


def get_config(path):
    #Returns the config object
    if not os.path.exists(path):
        create_config(path)
    
    config = configparser.ConfigParser()
    config.read(path)
    return config


def config_get_setting(path, section, setting):
    #Print out a setting
    config = get_config(path)
    value = config.get(section, setting)

    return value


def update_df_in_google_sheet(worksheet, df, cell):

    list_df = df.values.tolist()
    worksheet.update(cell, list_df)
