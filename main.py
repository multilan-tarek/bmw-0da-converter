import os

address = 0x200000
size = 65536
byte_count = 32

folder = "C:/Users/tarek/Desktop/E39/data/GD20/"

os.makedirs("output", exist_ok=True)

for file in os.listdir(folder):
    if not str(file).lower().endswith(".0da"):
        continue

    data = {}
    binary_data = bytearray()

    with open(os.path.join(folder, str(file)), "r") as data_file:
        bmw_data = data_file.read()
        data_file.close()

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

    for adr in range(address, address + size, byte_count):
        line_data = data.get(adr)

        if line_data is None:
            continue

        for line_byte in line_data:
            binary_data.append(line_byte)

    with open(f"output/{data_file_name}.BIN", "wb") as binary_file:
        binary_file.write(binary_data)
        binary_file.close()
