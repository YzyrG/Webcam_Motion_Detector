from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.utils import formataddr
import smtplib
import os
import ssl


def create_email(image):
    # related类型将图片以内嵌资源的方式存储在邮件中
    msg = MIMEMultipart('related')
    msg["From"] = formataddr(("My Motion Detector", "15683966878@163.com"))
    msg['To'] = formataddr(("ZYR", "245632738@qq.com"))
    msg['Subject'] = "检测到有物体出现！"

    # 邮件正文
    content = MIMEText('<html><head><style>#string{color:red;text-align:center;font-size:10px;}</style>'
                       '<div id="string">检测到新物体：<div></head><body><img src="cid:image1" '
                       'alt="image1"></body></html>', 'html', 'utf-8')
    msg.attach(content)

    # 添加图片附件
    with open(image, 'rb') as file:
        msg_image = MIMEImage(file.read(), _subtype=False)

    # 此处id用于上面html获取图片
    msg_image.add_header("Content-ID", 'image1')
    msg.attach(msg_image)

    return msg


def send_email(message):
    # 使用163邮箱作为SMTP服务器
    host = "smtp.163.com"
    port = 465

    # 发件人
    sender = "15683966878@163.com"
    password = os.getenv('PASSWORD')

    # 收件人
    receiver = "2456327328@qq.com"

    # 返回一个新的带有安全默认设置的上下文
    context = ssl.create_default_context()

    # 使用安全加密的SSL协议连接到SMTP服务器
    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(sender, password)
        server.sendmail(sender, receiver, message)


if __name__ == "__main__":
    msg = create_email("images/test.jpg").as_string()
    send_email(msg)
