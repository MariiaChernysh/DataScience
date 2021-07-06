import pandas as pd
import numpy as np
from datetime import datetime
import matrixprofile as mp
######################################################
Broker = "Broker1"
#To build datarange and convert to dataframe
date_rng = pd.date_range(start='2021-05-13', end='2021-06-02', freq='T')
dr = pd.DataFrame(date_rng)
dr.columns = ["DateTime"]
#open errors data
df = pd.read_csv("TSErrors_data.csv", sep = ";", index_col=False)
df['DateTime'] = pd.to_datetime(df['created_at'] + ' ' + df['Time'])

# round to minutes
df['DateTime'] =round(df['DateTime'], 'min')
df['DateTime'] = pd.to_datetime(df['DateTime'])
#delete leads data
dfe= df[df['E/L']=='E']
#delete col
del(dfe['created_at'])
del(dfe['Time'])
del(dfe['E/L'])
del(dfe['Broker id'])
#substract 1 broker
EuropeFX = dfe[dfe['Broker name']==Broker]
#join daterange with errors
date_rng = dr.merge(EuropeFX, on="DateTime", how="left")
date_rng.columns = ['DateTime', 'Errors']
#Replace text with 1 = error
date_rng = date_rng.replace(to_replace = Broker, value = "1")
#replace nans with 0
date_rng['Errors'] = date_rng['Errors'].fillna(0)
date_rng['Errors'] = pd.to_numeric(date_rng['Errors'])
#to make matrixprofile convert to numpy
df_1 = date_rng.T
df_1=df_1.rename(columns=df_1.iloc[0])
df_1=df_1.iloc[[1]]
arr = df_1.to_numpy()

float_arr=[]
for i in arr:
    for x in i:
        float_arr.append(float(format(x, '.4f')))

float_arr=np.array(float_arr)

limit_arr =float_arr[0:5000]
extra = float_arr[15000:20000]
limit_arr2 = np.append(limit_arr, extra)
#analyze matrixprofile
profile, figures = mp.analyze(limit_arr2, sample_pct=1.0, threshold=0.98, n_jobs=1, preprocessing_kwargs=None)

mp.visualize(profile)

#Hourly motifs
hour_window = 60
hour_profile = mp.utils.pick_mp(profile, hour_window)
mp.visualize(hour_profile)
#3Hour motifs
hour3_window = 180
hour3_profile = mp.utils.pick_mp(profile, hour3_window)
mp.visualize(hour3_profile)
#Analyze daily motifs
daily_window = 1440
daily_profile = mp.utils.pick_mp(profile, daily_window)
mp.visualize(daily_profile)
#Custom
window = 854
test_profile = mp.utils.pick_mp(profile, window)
mp.visualize(test_profile)
#discover motifs
window = 854
custom_profile = mp.compute(float_arr, windows=window)
cc_profile = mp.discover.motifs(custom_profile, k=1) # 1 - top motif
figures = mp.visualize(cc_profile)

#Discover snippets
sn = mp.discover.snippets(limit_arr, snippet_size=4)
figures = mp.visualize(sn)
