
import os
import pandas as pd
import numpy as np

def openfile(path,name):
    '''

    :param path:
    :param name:
    :return:
    '''
    df = pd.read_csv(path + name)
    return df
def del_rows(data_tl):
    '''
    :param data_tl:
    :return:
    '''
    list_data = []
    data_array = data_tl.values
    data = data_array.tolist()
    for one in data:
        flag = True
        for i in one:
            print(i)
            print(type(i))
            if i == None :
                flag = False
                print(one)
                break
        for j in one:
            count = 0
            if j == 0 :
                if one.index(j) != 2:
                    print('***')
                    flag = False
                    break
                else:
                    print(one)
                    print('**')
                    for item in enumerate(one):
                        print('1')
                        if item[1] == 0:
                            count += 1
                            print(count)
                    if count > 1:
                        flag = False
                        break
        if flag == True:
            list_data.append(one)
        else:
            continue
    return list_data
file_dir = "H:/taxi data/NYCFareDataCsv2/"  # 数据文件夹路径
for root, dirs, files in os.walk(file_dir):
    for i in range(3):
        name = files[i]
        new_name = name[0:-4]
        path = 'H:/taxi data/NYCFareDataCsv2/'
        f = openfile(path,name)
        data_tl = f.drop(['medallion',' hack_license',' vendor_id',' rate_code',' store_and_fwd_flag',' trip_time_in_secs',' trip_distance'],axis=1)  # data_tl includes time,location,passenger
        data_pure = del_rows(data_tl)
        data = pd.DataFrame(np.array(data_pure), columns=['pickup_datetime','dropoff_datetime','passenger_count','pickup_longitude','pickup_latitude','dropoff_longitude','dropoff_latitude'])
        data.to_csv('H:/taxi data/NYCFareDatapure/' + new_name + '.csv', index=False)


