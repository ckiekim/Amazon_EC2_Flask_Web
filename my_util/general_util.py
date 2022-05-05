import numpy as np

# used in seoul.py
def get_text_location(geo_str):
    gu_dict = {}
    for gu in geo_str['features']:
        for coord in gu['geometry']['coordinates']:
            geo = np.array(coord)
            gu_dict[gu['id']] = [np.mean(geo[:,1]), np.mean(geo[:,0])]
    return gu_dict

# used in rcmd.py, clsf.py, aclsf.py, rgrs.py
def get_index(index_str, upper, lower=0):
    if not index_str:               # 입력값이 없는 경우
        return lower
    
    try:                            # 숫자를 입력하지 않은 경우
        index = int(index_str)
    except:
        return lower
    
    if lower <= index <= upper:
        return index
    return lower