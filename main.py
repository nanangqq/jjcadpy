from sys import argv
import json
import ezdxf
from db import con

params = json.loads(argv[1])
print(params)

res = con.execute('''select jsonb_agg(st_asgeojson(st_transform(geometry, 5186))::jsonb) from seoul_jijuk_0501_4326 where "A1" in ('1168010600109450010')''')
data = res.fetchall()
# print(type(data))
# print(type(data[0]))
# print(type(data[0]['jsonb_agg']))


