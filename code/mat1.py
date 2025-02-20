import numpy as np

# 종이필기 2번
# 벡터 * 벡터 (내적)
a = np.arange(1, 4)
b=np.array([3, 6, 9])

a.dot(b)

# 종이필기 4번
# 행렬 * 벡터 (곱셈)
a=np.array([1,2,3,4]).reshape((2,2), order='F') # 세로로 원소 채우기
b=np.array([5, 6]).reshape(2,1)

a @ b # 행렬 * 벡터 (곱셈) a.dot(b)랑 같은 형식

# 종이필기 5번
# 행렬 * 행렬
a=np.array([1,2,3,4]).reshape((2,2), order='F')
b=np.array([5,6, 7, 8]).reshape((2,2), order='F')
a@b

# Q1
a=np.array([1,2,1,0,2,3]).reshape(2,3)
b=np.array([1,0,-1,1,2,3]).reshape(3,2)
a@b

# Q2
np.eye(3) # 단위행렬
a=np.array([3,5,7,
            2,4,9,
            3,1,0]).reshape(3, 3)
a @ np.eye(3)

# transpose
a
a.transpose()
b=a[:, :2]
b
b.transpose()

# 회귀분석 데이터행렬
x=np.array([13, 15,
            12, 14,
            10, 11,
            5, 6]).reshape(4,2)
x

vec1=np.repeat(1,4).reshape(4,1)
matX=np.hstack((vec1, x))
# hstack과 vstack
# hstack 옆으로 결합, vstack 위아래로 결합
matX

beta_vec=np.array([2,0,1]).reshape(3,1)
beta_vec
matX @ beta_vec

y=np.array([20, 19, 20, 12]).reshape(4,1)
(y-matX @ beta_vec).transpose() @ (y-matX @ beta_vec)

# 역행렬
a=np.array([1,5,3,4]).reshape(2,2)
a_inv=(-1/11)*np.array([4,-5,-3,1]).reshape(2,2)

a@a_inv

# 3 by 3 역행렬
a=np.array([-4, -6, 2,
            5, -1, 3,
            -2, 4, -3]).reshape(3,3)
a_inv=np.linalg.inv(a)
a_inv
np.round(a @ a_inv, 3)

# 역행렬 존재하지 않는 경우 (선형종속)
b=np.array([1,2,3,
            2,4,5,
            3,6,7]).reshape(3,3)
b_inv=np.linalg.inv(b) # 에러남
np.linalg.det(b) #행렬식이 항상 0

# 베타 구하기 (회귀직선계수 구하는 부분)
matX
y
XtX_inv=np.linalg.inv((matX.transpose() @ matX))
Xty=matX.transpose() @ y
beta_hat = XtX_inv @ Xty
beta_hat
# =========================================================================
# 손실 함수
# (y−y^)T(y−y^)는 모델의 예측값과 실제값 간의 차이를 정량적으로 평가
# 이는 예측 오차의 제곱합으로, 모델의 성능을 측정하는 데 사용
# 회귀 계수 β가 변경되면 예측값이 달라지고, 그에 따라 손실 함수 값도 변경
# 이 손실 함수를 최소화하는 것이 모델 학습의 목표

# model fit으로 베타 구하기
from sklearn.linear_model import LinearRegression
model=LinearRegression()
model.fit(matX[:, 1:], y)
model.coef_
model.intercept_
# =========================================================================
# minimize로 베타 구하기
from scipy.optimize import minimize

# line_perform: 회귀계수 beta를 받아서 잔차 제곱합을 계산하는 함수
# 잔차 제곱합은 회귀 모델이 데이터를 얼마나 잘 설명하는지 나타내는 지표
def line_perform(beta): 
    beta=np.array(beta).reshape(3, 1)
    a=(y - matX @ beta) # matX @ beta = y_hat, a는 잔차
    return (a.transpose() @ a) # 잔차제곱합

line_perform([8.55, 5.96, -4.38]) # 목표함수, 이 함수의 값이 최소가 되도록 회귀계수 찾음

# 초기 추정값
initial_guess = [0, 0, 0] # 최적화의 시작점

# 최소값 찾기 (잔차 제곱합을 최소화하는 회귀계수 찾고자)
result = minimize(line_perform, initial_guess)

# 결과 출력
print("최소값:", result.fun)
print("최소값을 갖는 x 값:", result.x)
# =========================================================================
# minimize로 라쏘 베타 구하기
from scipy.optimize import minimize

def line_perform_lasso(beta): 
    beta=np.array(beta).reshape(3, 1)
    a=(y - matX @ beta)
    return (a.transpose() @ a) + 3*np.abs(beta).sum() # 일단 람다를 3으로 고정했으니

line_perform_lasso([8.55,  5.96, -4.38])
line_perform_lasso([3.76,  1.36, 0])

# 초기 추정값
initial_guess = [0, 0, 0] # 최적화의 시작점

# 최소값 찾기 (잔차 제곱합을 최소화하는 회귀계수 찾고자)
result = minimize(line_perform_lasso, initial_guess)

# 결과 출력
print("최소값:", result.fun)
print("최소값을 갖는 x 값:", result.x)
# =========================================================================
# minimize로 릿지 베타 구하기
from scipy.optimize import minimize

def line_perform_ridge(beta):
    beta=np.array(beta).reshape(3, 1)
    a=(y - matX @ beta)
    return (a.transpose() @ a) + 3*(beta**2).sum() # 일단 3으로 고정했으니

line_perform_ridge([8.55,  5.96, -4.38]) # 목표함수, 이 함수의 값이 최소가 되도록 회귀계수 찾음
line_perform_ridge([3.76,  1.36, 0])

# 초기 추정값
initial_guess = [0, 0, 0] # 최적화의 시작점

# 최소값 찾기 (잔차 제곱합을 최소화하는 회귀계수 찾고자)
result = minimize(line_perform_ridge, initial_guess)

# 결과 출력
print("최소값:", result.fun)
print("최소값을 갖는 x 값:", result.x)