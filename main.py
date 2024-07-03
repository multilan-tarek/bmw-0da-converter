address = 0x200000
size = 65536
byte_count = 32

file = "C:/Users/tarek/Desktop/E39/data/GD20/A7570735.0DA"

data = {}
binary_data = bytearray()

with open(file, "r") as data_file:
    bmw_data = data_file.read()

address_length = len(hex(address)[2:])
data_file_name = "output"

for line in bmw_data.splitlines():
    if line.startswith(";;K_File-Name:"):
        data_file_name = line.replace(";;K_File-Name:", "").strip()

    if not line.startswith(":"):
        continue

    line_address = int(line[1:address_length + 1], 16)

    if line_address < address or line_address > address + size:
        continue

    line_data = line[address_length + 3:-2]
    line_bytes = [(int(line_data[i:i + 2], 16)) for i in range(0, len(line_data), 2)]
    data[line_address] = line_bytes

for address in range(address, address + size, byte_count):
    line_data = data.get(address)

    if line_data is None:
        continue

    for line_byte in line_data:
        binary_data.append(line_byte)

with open(f"{data_file_name}.BIN", "wb") as binary_file:
    binary_file.write(binary_data)
