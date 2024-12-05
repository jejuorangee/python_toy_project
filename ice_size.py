import pandas as pd
import matplotlib.pyplot as plt
import numpy as np  # numpy를 임포트하여 평균 계산

# 파일 경로
path = '경로' # 파일위치 경로
file_name = 'ice size count.csv' # CSV 파일 이름
file_path = path + file_name # 파일 경로

# CSV 파일 읽기
df = pd.read_csv(file_path, encoding='cp949')  # pd.read_csv == pandas의 함수로 CSV 파일을 읽어줌
                                    # cp949는 한글로 읽어들이기 위함

# 날짜 컬럼을 datetime 형식으로 변환
df['날짜'] = pd.to_datetime(df['날짜'].str.replace('년', '-').str.replace('월', '').str.replace('?', '').str.replace(' ', ''), errors='coerce')
# df['날짜'] 컬럼을ㄹ datetime 형식으로 변환
# str.replace == 문자열 내에 특정 문자를 다른 문자로 변환 
# pd.to_datetime == 문자열을 datetime 객체로 변환
# errors='coere'는 날짜 문자열을 datetime 형식으로 반환할 수 없을 때 해당 값을 Not a Time으로 설정 함

# 연도와 월 추출
# dt는 pandas의 datetime 객체에서 제공하는 속성이라 함
df['연도'] = df['날짜'].dt.year # 날짜 컬럼에서 year(연도)를 추출함
df['월'] = df['날짜'].dt.month # 날짜 컬럼에서 month(월)을 추출함 

# 연도별 평균값을 저장할 리스트
years = []  # 각 연도 리스트 초기화 
ice_size_avg = []  # 각 연도의 평균 해빙면적 리스트 초기화 

# 연도와 월을 결합하여 "연도-월" 형식으로 데이터를 필터링
for year in range(1981, 2024):  # 1981년부터 2023년까지 / range라는 파이썬 내장함수를 사용 (범위 지정)
    # 해당 연도와 1, 2, 3, 10, 11, 12월의 데이터만 추출
    filtered_data = df[(df['연도'] == year) & (df['월'].isin([1, 2, 3, 10, 11, 12]))]
                        # 위에서 추출한 연도와 반복문을 돌려서 나온 연도가 일치하면 true
                        # isin 메서를 사용하여 해당월이 추출한 df['월']에 포함된다면 true
    
    # 해당 연도의 해빙면적 평균 계산
    if len(filtered_data) > 0:  # 데이터가 있을 경우만 평균 계산 / len은 length
        avg_ice_size = filtered_data['북극 해빙면적 평균(10^6km)'].mean()
                            # mean() 메서드는 모든 값에 대해 평균을 구해줌
                            # filtered_data에 필터링된 데이터와 같은 행(row)에 있는 '북극 해빙면적 평균' 컬럼 값을 가지고 옴
        
        # 연도와 평균 해빙면적을 리스트에 추가
        years.append(year) # 반복문 돌려서 나온 year를 years에 저장
        ice_size_avg.append(avg_ice_size) # year와 일치하는 북해평 행 값을 ice_size_avg에 저장
        
        # 디버깅: 각 연도별 평균 출력
        print(f"Year: {year}, Average Ice Size: {avg_ice_size:.2f} (10^6 km²)")
        # f 는 f-String으로 { }안에 값을 바로 가져와서 사용할 수있음 / JS el표현식과 비슷한 느낌

# 데이터가 제대로 담겼는지 확인 (로그 출력)
print("연도별 평균 해빙면적:")
for i in range(len(years)): # years의 길이 만큼 range를 지정하여 반복문 수행
    print(f"Year: {years[i]}, Average Ice Size: {ice_size_avg[i]:.2f}")
    # years의 i번째 연도를 가지고오고 해빙면적 평균의 i번째 값을 가지고 오고 :.2f는 소수점 두자리 까지 반올림하여 출력

# 그래프 그리기
plt.figure(figsize=(16, 8)) # 그래프의 사이즈를 지정함 / figsize는 가로 세로의 크기 지정

# 연도별 해빙면적 평균 데이터 선 그래프
plt.plot(
    years, # x축 데이터 years
    ice_size_avg, # y축 데이터 해빙면적 평균
    color='tab:red', # 그래프 색은 red
    label='Ice Size Avg (10^6 km²)', # 그래프의 범례에 나타낼 텍스트
    linewidth=2 # 선의 두께 지정
)

# 각 데이터 포인트에 점 찍기
plt.scatter( # 각 그래프 데이터에 포인트 찍기
    years, # x축 데이터 years
    ice_size_avg, # y축 데이터 해빙면적 평균
    color='tab:red',  # 점 색상은 red
    zorder=5,  # 선 위에 점을 배치 / 우선 순위 배치 숫자가 크면 앞으로 옴
    label='Data Points' # 범례에 나타낼 텍스트 
)

# 그래프 제목 및 축 설정
plt.title('Ice Size Average (1981~2023 Winter)', fontsize=16) # 그래프 title 지정 / 글자 크기는 16
plt.xlabel('Year', fontsize=12) # x축 이름 지정 / 글자 크기는 12
plt.ylabel('Ice Size Avg (10^6 km²)', fontsize=12) # y축 이름 지정 / 글자 크기는 12

# x축 눈금 간격 설정 (연도 간격을 쉽게 보기 위해)
plt.xticks(years, fontsize=10, rotation=45) # x 축에 표시할 눈금 값 지정 / 글자 크기 10 / rotation == 기울기 45도
plt.grid(axis='y', linestyle='--', alpha=0.7) # y 축에만 그릴 그리드 지정/ linestyle == 선 모양 지정 '--' / alpha == 투명
        # axis에 'both'지정하면 x y 둘 다 그리드 표시

# 범례 추가
plt.legend(fontsize=12) # 그래프가 어떤 값인지 보여줌 / 글자 크기 12

# 그래프 레이아웃 조정 및 출력
plt.tight_layout() # 그래프의 모든 요소 레이아웃 최적화 / 공간 및 크기 조정

plt.show() # 그래프 출력하기
