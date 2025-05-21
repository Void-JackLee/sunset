import requests
from PIL import Image
import os
from io import BytesIO
import numpy as np
import math

MAP_BLOCK_PIXEL_SIZE = 512
GRAY_BLOCK_PIXEL_SIZE = 256

def get_grayland(x,y,scale = 7,log = False):
    if not(os.path.exists('grayland')): os.makedirs('grayland')
    data = None
    if not(os.path.exists(f'grayland/{scale}_{x}_{y}.png')):
        emp = np.zeros((GRAY_BLOCK_PIXEL_SIZE,GRAY_BLOCK_PIXEL_SIZE))
        if log: print(f'[REQUEST] https://tiles.windy.com/tiles/v10.0/grayland/{scale}/{x}/{y}.png')
        r = requests.request('GET',f'https://tiles.windy.com/tiles/v10.0/grayland/{scale}/{x}/{y}.png')
        if r.status_code == 200:
            data = Image.open(BytesIO(r.content)).convert('L')
            data.save(f'grayland/{scale}_{x}_{y}.png')
        else: return emp
    else:
        if log: print(f'[READ] grayland/{scale}_{x}_{y}.png') 
        data = Image.open(f'grayland/{scale}_{x}_{y}.png')
    data = np.array(data,dtype=np.uint8)
    return data

# 当scale = 4时，range为(0,16)
def get_map(rangeLongitude,rangeLatitude,scale = 7,log = False):
    if not(os.path.exists('simple-retina')): os.makedirs('simple-retina')
    emp = np.zeros((MAP_BLOCK_PIXEL_SIZE,MAP_BLOCK_PIXEL_SIZE))
    m = []
    for y in range(rangeLatitude[0],rangeLatitude[1]):
        line = []
        for x in range(rangeLongitude[0],rangeLongitude[1]):
            data = None
            if not(os.path.exists(f'simple-retina/{scale}_{x}_{y}.png')):
                if log: print(f'[REQUEST] https://tiles.windy.com/tiles/v10.0/simple-retina/{scale}/{x}/{y}.png')
                r = requests.request('GET',f'https://tiles.windy.com/tiles/v10.0/simple-retina/{scale}/{x}/{y}.png')
                if r.status_code == 200:
                    data = Image.open(BytesIO(r.content))
                    data.save(f'simple-retina/{scale}_{x}_{y}.png')
                    data = np.array(data,dtype=np.uint8)
                    if data.shape[0] == 256: data = emp
                else: data = emp
            else:
                if log: print(f'[READ] simple-retina/{scale}_{x}_{y}.png') 
                data = Image.open(f'simple-retina/{scale}_{x}_{y}.png')
                data = np.array(data,dtype=np.uint8)
                if data.shape[0] == 256: data = emp
            line.append(data)
        line = np.hstack(line)
        m.append(line)
    m = np.vstack(m)
    return m


# 墨卡托merator坐标取值范围[-20037508.34,20037508.34]这个数字就是地球赤道周长
def wgs84_to_mercator(lat, lng):
    x = lng * 20037508.34 / 180
    y = math.log(math.tan((90 + lat) * math.pi / 360)) / (math.pi / 180)
    y = y * 20037508.34 / 180
    return x, y

def mercator_to_wgs84(x, y):
    originShift = math.pi * 6378137
    lon = (x / originShift) * 180
    lat = (y / originShift) * 180
    lat = 180 / math.pi * (2 * math.atan(math.exp(lat * math.pi / 180)) - math.pi / 2)
    return lon, lat

def get_pixel_xy(x,y,dpi):
    a = 20037508.34
    x = (x + a) / a / 2 * dpi
    y = (a - y) / a / 2 * dpi
    return x, y

def scale_to_block_cnt(scale):
    return 1 << scale

# 获取对应分幅index
def get_block_index(px,py,block_size):
    return int(px // block_size), int(py // block_size)

# 获取从特定块作为原点的坐标
def get_pos_in_blocks(px,py,left_top_index_x,left_top_index_y,block_size):
    return px - left_top_index_x * block_size, py - left_top_index_y * block_size

def get_xy_in_blocks(lat,lng,scale = 7,offsetX=0,offsetY=0,beginX=None,beginY=None):
    # 获取墨卡托坐标
    mx,my = wgs84_to_mercator(lat,lng)
    # 获取平面地图坐标
    px,py = get_pixel_xy(mx,my,MAP_BLOCK_PIXEL_SIZE * scale_to_block_cnt(scale))
    # 获取坐标所在的区块
    bx,by = get_block_index(px,py,MAP_BLOCK_PIXEL_SIZE)
    if beginX == None: beginX = bx
    if beginY == None: beginY = by
    # 获取区块内的坐标
    return get_pos_in_blocks(px,py,beginX + offsetX,beginY + offsetY,MAP_BLOCK_PIXEL_SIZE)

def get_batch_block_range(dots,scale = 7):
    max_bx = -1
    max_by = -1
    min_bx = -1
    min_by = -1
    for lat,lng in dots:
        # 获取墨卡托坐标
        mx,my = wgs84_to_mercator(lat,lng)
        # 获取平面地图坐标
        px,py = get_pixel_xy(mx,my,MAP_BLOCK_PIXEL_SIZE * scale_to_block_cnt(scale))
        # 获取坐标所在的区块
        bx,by = get_block_index(px,py,MAP_BLOCK_PIXEL_SIZE)
        max_bx = max(max_bx,bx)
        max_by = max(max_by,by)
        if min_bx == -1:
            min_bx = bx
        if min_by == -1:
            min_by = by
        min_bx = min(min_bx,bx)
        min_by = min(min_by,by)
    return min_bx,min_by,max_bx,max_by

def get_batch_pos(dots,min_bx,min_by,scale=7):
    res = []
    # 获取区块内的坐标
    for lat,lng in dots:
        res.append(get_xy_in_blocks(lat,lng,scale,beginX=min_bx,beginY=min_by))
    return res