# 인터프리트언어의 고유한 별칭설정
import matplotlib.pyplot as plt
import pandas as pd

path = '경로'
file_name = 'earth_heating.csv'
file_path = path + file_name

# pandas로 CSV 파일 읽기
df = pd.read_csv(file_path,encoding='cp949')

print(df.columns)

df['년'] = df['날짜'].str.extract(r'(\d{4})')
year_avg_temp = df.groupby('년')['전지구 평균'].mean()

# 연도 인덱스를 정수형으로 변환
year_avg_temp.index = year_avg_temp.index.astype(int)

#그래프 그리기
plt.figure(figsize=(10,6))
year_avg_temp.plot(kind='line')

# x축 범위 설정 (1981년부터 2024년까지)
plt.xlim(1981, 2024)

# x축 라벨 포맷 설정 (1981년과 2024년 포함, 그 사이 5년 간격)
tick_labels = [str(year) for year in range(1981, 2024, 5)]  # 1981년부터 2024년까지 5년 간격
tick_positions = [year for year in range(1981, 2024, 5)]  # x축에서 표시할 위치를 5년 간격으로 설정

# 2024년을 추가하여 무조건 표시되도록 설정
if 2024 not in tick_positions:
    tick_positions.append(2024)
    tick_labels.append('2024')

# 1981년도 포함되도록 확인
if 1981 not in tick_positions:
    tick_positions.append(1981)
    tick_labels.append('1981')

# x축 값 설정
plt.xticks(tick_positions, tick_labels, rotation=45)

plt.title('yearly_earth_avg_temp(1981-2024)')
plt.xlabel('yearly')
plt.ylabel('avg_temp')
plt.grid(False)
plt.tight_layout()

#그래프 표시
plt.show()
