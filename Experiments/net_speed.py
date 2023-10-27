from speedtest import Speedtest as ST

st = ST()

# print(st.get_servers())
# print(st.get_best_server())
speed = st.download() / 1_000_000 # MBit/s
print(f'{speed:.2f}')
