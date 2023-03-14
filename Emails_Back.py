import email
import smtplib
import time
import cv2

# opencv 讀取的 channel 順序是 B → G → R

# 获取网络摄像头
# 参数是视频的路径，参数为数字时代表从摄像头获取视频
video = cv2.VideoCapture(0)

# 判断摄像头是否正常开启
if not video.isOpened():
    print("Cannot open camera")
    exit()

while True:
    # 读取视频的下一帧，check返回值为是否成功获取视频帧
    # frame返回值为返回的视频帧
    check, frame = video.read()
    # 如果读取错误，给出提示
    if not check:
        print("Cannot receive frame")
        break
    # 如果读取成功，显示读该帧的画面窗口，窗口名为my video
    cv2.imshow('my video', frame)
    # 會使用 cv2.waitKey() 來等待使用者按鍵
    # 每一毫秒更新一次，直到按下‘q’结束, 参数为0时表示视频暂停
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

# 完成后释放资源
video.release()
# 关闭所有窗口
video.destroyALLWindows()
































































