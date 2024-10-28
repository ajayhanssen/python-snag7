# python-snag7
Small python library for parsing .db-files exported from TIA-Portal.  
**Supported datatypes: Real, Int, Bool**
Export using "Generate source from block" in TIA.  
Create PLCDataBlock-Instance like this:
~~~
import snap7
from snag7 import PLCDataBlock

plc = snap7.client.Client() plc.connect('192.168.0.1', 0, 1)

db_num = 1

db1 = PLCDataBlock(db_num, 'path/to/.db', plc)
~~~

Access variables like this:
~~~
print(db1.data['bool_1']['value'])
print(db1.data['int_1']['value'])
~~~

Write variables like this:
~~~
db1.write('bool_1', True)
db1.write('int_1', 23)
~~~

Refresh loaded data using:
~~~
db1.refresh()
~~~