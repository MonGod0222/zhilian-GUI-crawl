from tkinter import *
from tkinter import ttk
import os
import tkinter
from PIL import Image, ImageTk


root = Tk()

#背景
canvas = tkinter.Canvas(root,
                        width=800,  # 指定Canvas组件的宽度
                        height=460,  # 指定Canvas组件的高度
                        bg='white')  # 指定Canvas组件的背景色
image = Image.open("img.jpg")
im = ImageTk.PhotoImage(image)

canvas.create_image(300, 350, image=im)  # 使用create_image将图片添加到Canvas组件中




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
f5_5 = Frame(root)
f5_5.pack()
f6 = Frame(root)
f6.pack()
f7 = Frame(root)
f7.pack()

label_l1 = Label(f1, text='关键字(必选)',background='pink')
label_l1.pack(side=LEFT)
# 关键字输入框
key = StringVar()
entry_e1 = Entry(f1, textvariable=key)
entry_e1.pack(side=RIGHT)

label_l2 = Label(f2, text='***页  数*** ',background='pink')
label_l2.pack(side=LEFT)
# 页数输入框
page = StringVar()
entry_e2 = Entry(f2, textvariable=page)
entry_e2.pack(side=RIGHT)

# 数据库复选框
label_c = Label(f3, text='选择数据库',background='pink')
label_c.pack()
mysql = IntVar()
check_one = Checkbutton(f3, text='MYSQL', variable=mysql)
check_one.pack()
mongo = IntVar()
check_two = Checkbutton(f3, text='MONGO', variable=mongo)
check_two.pack()


label_u = Label(f4, text='用户名',background='pink')
label_u.pack(side=LEFT)
# 用户名输入框
user = StringVar()
entry_u = Entry(f4, textvariable=user)
entry_u.pack(side=RIGHT)
label_p = Label(f5, text='密  码',background='pink')
label_p.pack(side=LEFT)
# 密码输入框
password = StringVar()
entry_p = Entry(f5, textvariable=password)
entry_p['show']='*'
entry_p.pack(side=RIGHT)

#下拉列表(地区)
area={
    '全国': 489,
    '北京': 530,
    '上海': 538,
    '深圳': 765,
    '广州': 763,
    '天津': 531,
    '成都': 801,
    '杭州': 653,
    '武汉': 736,
    '大连': 600,
    '南京': 635,
    '苏州': 639,
    '西安': 854,
}

label_ttk = Label(f5_5, text='地 区',background='pink')
label_ttk.pack(side=LEFT)

ttk_v='全国'
def functtk(event):
    global ttk_v
    ttk_v=cmb.get()
    print(ttk_v)

cmb=ttk.Combobox(f5_5)
cmb.pack(side=RIGHT)
cmb['value']=('全国','北京','上海','深圳','广州','天津','成都','杭州','武汉','大连','南京','苏州','西安')
cmb.current(0)
cmb.bind("<<ComboboxSelected>>",functtk)



#rbutton_one=Radiobutton(f5_5,text=area['全国'],variable=bintvar,vaule=1,command=bo)




def run():
    if key.get():
        now_path = os.path.dirname(__file__)
        params = '-a input_keyword={} '.format(
            key.get())
        if page.get():
            params = params+'-a input_page={} '.format(page.get())
        else:
            params = params+'-a input_page=1 '
        if mysql.get() == 1 and user.get() and password.get():
            params = params + '-s set_mysql=1 -s set_user={} -s set_password={} '.format(
                user.get(), password.get())
        else:
            params = params + '-s set_mysql=0 -s set_user={} -s set_password={} '.format(
                '','')
        if mongo.get() == 1:
            params = params + \
                '-s set_mongo=1 '
        else:
            params = params + '-s set_mongo=0 '

        params=params + '-a input_area={} '.format(area[ttk_v])

        os.system('cd {}'.format(now_path)+r'\recruit'+' && ' +
              'scrapy crawl zhilian {}'.format(params)+'-s COLLECTION={}'.format('求职信息'))


button = Button(f6, text='run', command=run,background='orange')
button.pack()

text = '''
页数默认为1页，每页有90条数据，最大限制在10页，避免恶意使用
只有选择MYSQL数据库才需要输入用户名和密码，存储在本地
'''
specification = Label(f7, text=text,background='yellow')
specification.pack()

unit=5.5

canvas.create_window(400,unit*10,
                   window=f1)
canvas.create_window(400,unit*20,
                   window=f2)
canvas.create_window(400,unit*30,
                   window=f3)
canvas.create_window(400,unit*40,
                   window=f4)
canvas.create_window(400,unit*50,
                   window=f5)
canvas.create_window(400,unit*60,
                   window=f5_5)
canvas.create_window(400,unit*70,
                   window=f6)
canvas.create_window(400,unit*80,
                   window=f7)




canvas.pack()  # 将Canvas添加到主窗口

root.mainloop()
