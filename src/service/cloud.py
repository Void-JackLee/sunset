import numpy as np
import requests
from PIL import Image
import os
from io import BytesIO
from datetime import datetime, timedelta
from .map import get_grayland

def generate_mosaic():
    line0 = []
    line1 = []
    mask = []
    black = np.array([1]*16*16).reshape(16,16)
    white = np.array([254]*16*16).reshape(16,16)
    for i in range(16):
        if i & 1 == 0: line0.append(black)
        else: line0.append(white)
    line0 = np.hstack(line0)
    for i in range(16):
        if i & 1 == 1: line1.append(black)
        else: line1.append(white)
    line1 = np.hstack(line1)
    for i in range(16):
        if i & 1 == 0: mask.append(line1)
        else: mask.append(line0)
    return np.vstack(mask)

def process_satellite(data, mask, all = False):
    visible = abs(data[:256,:] - mask)
    infra = abs(data[256:,:] - (255 - mask))
    if all: return np.dstack((visible,infra))
    if np.max(visible) == 0: return infra
    return visible

SATE_BLOCK_PIXEL_SIZE = 256

def get_single_satellite(date,lo,la,scale = 7,log = True, all = False):
    if log: print(f'[REQUEST] https://sat.windy.com/satellite/tile/deg140e/{date}/{scale}/{lo}/{la}/visir.jpg?mosaic=true')
    r = requests.request('GET',f'https://sat.windy.com/satellite/tile/deg140e/{date}/{scale}/{lo}/{la}/visir.jpg?mosaic=true')
    data = np.array(Image.open(BytesIO(r.content)),dtype=int)
    return final_satellite(data,generate_mosaic(),lo,la,scale,all,log)
    # return process_satellite(data,generate_mosaic(),all)

def get_time_list(log = False,where='deg140e'):
    # 时区转换
    now = (datetime.now()+ timedelta(hours=-8)).strftime('%H%M')
    # 得到当前时间列表
    if log: print(f'[REQUEST] https://sat.windy.com/satellite/info.json?{now}')
    r = requests.request('GET',f'https://sat.windy.com/satellite/info.json?{now}')

    if r.status_code == 200:
        res = r.json()
        for i in res['satellites']:
            if i['name'] != where:
                continue
            data = []
            for j in i['dstTime']:
                # 格式转换
                data.append(j[:4] + j[5:7] + j[8:10] + j[11:13] + j[14:16])
            return data
    else:
        return None

def get_cur_satellite(rangeLongitude,rangeLatitude,scale = 7,log = False,all=False,date=None,where='deg140e'):
    if date == None:
        dateList = get_time_list(where=where)
        if dateList == None:
            return
        date = dateList[-1]
    else:
        date = (datetime.strptime(str(date),'%Y%m%d%H%M') + timedelta(hours=-8)).strftime('%Y%m%d%H%M')
    sample = np.zeros((SATE_BLOCK_PIXEL_SIZE,SATE_BLOCK_PIXEL_SIZE))
    mask = generate_mosaic()
    m = []

    if not(os.path.exists('satellite')): os.makedirs('satellite')

    for y in range(rangeLatitude[0],rangeLatitude[1]):
        line = []
        for x in range(rangeLongitude[0],rangeLongitude[1]):
            if not(os.path.exists(f'satellite/{date}_{scale}_{x}_{y}.png')):
                if log: print(f'[REQUEST] https://sat.windy.com/satellite/tile/{where}/{date}/{scale}/{x}/{y}/visir.jpg?mosaic=true')
                r = requests.request('GET',f'https://sat.windy.com/satellite/tile/{where}/{date}/{scale}/{x}/{y}/visir.jpg?mosaic=true')
                if r.status_code == 200:
                    data = Image.open(BytesIO(r.content))
                    data.save(f'satellite/{date}_{scale}_{x}_{y}.png')
                    data = np.array(data,dtype=int)

                    line.append(final_satellite(data, mask, x, y, scale, all, log))
                    # line.append(process_satellite(data, mask, all))
                else: line.append(sample)
            else:
                if log: print(f'[READ] satellite/{date}_{scale}_{x}_{y}.png')
                data = np.array(Image.open(f'satellite/{date}_{scale}_{x}_{y}.png'),dtype=int)
                line.append(final_satellite(data, mask, x, y, scale, all, log))
                # line.append(process_satellite(data, mask, all))
        line = np.hstack(line)
        m.append(line)
    m = np.vstack(m)
    return m



## 进一步处理云图

# 需要通过grayland判断是否为陆地，130陆地，96水
# 陆地灰度减去20.5
# 海灰度减去18(暂时不考虑)
# 水灰度减去24.5

def final_satellite(data, mask, x, y, scale = 7, all = False, log = False):
    data = process_satellite(data, mask, True)
    visible = data[:,:,0]
    infra = data[:,:,1]
    gray = get_grayland(x,y,scale,log)
    # for i,e in enumerate(visible):
    #     for j,num in enumerate(e):
    #         if gray[i][j] == 130:
    #             visible[i][j] = max(0,num - 20.5)
    #         else:
    #             visible[i][j] = max(0,num - 24.5)
    for i,e in enumerate(infra):
        for j,num in enumerate(e):
            # if gray[i][j] == 130:
                # infra[i][j] = max(0,num - 48.15)
                # pass
            # else:
                # infra[i][j] = max(0,num - 51.3)
                # pass
            infra[i][j] = max(0,num - 51.3)
    if all: return np.dstack((visible,infra))
    if np.max(visible) == 0: return infra
    return visible
    