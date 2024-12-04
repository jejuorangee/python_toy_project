import pandas as pd
import matplotlib.pyplot as plt
import mplcursors  # mplcursors 추가

# 파일 경로
path = "경로" 
file_name = 'temp(2019.12~2022.02 seoul)+ao.csv'
file_path = path + file_name

# CSV 파일 읽기
data = pd.read_csv(file_path, encoding='cp949')

# '일시' 컬럼을 datetime 형식으로 변환
data['일시'] = pd.to_datetime(data['일시'])

# 연도와 월 추출
data['연도'] = data['일시'].dt.year
data['월'] = data['일시'].dt.month

# "겨울 연도" 정의: 12월은 현재 연도로, 1~2월은 이전 연도로 묶음
data['겨울연도'] = data.apply(lambda x: x['연도'] if x['월'] == 12 else x['연도'] - 1, axis=1)

# 겨울 데이터 필터링 (12월 ~ 2월만 선택)
winter_data = data[data['월'].isin([12, 1, 2])]

# x축 레이블을 'yyyy-MM-dd' 형식으로 설정
winter_data['x축'] = winter_data['일시'].dt.strftime('%Y-%m-%d')

# 그래프 그리기
plt.figure(figsize=(16, 8))

# 평균 기온 데이터 선 그래프
line1, = plt.plot(
    winter_data['x축'],
    winter_data['평균기온(°C)'],
    color='tab:red',
    label='Average Temperature (°C)',
    linewidth=1
)

# AO Index 데이터 선 그래프
line2, = plt.plot(
    winter_data['x축'],
    winter_data['ao_index_cdas'],
    color='tab:blue',
    label='AO Index',
    linewidth=1
)

# 0도 기준선 추가
plt.axhline(0, color='black', linewidth=1, linestyle='--', label='0°C')

# 그래프 제목 및 축 설정
plt.title('Winter Temperature and AO Index (2019 Winter ~ 2022 Winter)', fontsize=16)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Values', fontsize=12)

# x축 레이블을 적절한 간격으로 표시하기 위해 특정 날짜 간격 설정
# 예를 들어 1개월 간격으로 레이블을 표시
plt.xticks(
    ticks=winter_data['x축'][::30],  # 30번째 값마다 표시 (간격 조정 가능)
    labels=winter_data['x축'][::30],  # 해당 값들을 레이블로 설정
    rotation=45,  # 45도 회전
    fontsize=10  # 폰트 크기
)

# 범례 추가
plt.legend(fontsize=12)

# mplcursors를 이용한 마우스 hover 효과 추가
mplcursors.cursor([line1, line2], hover=True)

# 그래프 레이아웃 조정 및 출력
plt.tight_layout()
plt.show()
