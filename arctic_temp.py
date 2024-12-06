import pandas as pd
import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt

# NC 파일 로드
path = "경로"
file_name = 'HadCRUT.5.0.2.0.analysis.anomalies.ensemble_mean.nc'
file_path = path + file_name

# NC 파일 열기
dataset = nc.Dataset(file_path, 'r')

# 변수명, 타입, 샘플데이터 확인
for data in dataset.variables:
    # 샘플 데이터 출력
    sample = dataset.variables[data][:2]

    # 결측치 np.nan 처리
    if isinstance(sample, np.ma.MaskedArray):
        sample = sample.filled(np.nan)
    
    print("name = ", data)
    print("Type = ", dataset.variables[data].dtype)
    print("time = ", dataset.variables['time'])
    print("sample = ", sample)
    print('----------------------')

# 온도 변수 접근
temperature = dataset.variables['tas_mean']

# 위도, 경도, 시간 정보 추출
latitude = dataset.variables['latitude'][:]
longitude = dataset.variables['longitude'][:]
time = dataset.variables['time'][:]  # 시간 데이터
time_units = dataset.variables['time'].units  # 시간 단위 정보

print("Latitude length = ", len(latitude))
print("Longitude length = ", len(longitude))
print("Time length = ", len(time))
print("temperature length = ", len(temperature))

# 북극 위도를 찾아내, 해당 인덱스의 온도데이터 추출
latitude_arctic = np.where((latitude >= 60) & (latitude <= 90))[0]
## 북극 위도 찾아내 해당 위도값 추출, np.where() = 조건을 만족하는 인덱스 반환
temperature_arctic = temperature[:, latitude_arctic, :]

## 북극 위도만 조건식으로 걸어 데이터 정제
print('temperature_arctic sample1 = ',temperature_arctic[0])
print('temperature_arctic sample2 = ',temperature_arctic[1])

# 날짜 변환
time_units = time_units.split('since')[1].strip()
time_dates = pd.to_datetime(time, unit='D', origin=pd.Timestamp(time_units))
## time_unit =  days since 1850-01-01 00:00:00
## time_units.split('since') = {'days', '1850-01-01 00:00:00'} since를 기준으로 인덱스를 나누어 배열 반환
## time_units.split('since')[1].strip() = 인덱스 1번 요소 1850-01-01 00:00:00를 추출후 공백제거

## pd.to_datetime() = 주어진 일수를 실제 날짜로 변환하는 Pandas 라이브러리의 함수
## time =  NetCDF 파일에서 가져온 일수, origin으로 지정한 기준날짜에서 몇일이 지난시점의 데이터인지 판별
## origin=pd.Timestamp(time_units) = 추출한 1850-01-01 00:00:00를 날짜데이터로 변환이후 기준날짜로 적용
## Timestamp = Pandas의 Timestamp 객체 반환
print('time_dates = ',time_dates)

# 60°N에서 90°N까지의 평균 온도를 각 시간에 대해 계산
temperature_arctic_avg = temperature_arctic.mean(axis=(1, 2))
## axis 매개변수 = (시간, 위도, 경도) 3개 차원의 배열중 인덱스 1,2번(위도, 경도) 평균 계산
print("time_dates len = ",len(time_dates))
print("temperature_arctic_avg len = ",len(temperature_arctic_avg))

# 연도별 평균 온도 계산
time_years = time_dates.year
## pandas 날짜데이터의 연도만 추출
yearly_avg_temp = []
for year in range(time_years.min(), time_years.max() + 1):
    ## 첫번째 연도 ~ 마지막 연도 데이터 for문
    yearly_data = temperature_arctic_avg[time_years == year]
    yearly_avg_temp.append(np.mean(yearly_data))
    ## 같은 연도에 데이터를 전부 1개의 배열에 담아 평균값 구함

## 월별 분포되어있는 [시간][위도][경도] 데이터를 해당 시간에 따른 북극(위도60~90)전지역의 온도 평균값 추출
## 추출한 월별 북극 평균 데이터에 연도가 같은 온도데이터들의 평균값 추출
## 시간데이터(time_dates)와 온도데이터(temperature)는 1:1 관계이기때문

# 연도 리스트
years = list(range(time_years.min(), time_years.max() + 1))

# 그래프 그리기
plt.figure(figsize=(10, 6))

# 연평균 온도 그래프
plt.plot(years, yearly_avg_temp, color='red', label='60°N to 90°N Temperature (Arctic)', linewidth=2)

# 그래프 제목과 레이블 설정
plt.title('Yearly Average Temperature for 60°N to 90°N (Arctic)', fontsize=14)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Temperature (ºC)', fontsize=12)

# x축 레이블 회전
plt.xticks(rotation=45)
# 범례 추가
plt.legend()

# 그래프 출력
plt.tight_layout()
plt.show()
