import numpy as np
import math

# 生成一个形状为 (1000, ) 的随机浮点数数组
random_array = np.random.uniform(size=1000)

# 计算每个元素的累积概率
cdf_array = np.arange(1.0, len(random_array) + 1) / len(random_array)

# 对数组进行排序
sorted_array = np.sort(random_array)

# 计算每个元素的累积概率
for i in range(len(sorted_array)):
    cdf_array[i] = np.sum(sorted_array[:i + 1])

# 打印 CDF 数据样本
print(cdf_array)