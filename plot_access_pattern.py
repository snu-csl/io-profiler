#!/usr/bin/env python3
import matplotlib.pyplot as plt

# 데이터 파일 읽기
data = []
with open('io_log', 'r') as f:
    for line in f:
        parts = line.strip().split(',')
        if len(parts) == 5:
            io_type = int(parts[0])
            arrival_time = int(parts[1])
            elapsed_time = int(parts[2])
            lba = int(parts[3])
            size = int(parts[4])

            # LBA와 size 변환
            lba_actual = lba << 9
            size_actual = (size + 1) << 9

            data.append({
                'io_type': io_type,
                'arrival_time': arrival_time,
                'elapsed_time': elapsed_time,
                'lba': lba_actual,
                'size': size_actual
            })

# arrival time으로 정렬
data.sort(key=lambda x: x['arrival_time'])

# 가장 빠른 arrival time을 0으로 설정
if data:
    min_time = data[0]['arrival_time']
    for d in data:
        d['arrival_time'] -= min_time

# I/O type에 따라 데이터 분리
# 1 = Write (파란색), 2 = Read (빨간색)
write_ops = [d for d in data if d['io_type'] == 1]
read_ops = [d for d in data if d['io_type'] == 2]

# 플롯 생성
plt.figure(figsize=(14, 8))

# Write operations (파란색)
if write_ops:
    write_times = [op['arrival_time'] for op in write_ops]
    write_lbas = [op['lba'] for op in write_ops]
    plt.scatter(write_times, write_lbas, c='blue', s=10, alpha=0.6, label='Write')

# Read operations (빨간색)
if read_ops:
    read_times = [op['arrival_time'] for op in read_ops]
    read_lbas = [op['lba'] for op in read_ops]
    plt.scatter(read_times, read_lbas, c='red', s=10, alpha=0.6, label='Read')

plt.xlabel('Arrival Time', fontsize=12)
plt.ylabel('LBA', fontsize=12)
plt.title('LBA Access Pattern', fontsize=14)
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

# 그래프 저장 및 표시
plt.savefig('access_pattern.png', dpi=300, bbox_inches='tight')
print("Plot saved as 'access_pattern.png'")
