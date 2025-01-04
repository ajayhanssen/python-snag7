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
print(db1.data['real_1']['value'])
print(db1.data['bool_1']['value'])
print(db1.data['int_1']['value'])
~~~

Write variables like this:
~~~
db1.write('real_1, 3.0)
db1.write('bool_1', True)
db1.write('int_1', 23)
~~~

Refresh loaded data using:
~~~
db1.refresh()
~~~

Exported .db-file for this example looks like this:
~~~
DATA_BLOCK "test_db"
{ S7_Optimized_Access := 'FALSE' }
VERSION : 0.1
NON_RETAIN
   STRUCT 
      real_1 : Real;
      real_2 : Real;
      real_3 : Real;
      bool_1 : Bool;
      bool_2 : Bool;
      bool_3 : Bool;
      bool_4 : Bool;
      int_1 : Int;
      int_2 : Int;
   END_STRUCT;

BEGIN

END_DATA_BLOCK
~~~
Make sure "optimized access" is disabled on the datablock