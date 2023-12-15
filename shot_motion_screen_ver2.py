import cv2  # pip install opencv-python
import mediapipe as mp  # pip install mediapipe
from tkinter import *
from tkinter.font import Font
from PIL import Image, ImageTk  # pip install pillow
import math # atan2

# 1번 로그인 창
def get_text():
    global user_id, user_num
    if entry_id.get() and entry_num.get():
        user_id = entry_id.get()
        user_num = entry_num.get()
        root.destroy()


root = Tk()
root.title("login")
root.geometry("550x500+400+200")
root.resizable(True, True)

user_id = ""
user_num = ""
user_point = 0

title_font = Font(family="Yeongdeok_Sea.ttf", size=30, weight="bold")
lbl_font = Font(family="Yeongdeok_Sea.ttf", size=15)
txt_font = Font(family="Yeongdeok_Sea.ttf", size=15)
btn_font = Font(family="Yeongdeok_Sea.ttf", size=15, weight="bold")

frame = Frame(root, relief="solid", bd=2)
frame.place(relx=0.2, rely=0.1, width=330, height=400)

lbl_title = Label(frame, text="Login", font=title_font, anchor="w",
                width=50, padx=20, pady=20)
lbl_title.pack()

lbl = Label(frame, text="이름", font=lbl_font, anchor="w",
            width=50, padx=15, pady=10)
lbl.pack()
entry_id = Entry(frame, font=txt_font, bd=1, relief="solid", width=26)
entry_id.pack()

lbl2 = Label(frame, text="학번", font=lbl_font, anchor="w",
            width=50, padx=15, pady=10)
lbl2.pack()
entry_num = Entry(frame, font=txt_font, bd=1, relief="solid", width=26)
entry_num.pack()

lbl_space = Label(frame, text="", pady=15)
lbl_space.pack()

btn = Button(frame, text="Submit", command=get_text, font=btn_font, width=12,
            relief="solid")
btn.pack()

root.mainloop()


# 2번 손 인식 창
def func_opencv():
    global w, h, task_id, chk_time, point1, point2, point3
    ret, frame = cap.read()
    if ret:
        chk_time += 10
        cvtColor = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pose_results = pose.process(cvtColor)
        
        if pose_results.pose_landmarks:
            mp_drawing.draw_landmarks(
                frame,
                pose_results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2)
            )
        
        frame = cv2.resize(frame, (w, h))
        frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
        if pose_results.pose_landmarks:
            cv2.putText(frame, f"time:{max_time - chk_time}", (5, 35),font, 1, (0,255,0), 2)
            cv2.putText(frame, f"Hand:{'Right' if hand_side else 'Left'}", (w * 11 // 15, 35), font, 1, (0,255,0), 2)
            if hand_side:
                point1.append(abs(round(pose_results.pose_landmarks.landmark[14].z, 2) - round(pose_results.pose_landmarks.landmark[16].z, 2)))
                point2.append(pose_results.pose_landmarks.landmark[12].y)
                point3 = (pose_results.pose_landmarks.landmark[16], pose_results.pose_landmarks.landmark[20]) 
                # point_14, point_16 = round(pose_results.pose_landmarks.landmark[14].z, 2), round(pose_results.pose_landmarks.landmark[16].z, 2)
                # cv2.putText(frame, f"Right, 14:{point_14}, 16:{point_16}, dist:{round(abs(point_14 - point_16), 2)}", (5, 35),font,1,(0,255,0),2)
            else :
                point1.append(abs(round(pose_results.pose_landmarks.landmark[13].z, 2) - round(pose_results.pose_landmarks.landmark[15].z, 2)))
                point2.append(pose_results.pose_landmarks.landmark[11].y)
                point3 = (pose_results.pose_landmarks.landmark[15], pose_results.pose_landmarks.landmark[19])
                # point_13, point_15 = round(pose_results.pose_landmarks.landmark[13].z, 2), round(pose_results.pose_landmarks.landmark[15].z, 2)
                # cv2.putText(frame, f"'Left, 13:{point_13}, 15:{point_15}, dist:{round(abs(point_13 - point_15), 2)}", (5, 35),font,1,(0,255,0),2)
        # else :
            # cv2.putText(frame, f"0, 0, dist:0", (5, 35),font,1,(0,255,0),2)

        img = Image.fromarray(frame)
        img = ImageTk.PhotoImage(image=img)
        lbl_cv.config(image=img)
        lbl_cv.image = img
    
    if chk_time < max_time:
        task_id = main_window.after(10, func_opencv)
    else :
        main_window.after_cancel(task_id)
        lbl_cv.config(image=init_img)
        result_point()
        

def close_window():
    if task_id:
        main_window.after_cancel(task_id)
    hands.close()
    pose.close()
    cap.release()
    
    main_window.destroy()

def set_hand(side):
    global hand_side
    hand_side = side

def start_chk():
    global point1, point2, point3
    point1 = [] # z축 확인하여 벌어진 정도 확인
    point2 = [] # 어깨 높이 변화
    point3 = tuple() # 손 변화량 (각도)
    func_opencv()

def result_point():
    # 100 - (z축 평균값(사용자 지정 값) - 0.14(기준값))
    user_point = round(100 - (sum(point1) / len(point1) - 0.14), 2)
    with open("record.txt", "a", encoding="UTF-8") as f:
        f.write(f"이름:{user_id},학번:{user_num},{user_point}\n")
    
    print(len(point2), max(point2) - min(point2))
    at2 = math.atan2(point3[1].y - point3[0].y, point3[1].x - point3[0].x)
    print(f"atan2:{at2}, atan2(degrees){math.degrees(at2)}")

main_window = Tk()
main_window.title("main")
main_window.geometry("1000x1000+400+200")
main_window.resizable(True, True)

task_id = None
mp_drawing_styles = mp.solutions.drawing_styles
hand_side = True
chk_time = 0
max_time = 2000

point1 = [] # z축 확인하여 벌어진 정도 확인
point2 = [] # 어깨 높이 변화
point3 = tuple() # 손 변화량 (각도)

font=cv2.FONT_HERSHEY_SIMPLEX
w, h = 700, 560
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

init_img = PhotoImage(file="dksh.png")

lbl_cv = Label(main_window, width=w, height=h, image=init_img)
lbl_cv.grid(row=0,column=0, columnspan=2)

btn_start = Button(main_window, text="Start", command=start_chk)
btn_start.grid(row=1, column=0, columnspan=2)

btn_right_hand = Button(main_window, text="Right", command=lambda : set_hand(True))
btn_right_hand.grid(row=2, column=0)

btn_left_hand = Button(main_window, text="Left", command=lambda : set_hand(False))
btn_left_hand.grid(row=2, column=1)

btn_show_res = Button(main_window, text="Result", command=close_window)
btn_show_res.grid(row=3, column=0, columnspan=2)

cap = cv2.VideoCapture(0)

main_window.protocol("WM_DELETE_WINDOW", close_window)
main_window.mainloop()

# 3. 결과창
result_window = Tk()
result_window.title("result")
result_window.geometry("500x500+400+200")
result_window.resizable(True, True)

with open("record.txt", "r", encoding="UTF-8") as f:
    datas = f.readlines()
    data_list = []
    for data in datas:
        data = data.strip().split(",")
        data_list.append((data[0], data[1], float(data[2])))

    data_list.sort(key=lambda x: x[2], reverse=True)

    for data in data_list:
        lbl_res = Label(result_window, text=f"이름:{data[0]}, 학번:{data[1]}, 점수: {data[2]}", font=lbl_font)
        lbl_res.pack()

result_window.mainloop()
