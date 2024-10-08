# 균일확률변수 만들기
import numpy as np

np.random.rand(2)

def X(i):
    return np.random.rand(i) # 한 번씩 뽑은걸 i개로 보여주는

X(4)

# 베르누이 확률변수 모수: p 만들어보세요
# num = 3
# p = 0.5
def Y(num, p):
    x = np.random.rand(num)
    return np.where(x < p, 1, 0)

Y(num = 10000, p = 0.5).mean()

# 새로운 확률변수
# 가질 수 있는 값: 0, 1, 2
# 20%, 50%, 30%

def Z():
    x = np.random.rand(1)
    return np.where(x < 0.2, 0, np.where(x < 0.7, 1, 2))
           
Z()

p = np.array([0.2, 0.5, 0.3])
def Z(p):
    x = np.random.rand(1)
    p_cumsum = p.cumsum()
    return np.where(x < p_cumsum[0], 0, np.where(x < p_cumsum[1], 1, 2))

p = np.array([0.2, 0.5, 0.3])
Z(p)

# E[X]
sum(np.arange(4) * np.array([1, 2, 2, 1]) / 6) # 필기에 있는 확률분포표
