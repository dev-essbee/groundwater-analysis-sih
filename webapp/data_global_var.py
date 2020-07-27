import pandas as pd
import json

data = r"../data/"
#######################################################################################################################
################################################### load data #########################################################
#######################################################################################################################
# todo: optimize loading data
# def load_data():
#     bucket_name
#     folder_name

#     df_gw_pre_post = pd.read_parquet('gs://gnd-water-manage-sih.appspot.com/gw-block-pre-post.parquet.gzip')
#     # print(df_gw_pre_post.head())
#     fs=gcsfs.GCSFileSystem(project='gnd-water-manage-sih')
#     bucket='gnd-water-manage-sih.appspot.com/'
#     with fs.open(bucket + r'gadm36_IND_0_id.json') as f:
#         india_geojson = json.load(f)
#     with fs.open(bucket + r'gadm36_IND_1_id.json') as f:
#         states_geojson = json.load(f)
#     with fs.open(bucket + r'gadm36_IND_2_id.json') as f:
#         districts_geojson = json.load(f)
#     with fs.open(bucket + r'gadm36_IND_3_id.json') as f:
#         blocks_geojson = json.load(f)
df_gw_pre_post = pd.read_parquet(data + r'comp/gw-block-pre-post.parquet.gzip')
with open(data + r'geojson/gadm36_IND_0_id.json', 'r') as f:
    india_geojson = json.load(f)
with open(data + r'geojson/gadm36_IND_1_id.json', 'r') as f:
    states_geojson = json.load(f)
with open(data + r'geojson/gadm36_IND_2_id.json', 'r') as f:
    districts_geojson = json.load(f)
with open(data + r'geojson/gadm36_IND_3_id.json', 'r') as f:
    blocks_geojson = json.load(f)
# important constants
NO_OF_YEARS = (len(list(df_gw_pre_post.columns)) - 4) // 3
YEARS = [str(i + 1994) for i in range(NO_OF_YEARS)]
YEARS_PRE = list(map(lambda year: year + "-pre", YEARS))
YEARS_POST = list(map(lambda year: year + "-post", YEARS))
YEARS_STATIONS = list(map(lambda year: year + "-stations", YEARS))
YEARS_STATIONS.append("total-stations")
