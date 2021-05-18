from sys import argv
import json
import os
import ezdxf
import hashlib
import time
import numpy as np

from db import con

def getHashStr(string):
    return hashlib.sha256(string.encode()).hexdigest()

if len(argv)>1:
    params = json.loads(argv[1])
    # print(params['body'][0])
    pnus = params['body']
    out_dir = '../out'
else:
    pnus = ['1168010600109450010']
    out_dir = '../../../../out'

pnus_string = ','.join(["'%s'"%pnu for pnu in pnus])

sql = '''
select jsonb_build_object(
    'type', 'FeatureCollection',
    'features', jsonb_agg(ST_AsGeoJSON(t.*)::jsonb)
    )
from ( select "A1", "A5", st_transform(geometry, 5186) from seoul_jijuk_0501_4326
       where "A1" in (%s)
     ) as t(pnu, jibun, geom);
'''%pnus_string
# res = con.execute('''
# select jsonb_agg(st_asgeojson(st_transform(geometry, 5186))::jsonb) 
# from seoul_jijuk_0501_4326 
# where "A1" in (%s)'''%','.join(["'%s'"%pnu for pnu in pnus]))
res = con.execute(sql)
data = res.fetchall()
# print(type(data))
# print(type(data[0]))
# print(type(data[0]['jsonb_agg']))
# features = data[0]['jsonb_agg']
features = data[0]['jsonb_build_object']
# print(features)

doc = ezdxf.new()
# print(os.getcwd()) 
# => /root/share/np-api

shapes = {'Polygon': lambda x: x}
msp = doc.modelspace()
for f in features['features']:
    # print(f)
    if f['geometry']['type'] in shapes:
        polygon = f['geometry']['coordinates']
        for pts in polygon:
            msp.add_lwpolyline(pts)
            center = np.array(pts).mean(0)
            # print(center)
        name = f['properties']['jibun']
        # print(name)
        msp.add_text(name, {'height':5, 'insert': center})


hashStr = getHashStr(str(pnus)+str(time.time()))
filename = 'jj_%s.dxf'%hashStr
# out_path = '../out/'+filename
out_path = os.path.join(out_dir, filename)
doc.saveas(out_path)
print(filename)
