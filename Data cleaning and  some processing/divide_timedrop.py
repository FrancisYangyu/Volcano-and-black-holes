import pandas as pd
import numpy as np
import os
def openfile(path,name):
    df = pd.read_csv(path + name)
    return df
file_dir = "H:/taxi data/data/"  # 数据文件夹路径
for root, dirs, files in os.walk(file_dir):
    for i in range(1):
        name = files[i]
        path = 'H:/taxi data/data/'
        f = openfile(path,name)
        f["p_time"] = f.dropoff_datetime.apply(lambda t: int(t[:4] + t[5:7] + t[8:10] + t[11:13] + t[14:16] + t[17:19]))
        data = f.values
        data = data[data[: ,1].argsort()]
        start = 20131201000000
        end = 20131201010000
        list_time = []
        for one in data:
            if one[7] >= start and one[7] <end :
                list_time.append(one)

            else:

                store_data = pd.DataFrame(np.array(list_time),columns=['pickup_datetime','dropoff_datetime','passenger_count','pickup_longitude','pickup_latitude','dropoff_longitude','dropoff_latitude','p_time'])
                store_data.to_csv('H:/taxi data/drop12/' + str(start) + 'drop' + '.csv',index=False)
                list_time = []
                while one[7] >= end:
                    if str(start)[8:10] == '23':
                        start = start + 770000
                        end = end + 770000
                    else:
                        start = start + 10000
                        end = end + 10000
                list_time.append(one)

        final_data = pd.DataFrame(np.array(list_time),columns=['pickup_datetime', 'dropoff_datetime', 'passenger_count', 'pickup_longitude',
                                           'pickup_latitude', 'dropoff_longitude', 'dropoff_latitude', 'p_time'])
        final_data.to_csv('H:/taxi data/drop12/' + str(start) + 'drop' + '.csv', index=False)



