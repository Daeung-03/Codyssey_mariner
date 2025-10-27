import pandas as pd
import matplotlib.pyplot as plt


def read_concat():
    # CSV 파일 읽기
    train_origin = pd.read_csv('train.csv')
    test_origin = pd.read_csv('test.csv')

    # 병합
    all_data = pd.concat(
        [train_origin, test_origin], axis=0, ignore_index=True
    )

    # 전체 데이터 행 개수
    total_rows = len(all_data)
    print(f'전체 데이터 수량: {total_rows}개')

    return train_origin


# Transported와의 상관계수 계산 (수동 구현)
def calculate_correlation(x, y):
    # 결측치 제거
    valid_idx = (~x.isna()) & (~y.isna())
    x_valid = x[valid_idx]
    y_valid = y[valid_idx]

    if len(x_valid) < 2:
        return 0

    # 평균 계산
    x_mean = sum(x_valid) / len(x_valid)
    y_mean = sum(y_valid) / len(y_valid)

    # 편차 계산
    x_diff = [xi - x_mean for xi in x_valid]
    y_diff = [yi - y_mean for yi in y_valid]

    # 공분산 계산
    covariance = sum(
        [x_diff[i] * y_diff[i] for i in range(len(x_diff))]
    ) / len(x_diff)

    # 표준편차 계산
    x_std = (sum([xd**2 for xd in x_diff]) / len(x_diff)) ** 0.5
    y_std = (sum([yd**2 for yd in y_diff]) / len(y_diff)) ** 0.5

    # 상관계수
    if x_std == 0 or y_std == 0:
        return 0
    return covariance / (x_std * y_std)


def cal(train_origin):
    # train 데이터만 사용 (Transported 값이 있는 데이터)
    train_data = train_origin.copy()

    # Boolean 컬럼을 수치형으로 변환 (먼저 변환!)
    bool_cols = ['CryoSleep', 'VIP', 'Transported']
    for col in bool_cols:
        if col in train_data.columns:
            train_data[col] = train_data[col].map({True: 1.0, False: 0.0})

    # 수치형 컬럼 선택 (변환 후에 선택!)
    numeric_cols = train_data.select_dtypes(
        include=['float64', 'int64']
    ).columns.tolist()

    all_relationships = []

    # 전체 평균 전송 비율 계산
    transported_ratio = train_data['Transported'].mean()

    # 수치형 변수의 상관관계 계산
    transported_series = train_data['Transported']
    for col in numeric_cols:
        if col != 'Transported':
            corr = calculate_correlation(train_data[col], transported_series)
            all_relationships.append(
                {'Feature': col, 'Value': corr, 'Abs_Value': abs(corr)}
            )

    transported_ratio = train_data['Transported'].mean()
    # 범주형 변수 - Cabin Deck 분석
    cabin_data = train_data[train_data['Cabin'].notna()].copy()
    cabin_data['Deck'] = cabin_data['Cabin'].str.split('/').str[0]

    decks = sorted(cabin_data['Deck'].unique())
    for deck in decks:
        deck_passengers = cabin_data[cabin_data['Deck'] == deck]
        transported = len(deck_passengers[deck_passengers['Transported'] == 1])
        total = len(deck_passengers)
        if total > 0:
            ratio = transported / total
            ratio -= transported_ratio
        else:
            ratio = 0

        all_relationships.append(
            {
                'Feature': f'Deck_{deck}',
                'Value': ratio,
                'Abs_Value': abs(ratio),
            }
        )

    # 범주형 변수 - HomePlanet 분석
    planet_data = train_data[train_data['HomePlanet'].notna()].copy()
    planets = sorted(planet_data['HomePlanet'].unique())

    for planet in planets:
        planet_passengers = planet_data[planet_data['HomePlanet'] == planet]
        transported = len(
            planet_passengers[planet_passengers['Transported'] == 1]
        )
        total = len(planet_passengers)
        if total > 0:
            ratio = transported / total
            ratio -= transported_ratio
        else:
            ratio = 0

        all_relationships.append(
            {
                'Feature': f'HomePlanet_{planet}',
                'Value': ratio,
                'Abs_Value': abs(ratio),
            }
        )

    # 범주형 변수 - Destination 분석
    dest_data = train_data[train_data['Destination'].notna()].copy()
    destinations = sorted(dest_data['Destination'].unique())

    for dest in destinations:
        dest_passengers = dest_data[dest_data['Destination'] == dest]
        transported = len(dest_passengers[dest_passengers['Transported'] == 1])
        total = len(dest_passengers)
        if total > 0:
            ratio = transported / total
            ratio -= transported_ratio
        else:
            ratio = 0

        all_relationships.append(
            {
                'Feature': f'Destination_{dest}',
                'Value': ratio,
                'Abs_Value': abs(ratio),
            }
        )

    # TOP 5 출력
    sorted_relationships = sorted(
        all_relationships, key=lambda x: x['Abs_Value'], reverse=True
    )

    for i, item in enumerate(sorted_relationships[:5], 1):
        feature = item['Feature']
        value = item['Value']

        value_str = f'{value:+.4f}'
        print(f'{i:<5} {feature:<30} {value_str:<10}')


def group_by_age(age):
    if age < 20:
        return '10'
    elif age < 30:
        return '20'
    elif age < 40:
        return '30'
    elif age < 50:
        return '40'
    elif age < 60:
        return '50'
    elif age < 70:
        return '60'
    else:
        return '70+'


def aeg(train_origin):
    train_data = train_origin.copy()

    # 연령대 별 통계 출력
    age_data = train_data[
        (train_data['Age'] >= 10)
        & (train_data['Age'].notna())
        & (train_data['Transported'].notna())
    ].copy()

    age_data['AgeGroup'] = [group_by_age(age) for age in age_data['Age']]

    age_groups = ['10', '20', '30', '40', '50', '60', '70+']
    transported_counts = []

    for group in age_groups:
        group_data = age_data[age_data['AgeGroup'] == group]
        transported = len(group_data[group_data['Transported'] == 1])
        transported_counts.append(transported)

    # 연령대별 전송 비율 출력
    for i, group in enumerate(age_groups):
        total = len(age_data[age_data['AgeGroup'] == group])
        if total > 0:
            ratio = transported_counts[i] / total * 100
            print(f'{group}: {ratio:.4f}%')

    # 그래프 그리기
    plt.figure(figsize=(12, 6))
    x_pos = range(len(age_groups))
    width = 0.35

    plt.bar([x for x in x_pos], transported_counts, width, label='Transported')

    plt.xlabel('age', fontsize=12)
    plt.ylabel('numbers', fontsize=12)
    plt.title('Transported by age', fontsize=14, fontweight='bold')
    plt.xticks(x_pos, age_groups)
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.show()


def main():
    train_origin = read_concat()
    print('\n')
    cal(train_origin)
    print('\n')
    aeg(train_origin)


if __name__ == '__main__':
    main()
