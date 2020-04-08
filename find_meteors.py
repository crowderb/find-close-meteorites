import math
import requests

def calc_dist(lat1, lon1, lat2, lon2):
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    h = math.sin( (lat2 - lat1) / 2 ) ** 2 + \
      math.cos(lat1) * \
      math.cos(lat2) * \
      math.sin( (lon2 - lon1) / 2 ) ** 2

    return 6372.8 * 2 * math.asin(math.sqrt(h))

def get_dist(meteor):
    return meteor.get('distance', math.inf)
    
if __name__ == '__main__':
    my_loc = (29.424122, -98.493628)

    meteor_resp = requests.get('https://data.nasa.gov/resource/y77d-th95.json')
    meteor_data = meteor_resp.json()

    for meteor in meteor_data:
        if not ('reclat' in meteor and 'reclong' in meteor): continue
        meteor['distance'] = calc_dist(float(meteor['reclat']),
                                       float(meteor['reclong']),
                                       my_loc[0],
                                       my_loc[1])

    meteor_data.sort(key=get_dist)

    try:
        print(meteor_data[0:10])
    except UnicodeEncodeError as uee:
        print("UnicodeEncodeError:")
        print(type(uee))
        print(uee.args)
        print(uee)
    except Exception as ex:
        print(type(ex))
        print(ex.args)
        print(ex)
