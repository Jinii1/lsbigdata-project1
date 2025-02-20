# 필요한 패키지 불러오기
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# 워킹 디렉토리 설정
import os
cwd=os.getcwd()

## 필요한 데이터 불러오기
house_train=pd.read_csv("../../data/houseprice/train.csv")
house_test=pd.read_csv("../../data/houseprice/test.csv")
sub_df=pd.read_csv("../../data/houseprice/sample_submission.csv")

## NaN 채우기
# 각 숫치형 변수는 평균 채우기
# 각 범주형 변수는 Unknown 채우기
house_train.isna().sum()
house_test.isna().sum()

## 숫자형 채우기
quantitative = house_train.select_dtypes(include = [int, float])
quantitative.isna().sum()
quant_selected = quantitative.columns[quantitative.isna().sum() > 0]

for col in quant_selected:
    house_train[col].fillna(house_train[col].mean(), inplace=True)
house_train[quant_selected].isna().sum()

## 범주형 채우기
qualitative = house_train.select_dtypes(include = [object])
qualitative.isna().sum()
qual_selected = qualitative.columns[qualitative.isna().sum() > 0]

for col in qual_selected:
    house_train[col].fillna("unknown", inplace=True)
house_train[qual_selected].isna().sum()


# test 데이터 채우기
## 숫자형 채우기
quantitative = house_test.select_dtypes(include = [int, float])
quantitative.isna().sum()
quant_selected = quantitative.columns[quantitative.isna().sum() > 0]

for col in quant_selected:
    house_test[col].fillna(house_train[col].mean(), inplace=True)
house_test[quant_selected].isna().sum()

## 범주형 채우기
qualitative = house_test.select_dtypes(include = [object])
qualitative.isna().sum()
qual_selected = qualitative.columns[qualitative.isna().sum() > 0]

for col in qual_selected:
    house_test[col].fillna("unknown", inplace=True)
house_test[qual_selected].isna().sum()


house_train.shape
house_test.shape
train_n=len(house_train)

# 통합 df 만들기 + 더미코딩
# house_test.select_dtypes(include=[int, float])

df = pd.concat([house_train, house_test], ignore_index=True)
# df.info()
df = pd.get_dummies(
    df,
    columns= df.select_dtypes(include=[object]).columns,
    drop_first=True
    )
df

# train / test 데이터셋
train_df=df.iloc[:train_n,]
test_df=df.iloc[train_n:,]

## 이상치 탐색
train_df=train_df.query("GrLivArea <= 4500")

## train
train_x=train_df.drop("SalePrice", axis=1)
train_y=train_df["SalePrice"]

## test
test_x=test_df.drop("SalePrice", axis=1)

# Bootstrap: 무작위로 데이터를 여러 번 복제해서 뽑아냄
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import GridSearchCV

train_x.shape[0] # 행: 1458
btstrap_index1=np.random.choice(np.arange(1458), 1000, replace=True)
bts_train_x1=train_x.iloc[btstrap_index1,:]
bts_train_y1=np.array(train_y)[btstrap_index1] # train_y:series 형식이라

btstrap_index2=np.random.choice(np.arange(1458), 1458, replace=True)
bts_train_x2=train_x.iloc[btstrap_index2,:]
bts_train_y2=np.array(train_y)[btstrap_index2]

model = DecisionTreeRegressor(random_state=42,
                              max_features="sqrt") # 모델이 분기(split)를 만들 때 고려할 특성의 수를 제한하는 데 사용
# param_grid: hyper parameter 값의 후보들을 정의하는 딕셔너리
# 각 하이퍼 파라미터 이름을 키로 사용, 실햄해볼 값들의 리스트를 값으로 설정
param_grid={
    'max_depth': np.arange(7, 20, 1), # 질문을 몇 단계까지 할까?
    'min_samples_split': np.arange(10, 30, 1) # 몇 개의 데이터를 가지고 나눌까?
}
# max_features 주요옵션: None, sqrt, log2

# GridSearchCV: hyperparameter 최적화 자동 수행
# -> 모델의 성능을 판가름하는 hyper parameter 최적 조합 찾는 것 중요
# 교차검증 CV를 사용해 각 조합의 성능을 평가하여 최적의 hyper parameter 찾음
grid_search=GridSearchCV(
    estimator=model,
    param_grid=param_grid,
    scoring='neg_mean_squared_error',
    cv=5
)
grid_search.fit(bts_train_x1, bts_train_y1)
grid_search.best_params_
bts_model1=grid_search.best_estimator_

grid_search.fit(bts_train_x2, bts_train_y2)
grid_search.best_params_
bts_model2=grid_search.best_estimator_

bts1_y=bts_model1.predict(test_x)
bts2_y=bts_model2.predict(test_x)
(bts1_y + bts2_y)/2

# 평균