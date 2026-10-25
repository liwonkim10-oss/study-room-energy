
import streamlit as st
import numpy as np
import pandas as pd
import random

# 1. 대시보드 기본 설정
st.set_page_config(
    page_title="자습실 에너지 최적화",
    layout="wide"
)

st.title("💡 자율학습실 좌석 배치 & 조명 에너지 절약 시뮬레이터")
st.caption("학생들의 착석 방식에 따른 조명 소비전력과 절약 효과를 분석합니다.")

# 2. 사이드바 환경 설정
st.sidebar.header("⚙️ 환경 설정")

total_students = st.sidebar.slider(
    "현재 출석 학생 수 (명)",
    min_value=1,
    max_value=24,
    value=8
)

strategy = st.sidebar.radio(
    "좌석 배정 전략",
    [
        "자율 착석 (랜덤 분산)",
        "구역 집중 배치 (에너지 최적화)"
    ]
)

light_power_per_zone = st.sidebar.number_input(
    "구역(조명)당 소비전력 (W)",
    min_value=1,
    max_value=1000,
    value=60,
    step=10
)

# 3. 좌석 및 구역 모델링
# 전체 좌석: 4행 x 6열 = 24석
# 구역별 좌석: 2행 x 3열 = 6석
seats = np.zeros((4, 6), dtype=int)

# 구역별 좌석 목록
zones = [
    [(r, c) for r in range(0, 2) for c in range(0, 3)],
    [(r, c) for r in range(0, 2) for c in range(3, 6)],
    [(r, c) for r in range(2, 4) for c in range(0, 3)],
    [(r, c) for r in range(2, 4) for c in range(3, 6)]
]

# 전체 좌석 목록
all_seat_indices = [
    (r, c)
    for r in range(4)
    for c in range(6)
]

# 4. 좌석 배정
if strategy == "자율 착석 (랜덤 분산)":
    # 전체 좌석 중 무작위로 학생 수만큼 선택
    chosen_seats = random.sample(
        all_seat_indices,
        total_students
    )
else:
    # 구역 집중 배치: 한 구역을 채운 뒤 다음 구역으로 이동
    chosen_seats = []

    for zone in zones:
        remaining_students = total_students - len(chosen_seats)

        if remaining_students <= 0:
            break

        seats_to_fill = min(
            remaining_students,
            len(zone)
        )

        chosen_seats.extend(zone[:seats_to_fill])

# 좌석 점유 상태 반영
# 1 = 착석, 0 = 빈자리
for r, c in chosen_seats:
    seats[r, c] = 1

# 5. 구역별 조명 가동 상태 계산
zone_status = []

for zone in zones:
    occupied = sum(
        seats[r, c]
        for r, c in zone
    )

    zone_status.append(1 if occupied > 0 else 0)

active_zones = sum(zone_status)

# 6. 소비전력 계산
total_power = active_zones * light_power_per_zone

# 전체 조명을 모두 켰을 때의 소비전력
max_possible_power = 4 * light_power_per_zone

# 절감 전력과 절감률
saved_power = max_possible_power - total_power

saved_percentage = (
    saved_power / max_possible_power * 100
    if max_possible_power > 0
    else 0
)

# 7. 핵심 지표 출력
st.subheader("📊 에너지 절약 분석 결과")

col1, col2, col3 = st.columns(3)

col1.metric(
    "가동 중인 조명 구역",
    f"{active_zones} / 4 구역"
)

col2.metric(
    "현재 소비전력",
    f"{total_power} W"
)

col3.metric(
    "절감 전력",
    f"{saved_power} W",
    f"{saved_percentage:.1f}% 절감"
)

st.divider()

# 8. 구역별 조명 상태
st.subheader("💡 구역별 조명 가동 상태")

zone_names = [
    "구역 1 (앞쪽 좌측)",
    "구역 2 (앞쪽 우측)",
    "구역 3 (뒤쪽 좌측)",
    "구역 4 (뒤쪽 우측)"
]

zone_data = pd.DataFrame({
    "조명 구역": zone_names,
    "착석 학생 수": [
        sum(seats[r, c] for r, c in zone)
        for zone in zones
    ],
    "조명 상태": [
        "ON 💡" if status == 1 else "OFF 🌙"
        for status in zone_status
    ],
    "소비전력 (W)": [
        status * light_power_per_zone
        for status in zone_status
    ]
})

st.table(zone_data)

st.divider()

# 9. 좌석 배치 현황
st.subheader("🪑 좌석 점유 현황")
st.caption("1 = 착석, 0 = 빈자리")

seat_display = pd.DataFrame(
    seats,
    index=[
        "A열 (앞쪽)",
        "B열 (앞쪽)",
        "C열 (뒤쪽)",
        "D열 (뒤쪽)"
    ],
    columns=[
        "1번석",
        "2번석",
        "3번석",
        "4번석",
        "5번석",
        "6번석"
    ]
)

st.table(seat_display)

# 10. 시뮬레이션 결과 해석
st.divider()
st.subheader("📝 시뮬레이션 해석")

st.write(
    f"현재 출석 학생은 {total_students}명이며, "
    f"{active_zones}개 조명 구역이 가동되고 있습니다."
)

st.write(
    f"현재 소비전력은 {total_power}W이며, "
    f"전체 조명을 켰을 때보다 "
    f"{saved_power}W를 절약하는 것으로 계산됩니다."
)

st.info(
    "이 결과는 학생이 한 명이라도 있는 구역의 조명을 켠다는 "
    "가정에 따른 시뮬레이션입니다. "
    "실제 전력 사용량을 측정한 결과는 아닙니다."
)
