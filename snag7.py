import re
import snap7
from snap7.util import get_real, set_real, get_int, set_int, get_bool, set_bool

class PLCDataBlock:
    def __init__(self, db_number, db_path, plc):
        self.db_number = db_number
        self.db_path = db_path
        self.plc = plc
        self.data = {}
        self.data_types = {
            'Real': {'size': 4, 'read': get_real, 'write': set_real},
            'Int': {'size': 2, 'read': get_int, 'write': set_int},
            'Bool': {'size': 1, 'read': get_bool, 'write': set_bool}
        }
        self._parse_db_file()
        self.refresh()

    def _parse_db_file(self):
        with open(self.db_path, 'r') as file:
            content = file.read()

        # Find all variables in the VAR block
        var_pattern = r'(\w+)\s*:\s*(\w+);'
        matches = re.findall(var_pattern, content)

        byte_offset = 0
        bit_offset = 0  # Track bit offset for boolean variables
        for var_name, var_type in matches:
            if var_type == 'Bool':
                # Assign Bool to current byte and bit offset
                self.data[var_name] = {'type': var_type, 'byte_offset': byte_offset, 'bit_offset': bit_offset}
                bit_offset += 1
                # Move to the next byte if 8 bits (1 byte) have been filled
                if bit_offset == 8:
                    bit_offset = 0
                    byte_offset += 1
            elif var_type in self.data_types:
                # If non-boolean, make sure the next Bool starts in a new byte
                if bit_offset > 0:
                    byte_offset += 1
                    bit_offset = 0
                self.data[var_name] = {'type': var_type, 'byte_offset': byte_offset}
                byte_offset += self.data_types[var_type]['size']

    def refresh(self):
        """Refreshes the data values by reading them from the PLC."""
        db_size = self._calculate_db_size()
        db_data = self.plc.read_area(snap7.types.Areas.DB, self.db_number, 0, db_size)

        for var_name, var_info in self.data.items():
            var_type = var_info['type']
            offset = var_info['byte_offset']
            if var_type == 'Bool':
                bit_offset = var_info['bit_offset']
                self.data[var_name]['value'] = get_bool(db_data, offset, bit_offset)
            else:
                self.data[var_name]['value'] = self.data_types[var_type]['read'](db_data, offset)

    def write(self, var_name, value):
        """Writes the value back to the PLC."""
        if var_name not in self.data:
            raise ValueError(f"Variable {var_name} not found in the data block.")

        var_info = self.data[var_name]
        var_type = var_info['type']
        offset = var_info['byte_offset']
        
        # Read the entire DB, modify the value, and then write back
        db_size = self._calculate_db_size()
        db_data = self.plc.read_area(snap7.types.Areas.DB, self.db_number, 0, db_size)

        if var_type == 'Bool':
            bit_offset = var_info['bit_offset']
            set_bool(db_data, offset, bit_offset, value)
        else:
            self.data_types[var_type]['write'](db_data, offset, value)

        # Write modified data back to the PLC
        self.plc.write_area(snap7.types.Areas.DB, self.db_number, 0, db_data)

    def _calculate_db_size(self):
        """Calculates the total size of the DB."""
        total_size = 0
        for var_info in self.data.values():
            var_type = var_info['type']
            if var_type == 'Bool':
                total_size = max(total_size, var_info['byte_offset'] + 1)
            else:
                total_size += self.data_types[var_type]['size']
        return total_size

# Example usage
if __name__ == "__main__":
    plc = snap7.client.Client()
    plc.connect('192.168.0.1', 0, 1)  # Adjust IP and rack/slot accordingly

    # Create a PLCDataBlock object
    db1 = PLCDataBlock(1, 'path/to/your/db/file.db', plc)

    # Access values
    print(db1.data['vx']['value'])

    # Refresh data from PLC
    db1.refresh()

    # Write a value back to the PLC
    db1.write('di_1', True)  # Example to write a boolean

    # Close connection
    plc.disconnect()
