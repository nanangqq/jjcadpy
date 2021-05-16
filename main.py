from sys import argv
import json
import ezdxf
from db import con

params = json.loads(argv[1])
# print(params['body'][0])
pnus = params['body']

res = con.execute('''
select jsonb_agg(st_asgeojson(st_transform(geometry, 5186))::jsonb) 
from seoul_jijuk_0501_4326 
where "A1" in (%s)'''%','.join(["'%s'"%pnu for pnu in pnus]))
data = res.fetchall()
# print(type(data))
# print(type(data[0]))
# print(type(data[0]['jsonb_agg']))
features = data[0]['jsonb_agg']
print(features)

doc = ezdxf.new()