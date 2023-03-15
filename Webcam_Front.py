import os
from glob import glob
from time import strftime

import cv2
from Emails_Back import create_email, send_email

# opencv 讀取的 channel 順序是 B → G → R

# 获取网络摄像头
# 参数是视频的路径，参数为数字时代表从摄像头获取视频
video = cv2.VideoCapture(0)

# 判断摄像头是否正常开启
if not video.isOpened():
    print("Cannot open camera")
    exit()

first_frame = None
status_list = []
image_number = 0


# 删除images文件夹中的所有图片
def clean_images():
    images = glob("images/*.png")
    for img in images:
        os.remove(img)


while True:
    status = 0
    # 读取视频的下一帧，check返回值为是否成功获取视频帧
    # frame返回值为返回的视频帧
    check, frame = video.read()
    # 给视频加上时间戳
    current_time = strftime("%Y-%m-%d %H:%M:%S %A")
    cv2.putText(img=frame, text=current_time, org=(50, 50),
                fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=2,
                color=(255, 0, 0), thickness=2, lineType=cv2.LINE_AA)

    # 如果读取错误，给出提示
    if not check:
        print("Cannot receive frame")
        break
    # 如果读取成功，图像转灰阶，三维变二维，减少图像矩阵复杂度
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # 用高斯滤波函数，将灰阶图像平滑模糊化，减少高斯噪音
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (15, 15), 0)

    # 保证first_frame的值是第一帧(转灰阶后的值)不变
    if first_frame is None:
        first_frame = gray_frame_gau

    # 比较当前帧与第一帧，把两幅图的差的绝对值输出到另一幅图上面来
    comp_frame = cv2.absdiff(first_frame, gray_frame_gau)

    # 使用二值转化函数，将灰阶比较图像中的>=30的值都赋为255白色,使对比更明显
    thresh_frame = cv2.threshold(comp_frame, 25, 255, cv2.THRESH_BINARY)[1]
    # 使用膨胀函数，将二值化后的灰阶图像进行轮廓加强处理
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)

    # 显示带矩形轮廓的原图像
    cv2.imshow('detect video', dil_frame)

    # 检测图像（即白色区域）周围的轮廓
    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        # 如果某个白色区域的轮廓大小小于1000，则判断为不是检测对象，跳出for循环继续判断
        if cv2.contourArea(contour) < 5000:
            continue
        # >=1000说明是检测对象，确定矩形参数
        x, y, w, h = cv2.boundingRect(contour)
        # 在原图像周围画出该绿色矩形
        rectangle = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)

        # 检测到移动物体时将status置为1
        if rectangle.any():
            status = 1
            # 将当前帧存为图片
            image_number += 1
            cv2.imwrite(f"images/{image_number}.png", frame)

            # 将所有截取的图片名称存入list
            all_images = glob("images/*.png")

            # 获取最中间的图像
            middle = int(len(all_images) / 2)
            middle_image = all_images[middle]

    # 获取当前帧下状态列表最后俩元素的值
    status_list.append(status)
    status_list = status_list[-2:]
    print(status_list)

    # 如果最后俩元素为[1, 0]则说明物体刚离开检测画面，此时再发邮件
    if status_list[0] == 1 and status_list[1] == 0:
        message = create_email(middle_image).as_string()
        send_email(message)
        # 邮件发送后清除images文件夹
        clean_images()

    # 显示带矩形轮廓的原图像
    cv2.imshow('detect video', frame)

    # 使用 cv2.waitKey() 來等待使用者按鍵
    key = cv2.waitKey(1)
    # 每一毫秒更新一次，直到按下ESC结束
    if key == 27:
        break

# 完成后释放资源
video.release()
# 关闭所有窗口(注意是小写的ll，不是LL)
cv2.destroyAllWindows()
