import pandas as pd
import matplotlib.pyplot as plt

# 한글 폰트 설정 (Mac의 경우)
plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False


def read_csv():
    # 일반 가구원 제외 나머지 항목 제거
    origin_df = pd.read_csv('problem.csv')
    df_filtered = origin_df[['시점', '연령별', '성별', '일반가구원']].copy()
    # print(df_filtered.to_string(index=False))
    return df_filtered


def print_gender(origin_df):
    # 1. 성별 계 제외, 2. 연령별은 합계만 사용, 3. 일반 가구원만 출력
    gender_stats = origin_df[
        (origin_df['성별'].isin(['남자', '여자']))
        & (origin_df['연령별'] == '합계')
    ][['시점', '성별', '연령별', '일반가구원']].copy()
    print(gender_stats.to_string(index=False))


def print_age(origin_df):
    # 1. 성별 구분 X, 2. 연령별 합계 출력
    filtered_df = origin_df[(origin_df['성별'] == '계')].copy()
    age_stats = filtered_df.groupby('연령별', as_index=False)[
        '일반가구원'
    ].sum()
    print(age_stats.to_string(index=False))


def print_age_gender(origin_df):
    # . 1. 남자, 여자 데이터 필터링 2. 연령별, 성별로 그룹화 3. 일반 가구원 합계 계산 4. pivot을 사용해서 성별을 컬럼으로 변환
    filtered_df = origin_df[origin_df['성별'].isin(['남자', '여자'])].copy()
    age_gender_stats = (
        filtered_df.groupby(['연령별', '성별'])['일반가구원']
        .sum()
        .reset_index()
    )
    pivot_stats = age_gender_stats.pivot(
        index='연령별', columns='성별', values='일반가구원'
    ).reset_index()
    print(pivot_stats.to_string(index=False))
    return pivot_stats


def draw_graph(graph_data):
    plt.figure(figsize=(12, 6))
    plt.plot(
        graph_data['연령별'], graph_data['남자'], marker='o', label='남자'
    )
    plt.plot(
        graph_data['연령별'], graph_data['여자'], marker='o', label='여자'
    )
    plt.xlabel('연령별')
    plt.ylabel('일반가구원')
    plt.title('연령별 일반가구원 데이터 통계')
    plt.xticks(rotation=45, ha='right')  # x축 레이블 45도 회전
    plt.grid(True, alpha=0.3)
    plt.legend()

    # log scale
    # plt.yscale('log')

    plt.tight_layout()  # 레이아웃 자동 조정
    plt.show()


def main():
    df_filtered = read_csv()
    print(
        '\n=== 1. 2015년 이후 남자 및 여자의 연도별 일반가구원 데이터 통계 ==='
    )
    print_gender(df_filtered)
    print('\n=== 2. 2015년 이후 연령별 일반가구원 데이터 통계 ===')
    print_age(df_filtered)
    print(
        '\n=== 3. 2015년 이후 남자 및 여자의 연령별 일반가구원 데이터 통계 ==='
    )
    graph_data = print_age_gender(df_filtered)
    draw_graph(graph_data)


if __name__ == '__main__':
    main()
