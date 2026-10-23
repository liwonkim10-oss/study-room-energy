import streamlit as st 
import numpy as np
import pandas as pandas
import random

st.set_page_config(page_title="자습실 에너지 최적화",layout="wide")
st.title("자율학습실 좌석 배치 &조명 에너지 절약 시뮬레이터")
st.caption("학생 착석 방식(자율 분산 vs 구역 집중)에 따른 조명 전력 절감 효과르 분석합니다.")

st.sidebar.header("환경 설정")
total_students = st.sidebar.slider("현재 출석 학생 수 (명)",min_value=1, max_value=24,value=8)
strategy = st.sidebar.radio("좌석 배정 전략", ["자율 착석 (랜덤 분산)", "구역 집중 배치 (에너지 최적화)"])
light_power_per_zone= st.sidebar.number_input("구역(조명)당 소비전력 (W)",value=60,step=10)

seats = np.zeros((4,6),dtype=int)
all_seat_indices = [(r,c) for i in range(4) for c in range(6)]

if strategy == "자율 착석(랜덤 분산)":
chosen_seats = random.sample(all_seat_indices, total_students)
else:
chosen_seats = all_seat_indices[:total_students]

for r, c in chosen_seats:
seats[r, c] = 1

zone-status = [
    1 if np.sum(seats[0:2, 0:3]) > 0 else 0,
    1 if np.sum(seats[0:2, 3:6]) > 0 else 0,
    1 if np.sum(seats[2:4, 0:3]) > 0 else 0,
    1 if np.sum(seats[2:4, 3:6]) > 0 else 0
]

active_zones = sum(zone_status)
total_power = active_zones * light_power_per_zone
max_possible_power = 4 * light_power_per_zone
saved_power = max_possible_power -total_power

col1,col2,col3 = st.columns(3)
col1.metric("가동 중인 조명 구역," f"{active_zones}/4구역")
col2.metric("현재 소비전력", f"{total_power}W")
col3.metric("전체 점등 대비 절감 전력", f"{saved_power} W", f"{(saved_power/max_possible_power)*100:.1f}% 절감")

st.divider()

st.subheader("실시간 좌석 점유 현황 (1: 착석, 0:빈자리)")
seat_display = pd.DataFrame(
    seats,
    index=["A열(1분단)","B열(1분단)","C열(2분단)","D열(2분단)"],
    columns=["1번석","2번석","3번석","4번석","5번석","6번석"]
)
st.table(seat_display)
liwonkim10
