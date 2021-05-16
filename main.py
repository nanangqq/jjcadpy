import ezdxf
from db import con

res = con.execute('select 1')
print(res.fetchall())


