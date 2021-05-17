from sys import argv
import json
import os
import ezdxf
from db import con

params = json.loads(argv[1])
# print(params['body'][0])
pnus = params['body']
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
print(features)

doc = ezdxf.new()
# print(os.getcwd()) 
# => /root/share/np-api

