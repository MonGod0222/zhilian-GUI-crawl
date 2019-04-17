from tkinter import *
from tkinter import ttk
import os
import tkinter
from PIL import Image, ImageTk

root = Tk()

# 背景
canvas = tkinter.Canvas(root,
                        width=400,  # 指定Canvas组件的宽度
                        height=500,  # 指定Canvas组件的高度
                        bg='white')  # 指定Canvas组件的背景色
image = Image.open("MAILimg.jpg")
im = ImageTk.PhotoImage(image)

# Frame框架
f1 = Frame(root)
f1.pack()
f2 = Frame(root)
f2.pack()
f3 = Frame(root)
f3.pack()
f4 = Frame(root)
f4.pack()
f5 = Frame(root)
f5.pack()
f6 = Frame(root)
f6.pack()
f7 = Frame(root)
f7.pack()
f8 = Frame(root)
f8.pack()
f9 = Frame(root)
f9.pack()

# 账号输入框
label_user = Label(f1, text='邮箱账号', background='pink')
label_user.pack(side=LEFT)
user = StringVar()
entry_user = Entry(f1, textvariable=user)
entry_user.pack(side=RIGHT)

# 密码输入框
label_password = Label(f2, text='邮箱密码', background='pink')
label_password.pack(side=LEFT)
password = StringVar()
entry_password = Entry(f2, textvariable=password)
entry_password['show']='*'
entry_password.pack(side=RIGHT)

# 收件邮箱输入框
label_password = Label(f3, text='收件邮箱', background='pink')
label_password.pack(side=LEFT)
send_mail = StringVar()
entry_password = Entry(f3, textvariable=send_mail)
entry_password.pack(side=RIGHT)

# 主题输入框
label_password = Label(f4, text='主  题', background='pink')
label_password.pack(side=LEFT)
theme = StringVar()
entry_password = Entry(f4, textvariable=theme)
entry_password.pack(side=RIGHT)

# 数据库单选框
label_db = Label(f5, text='选择数据库', background='pink')
label_db.pack()


def sel():
    pass


which_db = IntVar()
radio_button_one = Radiobutton(f5, text="MYSQL", variable=which_db, value=1)
radio_button_two = Radiobutton(f5, text="MONGO", variable=which_db, value=2)
radio_button_one.pack()
radio_button_two.pack()

label_u = Label(f6, text='用户名', background='pink')
label_u.pack(side=LEFT)
# 用户名输入框
mysql_user = StringVar()
entry_u = Entry(f6, textvariable=mysql_user)
entry_u.pack(side=RIGHT)
label_p = Label(f7, text='密  码', background='pink')
label_p.pack(side=LEFT)
# 密码输入框
mysql_password = StringVar()
entry_p = Entry(f7, textvariable=mysql_password)
entry_p['show']='*'
entry_p.pack(side=RIGHT)

text = '''
默认取前三条数据
只有选择MYSQL数据库才需要输入用户名和密码，本地查询
'''
specification = Label(f9, text=text, background='yellow')
specification.pack()


# run按钮
def run():
    now_path = os.path.dirname(__file__)
    do = 'cd {} && '.format(now_path)
    do = do + 'python sendmail.py '
    params = '{} {} {} {} '.format(user.get(), password.get(), send_mail.get(), theme.get())

    if which_db.get() == 1:  # mysql
        params = params + '{} {} {}'.format('mysql', mysql_user.get(), mysql_password.get())
    if which_db.get() == 2:  # mongo
        params = params + '{} {} {}'.format('mongo', '空', '空')

    do = do + params
    print(do)


button = Button(f8, text='run', command=run, background='orange')
button.pack()

canvas.create_image(400, 285, image=im)  # 使用create_image将图片添加到Canvas组件中

k_unit_b = 5
g_unit = 200

canvas.create_window(g_unit, k_unit_b * 10,
                     window=f1)
canvas.create_window(g_unit, k_unit_b * 20,
                     window=f2)
canvas.create_window(g_unit, k_unit_b * 30,
                     window=f3)
canvas.create_window(g_unit, k_unit_b * 40,
                     window=f4)
canvas.create_window(g_unit, k_unit_b * 52,
                     window=f5)
canvas.create_window(g_unit, k_unit_b * 66,
                     window=f6)
canvas.create_window(g_unit, k_unit_b * 72,
                     window=f7)
canvas.create_window(g_unit, k_unit_b * 82,
                     window=f8)
canvas.create_window(g_unit, k_unit_b * 95,
                     window=f9)

canvas.pack()  # 将Canvas添加到主窗口

root.mainloop()
