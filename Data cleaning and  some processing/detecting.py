import pandas as pd
import numpy as np
import os

filedir='H:/taxi data/'		#dir of the datasets
date='20130101'
NW=[-74.259090,40.917577]	#NW Point
SE=[-73.700272,40.477399]	#SE Point
threshold=0.1					#percentage
lon_0=NW[0]
lat_0=NW[1]
lon_1=SE[0]
lat_1=SE[1]
num_grids=401				#number of points divided
lons=np.linspace(lon_0,lon_1,num_grids)
lats=np.linspace(lat_0,lat_1,num_grids)


def openfile(path,name):

	df=pd.read_csv(path+name)
	return df

def countoutflow(data):
	outlier_points=0
	print('data.shape',data.shape)
	of=np.zeros((num_grids-1,num_grids-1))
	for item in data:
		index_lon = -1				
		index_lat = -1
		if(item[3]<lons[0] or item[3]>lons[num_grids-2] or item[4]>lats[0] or item[4]<lats[num_grids-2]):
			outlier_points=outlier_points+1
		else:
			for lon in lons:
				if(item[3]>lon):
					index_lon=index_lon+1
				else:
					break
			for lat in lats:
				if(item[4]<lat):
					index_lat=index_lat+1
				else:
					break
			of[index_lon][index_lat]=of[index_lon][index_lat]-1
	print('outlier_PU',outlier_points)
	return of		#negative values

def countinflow(data):
	outlier_points=0
	do=np.zeros((num_grids-1,num_grids-1))
	for item in data:
		index_lon = -1				
		index_lat = -1
		if(item[5]<lons[0] or item[5]>lons[num_grids-2] or item[6]>lats[0] or item[6]<lats[num_grids-2]):
			outlier_points=outlier_points+1
		else:
			for lon in lons:
				if(item[5]>lon):
					index_lon=index_lon+1
				else:
					break
			for lat in lats:
				if(item[6]<lat):
					index_lat=index_lat+1
				else:
					break
			do[index_lon][index_lat]=do[index_lon][index_lat]+1
	print('outlier_DO',outlier_points)
	return do

def volcanoes(filedir,date):
    time=date+'000000'
    grids=[]
    while(time[8:10]!='24'):
        print(time)
        temp=[]
        temp_pos=[]	#positive values
        temp_neg=[]	#negative values
        grids_AF=np.zeros((num_grids-1,num_grids-1))
        if(os.path.exists(filedir+'drop'+str(int(date[4:6]))+'/'+time+'drop.csv')):
            df=openfile(filedir+'drop'+str(int(date[4:6]))+'/',time+'drop.csv')
            data=df.values
            grids_AF=grids_AF+countoutflow(data)
        if(os.path.exists(filedir+'pickup'+str(int(date[4:6]))+'/'+time+'pickup.csv')):
            df=openfile(filedir+'pickup'+str(int(date[4:6]))+'/',time+'pickup.csv')
            data=df.values
            grids_AF=grids_AF+countinflow(data)
        ''''
        dt=pd.DataFrame(grids_AF)
        dt.to_csv(time+'.csv',index=False)'''
        # ###get threshold
        for rows in grids_AF:
            for i in rows:
                if i>0:
                    temp_pos.append(i)
                elif i<0:
                    temp_neg.append(i)
        if not len(temp_pos):
            temp_pos.append(0)
        if not len(temp_neg):
            temp_neg.append(0)
        temp_pos.sort()
        temp_neg.sort()

        t_pos=temp_pos[int((1-threshold)*len(temp_pos))-1]
        if int(threshold*len(temp_neg))-1<0:
            t_neg=temp_neg[0]
        else:
            t_neg=temp_neg[int(threshold*len(temp_neg))-1]
        ###store abnormal grids
        index_row=0
        for row in grids_AF:
            index_col=0
            index_row=index_row+1
            for col in row:
                index_col=index_col+1
                if (grids_AF[index_row-1][index_col-1]>t_pos):
                    temp.extend([1,lons[index_row-1],lats[index_col-1],lons[index_row],lats[index_col]])
                elif (grids_AF[index_row-1][index_col-1]<t_neg):
                    temp.extend([0,lons[index_row-1],lats[index_col-1],lons[index_row],lats[index_col]])
        grids.append(temp)
        time=str(int(time)+10000)
	
	
    f=open(date+'.json','w')	#saving json files
    flag1=0
    f.write('[')
    for i in grids:
        c='['
        flag2=0
        for j in i:
            if flag2!=(len(i)-1):
                c=c+str(j)+','
            else:
                c=c+str(j)
            flag2=flag2+1
        if flag1!=(len(grids)-1):
            c=c+'],'
        else:
            c=c+']'
        flag1=flag1+1
        f.write(c)
        print(flag1,flag2)
    f.write(']')
    f.close()
date='20130310'
while(date!='20140101'):
    print(date)
    volcanoes(filedir,date)
    date=str(int(date)+1)
    if(date[2:4]=='13'):
        if((date[4:6] in ['04','06','09','11']) and date[6:8]=='31'):
            date=str(int(date)+100-30)
        elif(date[4:6]=='02' and date[6:8]=='29'):
            date=str(int(date)+100-28)
        elif(date[4:6]=='12' and date[6:8]=='32'):
            date=str(int(date)-1100-31+10000)
        elif(date[6:8]=='32'):
            date=str(int(date)-31+100)



