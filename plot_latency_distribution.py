#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np

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

# Read operations (type 2)만 필터링
read_ops = [d for d in data if d['io_type'] == 2]

if not read_ops:
    print("No read operations found!")
    exit(1)

# elapsed time을 ns에서 us로 변환
elapsed_times_us = [op['elapsed_time'] / 1000.0 for op in read_ops]

# 최소/최대 latency 찾기
min_latency = min(elapsed_times_us)
max_latency = max(elapsed_times_us)

print(f"Min latency: {min_latency:.2f} us")
print(f"Max latency: {max_latency:.2f} us")
print(f"Total read commands: {len(read_ops)}")

# 20개 구간으로 나누기
num_bins = 20
bin_edges = np.linspace(min_latency, max_latency, num_bins + 1)

# 각 구간에 속하는 커맨드 개수 계산
counts, _ = np.histogram(elapsed_times_us, bins=bin_edges)

# 각 bin의 중심값 계산 (x축 레이블용)
bin_centers = [(bin_edges[i] + bin_edges[i+1]) / 2 for i in range(num_bins)]

# Bar chart 그리기
plt.figure(figsize=(14, 8))
plt.bar(range(num_bins), counts, width=0.8, edgecolor='black', alpha=0.7)

# x축 레이블 설정 (각 구간의 범위 표시)
x_labels = [f"{bin_edges[i]:.1f}-\n{bin_edges[i+1]:.1f}" for i in range(num_bins)]
plt.xticks(range(num_bins), x_labels, rotation=45, ha='right', fontsize=9)

plt.xlabel('Latency Range (us)', fontsize=12)
plt.ylabel('Number of Commands', fontsize=12)
plt.title('Read Command Latency Distribution', fontsize=14)
plt.grid(True, axis='y', alpha=0.3)
plt.tight_layout()

# 통계 정보 출력
print(f"\nLatency distribution (20 bins):")
for i in range(num_bins):
    print(f"Bin {i+1:2d}: [{bin_edges[i]:8.2f} - {bin_edges[i+1]:8.2f}] us: {counts[i]:5d} commands")

# 그래프 저장 및 표시
plt.savefig('latency_distribution.png', dpi=300, bbox_inches='tight')
print("\nPlot saved as 'latency_distribution.png'")
