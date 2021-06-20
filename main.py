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
from ( 
    select 
        "A1",
        "A3",
        "A5",
        st_transform(geometry, 5186),
        st_transform(st_pointonsurface(geometry), 5186)
    from seoul_jijuk_0501_4326
    where "A1" in (%s)
    ) as t(
        pnu,
        dong_name,
        jibun,
        geom,
        center_point
    );
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
dong_names = {}
for f in features['features']:
    # print(f)
    if f['geometry']['type'] in shapes:
        # print(f['properties']['center_point'])
        center_point = f['properties']['center_point']['coordinates']

        pnu = f['properties']['pnu']
        # print(pnu)
        land_block = doc.blocks.new(name=pnu, base_point=center_point)

        polygon = f['geometry']['coordinates']
        for pts in polygon:
            # msp.add_lwpolyline(pts)
            land_block.add_lwpolyline(pts)

        # print(f['properties']['dong_name'])
        dong_name = f['properties']['dong_name']
        if dong_name in dong_names:
            dong_names[dong_name].append(f['properties']['pnu'])
        else:
            dong_names[dong_name] = [f['properties']['pnu']]

        name = f['properties']['jibun']
        # print(name)
        # msp.add_text(name, {'height':5}).set_pos(center_point, align='MIDDLE_CENTER')
        land_block.add_text(name, {'height':5}).set_pos(center_point, align='MIDDLE_CENTER')
        msp.add_blockref(pnu, center_point)


hashStr = getHashStr(str(pnus)+str(time.time()))
most_number_dong = sorted(dong_names.keys(), key=lambda dong_name: len(dong_names[dong_name]))[0]
filename = 'jj_%s_%s.dxf'%(most_number_dong.replace(' ', '_'), hashStr[:6])
# out_path = '../out/'+filename
out_path = os.path.join(out_dir, filename)
doc.saveas(out_path)
print(filename)
