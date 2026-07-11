import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button, Slider

# --- 1. 수학 모델 정의 ---
def f(x):   return 3*x**4 + 4*x**3 + 1
def df(x):  return 12*x**3 + 12*x**2
def ddf(x): return 36*x**2 + 24*x

# --- 2. 데이터 및 환경 설정 ---
시간_데이터 = np.linspace(-1.5, 0.5, 200)

# 한글 깨짐 및 마이너스 기호 깨짐 방지 강제 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

fig = plt.figure(figsize=(16, 9))
fig.suptitle("트랜지스터 구간별 미분 특성 및 발열 분석기", fontsize=16, fontweight='bold', color='#2C3E50')

# 축 설정
ax_3d = fig.add_subplot(1, 2, 1, projection='3d')
ax_f = fig.add_subplot(3, 2, 2)
ax_df = fig.add_subplot(3, 2, 4)
ax_ddf = fig.add_subplot(3, 2, 6)

# 우측 상단 독립 텍스트 창
ax_status_text = fig.add_axes([0.55, 0.90, 0.35, 0.05])
ax_status_text.axis('off')

plt.subplots_adjust(bottom=0.18, hspace=0.35, top=0.88)

애니메이션_진행중 = True
현재_프레임 = 0

# --- 3. 구간별 색상 및 상태 정의 ---
def get_status_and_color(x):
    if x < -1:
        color = '#4A5568'
        heat = 30.0 + abs(df(x))*4
        status = "구간 ① (x < -1) : 신호 감소 및 활성화 준비 (안정 냉각)"
    elif x == -1:
        color = '#2B6CB0'
        heat = 25.0
        status = "지점 ② (x = -1) : [극소점] 신호 최저, 방향 전환 대기"
    elif -1 < x < -2/3:
        color = '#DD6B20'
        heat = 55.0 + df(x)*12
        status = "구간 ③ (-1 < x < -2/3) : 전류 가속화 및 전자 급증 (발열 시작)"
    elif x == -2/3:
        color = '#D69E2E'
        heat = 85.0
        status = "지점 ④ (x = -2/3) : [변곡점] 최대 가속 지점 (피크 발열)"
    elif -2/3 < x < 0:
        color = '#B83280'
        heat = 65.0 - abs(ddf(x))*4
        status = "구간 ⑤ (-2/3 < x < 0) : 신호 지속 증가, 가속도 둔화 (안정화)"
    elif x == 0:
        color = '#319795'
        heat = 50.0
        status = "지점 ⑥ (x = 0) : 변화 특성 재전환 경계 지점"
    else:
        color = '#C53030'
        heat = 90.0 + df(x)*8
        status = "구간 ⑦ (x > 0) : 트랜지스터 100% 완전 활성화 (고부하 연산)"
        
    return color, heat, status

