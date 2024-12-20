from snag7 import *
import snap7

# Regelstrecke

plc = snap7.client.Client()
plc.connect('192.168.0.1', 0, 1)

db1 = PLCDataBlock(1, 'DB_Main.db', plc)

print(db1.read('r_fan_power_percent'))

db1.write('b_fan_enable', False)
db1.write('r_fan_power_percent', 20)


plc.disconnect()