# --- 4. 화면 업데이트 ---
def draw_frame(frame):
    global 현재_프레임
    현재_프레임 = frame
    current_x = 시간_데이터[frame]
    current_f = f(current_x)
    current_df = df(current_x)
    current_ddf = ddf(current_x)
    
    판_색상, 현재_발열, 상태_문구 = get_status_and_color(current_x)
    
    # --- [좌측 3D 구조 및 정보 텍스트 복원] ---
    ax_3d.clear()
    ax_3d.set_title("트랜지스터 소자 내부 상태 (3D 시각화)", fontsize=12, fontweight='bold', color='#4A5568')
    
    grid_x, grid_y = np.meshgrid(np.linspace(-1, 1, 12), np.linspace(-1, 1, 12))
    grid_z = np.ones_like(grid_x) * (current_f * 0.12)
    
    ax_3d.plot_surface(grid_x, grid_y, grid_z, color=판_색상, alpha=0.75, edgecolor='#718096', linewidth=0.5)
    
    입자_수 = min(int(abs(current_f) * 10) + 5, 40)
    입자_x = np.random.uniform(-0.8, 0.8, 입자_수)
    입자_y = np.random.uniform(-0.8, 0.8, 입자_수)
    입자_z = grid_z[0,0] + np.random.normal(0, 0.02 + abs(current_df)*0.02, 입자_수)
    ax_3d.scatter(입자_x, 입자_y, 입자_z, color='#63B3ED', s=35, edgecolor='#2B6CB0', alpha=0.9)
    
    ax_3d.set_zlim(-0.5, 2.5)
    
    # ⭐ [요청 반영] 3D 공간의 네모난 축 테두리, 레이블, 격자 완벽히 되돌리기
    ax_3d.set_xlabel('가로축 (X)')
    ax_3d.set_ylabel('세로축 (Y)')
    ax_3d.set_zlabel('높이축 (Z)')
    ax_3d.grid(True)
    
    # ⭐ [요청 반영] 물음표(??) 깨짐 현상을 해결하기 위한 특수 인코딩 및 맑은 고딕 강제 바인딩
    정보_텍스트 = (
        f"■ 실시간 소자 모니터링 ■\n"
        f"---------------------------\n"
        f"현재 시간 (x)      : {current_x:.2f}\n"
        f"신호 세기 f(x)    : {current_f:.2f}\n"
        f"전류 속도 f'(x)   : {current_df:.2f}\n"
        f"전류 가속도 f''(x) : {current_ddf:.2f}\n"
        f"---------------------------\n"
        f"소자 내부 온도    : {현재_발열:.1f} °C"
    )
    # 한글 지원 폰트 설정을 다시 명시하여 깨짐 방지
    ax_3d.text2D(0.02, 0.75, 정보_텍스트, transform=ax_3d.transAxes, fontsize=10, fontfamily='Malgun Gothic',
                 bbox=dict(facecolor='#F7FAFC', edgecolor='#CBD5E0', boxstyle='round,pad=0.8', alpha=0.9))

    # 상단 독립 창 문구 출력
    ax_status_text.clear()
    ax_status_text.axis('off')
    ax_status_text.text(0.0, 0.3, f"현재 동작 상태: {상태_문구}", fontsize=11, fontweight='bold', 
                        color='white', bbox=dict(facecolor=판_색상, edgecolor='none', boxstyle='round,pad=0.5'))

    # --- [우측 수학 그래프들 - 전체 가이드 점선 삭제] ---
    # 1) f(x) 신호 세기
    ax_f.clear()
    ax_f.plot(시간_데이터[:frame+1], f(시간_데이터[:frame+1]), color='#3182CE', linewidth=2.5, label='신호 세기 f(x)')
    ax_f.scatter(current_x, current_f, color='#2B6CB0', s=60, zorder=5)
    ax_f.set_ylabel("신호 세기", fontsize=9)
    ax_f.set_xlim(-1.5, 0.5)
    ax_f.set_ylim(-0.5, 2.5)
    ax_f.grid(True, linestyle=':', alpha=0.6)
    ax_f.legend(loc='upper left', fontsize=9)
    
    # 2) f'(x) 전류 속도
    ax_df.clear()
    ax_df.plot(시간_데이터[:frame+1], df(시간_데이터[:frame+1]), color='#38A169', linewidth=2.5, label="전류 속도 f'(x)")
    ax_df.scatter(current_x, current_df, color='#276749', s=60, zorder=5)
    ax_df.axhline(0, color='#E53E3E', linestyle='-', linewidth=0.8, alpha=0.7)
    ax_df.set_ylabel("전류 속도", fontsize=9)
    ax_df.set_xlim(-1.5, 0.5)
    ax_df.set_ylim(-15, 5)
    ax_df.grid(True, linestyle=':', alpha=0.6)
    ax_df.legend(loc='upper left', fontsize=9)

    # 3) f''(x) 활성화 가속도
    ax_ddf.clear()
    ax_ddf.plot(시간_데이터[:frame+1], ddf(시간_데이터[:frame+1]), color='#805AD5', linewidth=2.5, label="활성화 가속도 f''(x)")
    ax_ddf.scatter(current_x, current_ddf, color='#553C9A', s=60, zorder=5)
    ax_ddf.axhline(0, color='#E53E3E', linestyle='-', linewidth=0.8, alpha=0.7)
    ax_ddf.set_xlabel("시간 (x)", fontsize=10)
    ax_ddf.set_ylabel("가속도", fontsize=9)
    ax_ddf.set_xlim(-1.5, 0.5)
    ax_ddf.set_ylim(-10, 50)
    ax_ddf.grid(True, linestyle=':', alpha=0.6)
    ax_ddf.legend(loc='upper left', fontsize=9)
    
    fig.canvas.draw_idle()

def update(frame):
    if 애니메이션_진행중:
        슬라이더.set_val(frame)
        draw_frame(frame)

# 컨트롤러 설정
ax_slider = plt.axes([0.15, 0.08, 0.7, 0.03], facecolor='#E2E8F0')
슬라이더 = Slider(ax_slider, '시간 위치 조절', 0, len(시간_데이터)-1, valinit=0, valfmt='%d', color='#4A5568')

ax_btn_pause = plt.axes([0.4, 0.02, 0.08, 0.04])
ax_btn_play = plt.axes([0.5, 0.02, 0.08, 0.04])

버튼_일시정지 = Button(ax_btn_pause, '일시정지', color='#EDF2F7', hovercolor='#E2E8F0')
버튼_재생 = Button(ax_btn_play, '다시재생', color='#EDF2F7', hovercolor='#E2E8F0')

def 언제_슬라이더_움직임(val):
    if not 애니메이션_진행중:
        draw_frame(int(val))

슬라이더.on_changed(언제_슬라이더_움직임)

def 일시정지_액션(event):
    global 애니메이션_진행중
    애니메이션_진행중 = False

def 재생_액션(event):
    global 애니메이션_진행중
    애니메이션_진행중 = True

버튼_일시정지.on_clicked(일시정지_액션)
버튼_재생.on_clicked(재생_액션)

ani = FuncAnimation(fig, update, frames=len(시간_데이터), interval=60, repeat=True)
plt.show()