# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 18:12:14 2020

@author: acer
"""

import pymssql
from tkinter import ttk #使用树形列表控件treeview
import tkinter as tk
import tkinter.messagebox as messagebox # 弹窗
import datetime

# 连接数据库
def conn():
    connect = pymssql.connect('LAPTOP-TDMA9HB9', 'db123', '1234', 'db_commodity',charset='utf8') #服务器名,账户,密码,数据库名
    if connect:
        print("连接成功!")
    return connect
 

class AdminPage:
    def __init__(self,parent_window):
        parent_window.destroy() # 销毁上一个界面
        self.window = tk.Tk()  # 初始框的声明
        self.window.title('商品进存管理登陆界面')
        self.window.geometry('405x300+450+120')
        BJfile=r'D:/商品进销存管理系统/GNKMX.gif'
        #将图片设置为背景
        BJpic=tk.PhotoImage(file=BJfile)
        BJlabel=tk.Label(image=BJpic)
        BJlabel.pack()#载入图片做背景
        BJlabel.place(x=0,y=0)
        
        # 创建提示信息
        tk.Label(self.window, text='用户名: ').place(x=80, y= 140)
        tk.Label(self.window, text='密码: ').place(x=80, y= 180)
        
        #用户名和密码输入框
        u_name=tk.StringVar()
        self.entry_usr_name=tk.Entry(self.window,textvariable=u_name)
        self.entry_usr_name.place(x=160,y=140)
        p_pwd=tk.StringVar()
        self.entry_usr_pwd=tk.Entry(self.window, show='*',textvariable=p_pwd)
        self.entry_usr_pwd.place(x=160,y=180)
        # 登陆和返回首页得按钮
        btn_login = tk.Button(self.window, text='登录',  width=10, command=self.usr_log_in)
        btn_login.place(x=120, y=230)
        btn_logquit = tk.Button(self.window,text='退出',width=10,command=self.usr_sign_quit)
        btn_logquit.place(x=240,y=230)
        self.window.mainloop()

	# 登陆的函数
    def usr_log_in(self):
        #输入框获取用户名密码
        usr_name=self.entry_usr_name.get()
        usr_pwd=self.entry_usr_pwd.get()
        #从本地字典获取用户信息，如果没有则新建本地数据库
        cn = conn()
        cur=cn.cursor()
        cur.execute("select d.用户编号,密码,管理权限 from 登录表 as d LEFT OUTER JOIN 权限表 as q on d.用户编号=q.用户编号 where d.用户编号=\'{}\'".format(usr_name))
        user=cur.fetchall()
        print(user)
        name=user[0][0]
        pwd=user[0][1]
        quanxian=user[0][2]
        cn.commit()
        cn.close()
        print("正在登陆管理员管理界面.......")
        #判断用户名和密码是否匹配
        if usr_name == name:
            if usr_pwd == pwd:
                if quanxian == 1:
                    All_admin(self.window)   # 进入管理员子菜单操作界面
                else:
                    all_admin(self.window)
            else:
                tk.messagebox.showinfo('警告！', '用户名或密码不正确！')
        #用户名密码不能为空
        elif usr_name=='' or usr_pwd=='' :
            tk.messagebox.showerror(message='用户名或密码为空')

    #退出的函数
    def usr_sign_quit(self):
        self.window.destroy()


# 管理员子菜单操作界面
class All_admin:
    def __init__(self, parent_window):
        parent_window.destroy() # 自定销毁上一个界面
        self.window = tk.Tk()  # 初始框的声明
        self.window.title('管理员操作界面')
        self.window.geometry('376x550+450+75')
        BJfile=r'D:/商品进销存管理系统/douyin.gif'
        #将图片设置为背景
        BJpic=tk.PhotoImage(file=BJfile)
        BJlabel=tk.Label(image=BJpic)
        BJlabel.pack()#载入图片做背景
        BJlabel.place(x=0,y=0)
        label = tk.Label(self.window, text="欢迎光临管理员系统\n请选择需要进行的操作", font=("Verdana", 22))
        label.pack(pady=75)  # pady=100 界面的长度   
        
        tk.Button(self.window, text="商品销售管理", font=20, width=45, height=2, command=lambda: AdminManage(self.window),
			fg='white', bg='gray', activebackground='black', activeforeground='white').pack()
        tk.Button(self.window, text="商品库存管理", font=20, width=45,height=2, command=lambda:Commodity_inventory(self.window),
			fg='white', bg='gray', activebackground='black', activeforeground='white').pack()
        tk.Button(self.window, text="原材料库存管理", font=20, width=45, height=2, command=lambda:Material_inventory(self.window),
			fg='white', bg='gray', activebackground='black', activeforeground='white').pack()
        tk.Button(self.window, text="仓库管理", font=20, width=45, height=2, command=lambda:WarehouseManage(self.window),
			fg='white', bg='gray', activebackground='black', activeforeground='white').pack()
        tk.Button(self.window, text="进货管理", font=20, width=45, height=2, command=lambda:ProcurementManage(self.window),
			fg='white', bg='gray', activebackground='black', activeforeground='white').pack()
        tk.Button(self.window, text="供应商资料管理", font=20, width=45, height=2, command=lambda:DataManage(self.window),
			fg='white', bg='gray', activebackground='black', activeforeground='white').pack()
        tk.Button(self.window, text="系统管理", font=20, width=45, height=2, command=lambda:AuthorityManage(self.window),
			fg='white', bg='gray', activebackground='black', activeforeground='white').pack()

        self.window.protocol("WM_DELETE_WINDOW", self.back)  # 捕捉右上角关闭点击
        self.window.mainloop()  # 进入消息循环

    def back(self):
        AdminPage(self.window) # 显示主窗口 销毁本窗口

# 普通员工子菜单操作界面
class all_admin:
    def __init__(self, parent_window):
        parent_window.destroy() # 自定销毁上一个界面
        self.window = tk.Tk()  # 初始框的声明
        self.window.title('普通员工操作界面')
        self.window.geometry('376x420+450+75')
        BJfile=r'D:/商品进销存管理系统/douyin.gif'
        #将图片设置为背景
        BJpic=tk.PhotoImage(file=BJfile)
        BJlabel=tk.Label(image=BJpic)
        BJlabel.pack()#载入图片做背景
        BJlabel.place(x=0,y=0)
        label = tk.Label(self.window, text="欢迎光临普通员工系统\n请选择需要进行的操作", font=("Verdana", 20))
        label.pack(pady=80)  # pady=100 界面的长度   
        
        tk.Button(self.window, text="购买界面", font=20, width=45,height=3, command=lambda:BuyManage(self.window),
			fg='white', bg='gray', activebackground='black', activeforeground='white').pack()
        tk.Button(self.window, text="收付款信息管理", font=20, width=45, height=3, command=lambda: BuyminManage(self.window),
			fg='white', bg='gray', activebackground='black', activeforeground='white').pack()
        tk.Button(self.window, text="顾客信息管理", font=20, width=45,height=3, command=lambda:Dataclient(self.window),
			fg='white', bg='gray', activebackground='black', activeforeground='white').pack()

        self.window.protocol("WM_DELETE_WINDOW", self.back)  # 捕捉右上角关闭点击
        self.window.mainloop()  # 进入消息循环
        
    def back(self):
        AdminPage(self.window) # 显示主窗口 销毁本窗口

#建立商品销售管理类
class AdminManage:
    def __init__(self,parent_window):
        parent_window.destroy() # 自定销毁上一个界面
        self.window = tk.Tk()  # 初始框的声明
        self.window.title('商品销售界面')
        self.window.geometry("760x637+250+15")	# 初始窗口在屏幕中的位置
        self.frame_left_top = tk.Frame(width=400, height=230)	# 指定框架，在窗口上可以显示，这里指定四个框架	
        self.frame_right_top = tk.Frame(width=250, height=250)
        self.frame_center = tk.Frame(width=740, height=270)
        self.frame_bottom = tk.Frame(width=650, height=70)
        
        # 定义下方中心列表区域
        self.columns = ("商品名称", "商品价格","销售数量","用户编号","顾客编号","销售时间")
        self.tree = ttk.Treeview(self.frame_center, show="headings", height=16, columns=self.columns)
        # 添加竖直滚动条
        self.vbar = ttk.Scrollbar(self.frame_center, orient="vertical", command=self.tree.yview)
		# 定义树形结构与滚动条
        self.tree.configure(yscrollcommand=self.vbar.set)

		# 定义id1为修改id时的暂存变量，这个是为了更新信息而设计的
        self.id1 = 0
 
		# 表格的标题
        self.tree.column("商品名称", width=130, anchor='center')
        self.tree.column("商品价格", width=100, anchor='center')
        self.tree.column("销售数量", width=100, anchor='center')
        self.tree.column("用户编号", width=130, anchor='center')
        self.tree.column("顾客编号", width=130, anchor='center')
        self.tree.column("销售时间", width=130, anchor='center')
 
		# grid方法将tree和vbar进行布局
        self.tree.grid(row=0, column=0, sticky="NSEW")
        self.vbar.grid(row=0, column=1, sticky="NS")
	
		# 定义几个数组，为中间的那个大表格做一些准备
        self.name = []
        self.price = []
        self.number = []
        self.yno = []
        self.gno = []
        self.saletime = []
        
        #连接数据库
        db = conn()
        #获取游标、数据
        cur = db.cursor()
        sql = "SELECT * FROM 商品销售表 "
        try:
			# 执行SQL语句
            cur.execute(sql)
			# 获取所有记录列表
            results = cur.fetchall()
            for row in results:
                self.name.append(row[0].encode('latin-1').decode('gbk'))
                self.price.append(row[1])
                self.number.append(row[2])
                self.yno.append(row[3])
                self.gno.append(row[4])
                self.saletime.append(row[5])
        except:
            messagebox.showinfo('警告！', '数据库连接失败！')
        db.close()# 关闭数据库连接
        
        print("test***********************")
        for i in range(len(self.name)):  # 写入数据
            self.tree.insert('', i, values=(self.name[i], self.price[i], self.number[i],self.yno[i],self.gno[i],self.saletime[i]))

        for col in self.columns:  # 绑定函数，使表头可排序(这里的command=lambda _col=col还不是太懂)
            self.tree.heading(col, text=col, command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))
 
		# 定义顶部区域
		# 定义左上方区域
        self.top_title = tk.Label(self.frame_left_top, text="商品信息:", font=('Verdana', 15))
        self.top_title.grid(row=0, column=0, columnspan=2, sticky="NSEW", padx=40, pady=5)   # NSEW表示允许组件向4个方向都可以拉伸

		# 定义下方区域
        self.chaxun = tk.StringVar()
        self.right_bottom_gender_entry = tk.Entry(self.frame_bottom, textvariable=self.chaxun, font=('Verdana', 15))
        self.right_bottom_button = ttk.Button(self.frame_bottom, text='商品名称查询', width=18, command=self.put_data)
        self.right_bottom_button.grid(row=0, column=0, padx=18, pady=18)  # 位置设置
        self.right_bottom_gender_entry.grid(row=0, column=1)
 
        self.left_top_frame = tk.Frame(self.frame_left_top)
        self.var_name = tk.StringVar()  
        self.var_price = tk.StringVar()  
        self.var_number = tk.StringVar()  
        self.var_yno = tk.StringVar()  
        self.var_gno = tk.StringVar()
        self.var_saletime = tk.StringVar()
		# 商品名称
        self.right_top_id_label = tk.Label(self.frame_left_top, text="商品名称: ", font=('Verdana', 11))
        self.right_top_id_entry = tk.Entry(self.frame_left_top, textvariable=self.var_name, font=('Verdana', 15))
        self.right_top_id_label.grid(row=1, column=0)
        self.right_top_id_entry.grid(row=1, column=1)
		# 商品价格
        self.right_top_price_label = tk.Label(self.frame_left_top, text="商品价格：", font=('Verdana', 11))
        self.right_top_price_entry = tk.Entry(self.frame_left_top, textvariable=self.var_price, font=('Verdana', 15))
        self.right_top_price_label.grid(row=2, column=0)  # 位置设置
        self.right_top_price_entry.grid(row=2, column=1)
		# 销售数量
        self.right_top_number_label = tk.Label(self.frame_left_top, text="销售数量：", font=('Verdana', 11))
        self.right_top_number_entry = tk.Entry(self.frame_left_top, textvariable=self.var_number,font=('Verdana', 15))
        self.right_top_number_label.grid(row=3, column=0)  # 位置设置
        self.right_top_number_entry.grid(row=3, column=1)
		# 用户编号
        self.right_top_yno_label = tk.Label(self.frame_left_top, text="用户编号：", font=('Verdana', 11))
        self.right_top_yno_entry = tk.Entry(self.frame_left_top, textvariable=self.var_yno, font=('Verdana', 15))
        self.right_top_yno_label.grid(row=4, column=0)  # 位置设置
        self.right_top_yno_entry.grid(row=4, column=1)
        # 顾客编号
        self.right_top_gno_label = tk.Label(self.frame_left_top, text="顾客编号：", font=('Verdana', 11))
        self.right_top_gno_entry = tk.Entry(self.frame_left_top, textvariable=self.var_gno, font=('Verdana', 15))
        self.right_top_gno_label.grid(row=5, column=0)  # 位置设置
        self.right_top_gno_entry.grid(row=5, column=1)
        # 销售时间
        self.right_top_saletime_label = tk.Label(self.frame_left_top, text="销售时间：", font=('Verdana', 11))
        self.right_top_saletime_entry = tk.Entry(self.frame_left_top, textvariable=self.var_saletime, font=('Verdana', 15))
        self.right_top_saletime_label.grid(row=6, column=0)  # 位置设置
        self.right_top_saletime_entry.grid(row=6, column=1)
 
		# 定义右上方区域
        self.right_top_title = tk.Label(self.frame_right_top, text="操作：", font=('Verdana', 17))
        self.tree.bind('<Button-1>', self.click)  # 左键获取位置(tree.bind可以绑定一系列的事件，可以搜索ttk相关参数查看)
        self.right_top_button1 = ttk.Button(self.frame_right_top, text='新建商品信息', width=20, command=self.new_row)
        self.right_top_button2 = ttk.Button(self.frame_right_top, text='更新选中商品信息', width=20,command=self.updata_row)
        self.right_top_button3 = ttk.Button(self.frame_right_top, text='删除选中商品信息', width=20,command=self.del_row)
        self.right_top_button4 = ttk.Button(self.frame_right_top, text='提交数据', width=20,command=self.putin)

		# 右上角按钮的位置设置
        self.right_top_title.grid(row=1, column=0, pady=10)
        self.right_top_button1.grid(row=2, column=0, padx=20, pady=10)
        self.right_top_button2.grid(row=3, column=0, padx=20, pady=10)
        self.right_top_button3.grid(row=4, column=0, padx=20, pady=10)
        self.right_top_button4.grid(row=5, column=0, padx=20, pady=10)
 
		# 整体区域定位，利用了Frame和grid进行布局
        self.frame_left_top.grid(row=0, column=0, padx=2, pady=5)
        self.frame_right_top.grid(row=0, column=1, padx=30, pady=30)
        self.frame_center.grid(row=1, column=0, columnspan=2, padx=3, pady=5)
        self.frame_bottom.grid(row=2, column=0, columnspan=2)
 
		# 设置固定组件，(0)就是将组件进行了固定
        self.frame_left_top.grid_propagate(0)
        self.frame_right_top.grid_propagate(0)
        self.frame_center.grid_propagate(0)
        self.frame_bottom.grid_propagate(0)
 
        self.frame_left_top.tkraise() # 开始显示主菜单，tkraise()提高z轴的顺序（不太懂）
        self.frame_right_top.tkraise() # 开始显示主菜单
        self.frame_center.tkraise() # 开始显示主菜单
        self.frame_bottom.tkraise() # 开始显示主菜单
 
        self.window.protocol("WM_DELETE_WINDOW", self.back)  # 捕捉右上角关闭点击，执行back方法
        self.window.mainloop()  # 进入消息循环

	# 将查到的信息放到中间的表格中
    def put_data(self):
        self.delButton()	# 先将表格内的内容全部清空
        self.bottom_name=self.right_bottom_gender_entry.get()
        if self.bottom_name=='':
            for i in range(len(self.name)):  # 写入数据
                self.tree.insert('', i, values=(self.name[i], self.price[i], self.number[i],self.yno[i],self.gno[i],self.saletime[i]))
            for col in self.columns:  # 绑定函数，使表头可排序(这里的command=lambda _col=col还不是太懂)
                self.tree.heading(col, text=col, command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))
        else:
            try:
                name_index=self.name.index(self.bottom_name)
                self.tree.insert('', name_index, values=(
                    self.name[name_index], self.price[name_index], self.number[name_index],
                    self.yno[name_index],self.gno[name_index],self.saletime[name_index]))
                self.tree.update()
                for col in self.columns:  # 绑定函数，使表头可排序
                    self.tree.heading(col, text=col,
                                  command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))
            except:
                messagebox.showinfo('警告！', '商品不存在！')
        
	# 清空表格中的所有信息
    def delButton(self):
        x=self.tree.get_children()
        for item in x:
            self.tree.delete(item)


	# 在表格上的点击事件，这里是作用就是一点击表格就可以将信息直接写到左上角的框框中
    def click(self, event):
        self.col = self.tree.identify_column(event.x)  # 通过tree.identify_column()函数可以直接获取到列
        self.row = self.tree.identify_row(event.y)  # 行
 
        print(self.col)
        print(self.row)
        self.row_info = self.tree.item(self.row, "values")
        self.var_name.set(self.row_info[0])
        self.id1 = self.var_name.get()
        self.var_price.set(self.row_info[1])
        self.var_number.set(self.row_info[2])
        self.var_yno.set(self.row_info[3])
        self.var_gno.set(self.row_info[4])
        self.var_saletime.set(self.row_info[5])
        self.right_top_id_entry = tk.Entry(self.frame_left_top, state='disabled', textvariable=self.var_name, font=('Verdana', 15))
 
	# 点击中间的表格的表头，可以将那一列进行排序
    def tree_sort_column(self, tv, col, reverse):  # Treeview、列名、排列方式
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)  # 排序方式
        for index, (val, k) in enumerate(l):  # 根据排序后索引移动
            tv.move(k, '', index)
        tv.heading(col, command=lambda: self.tree_sort_column(tv, col, not reverse))  # 重写标题，使之成为再点倒序的标题
    #添加功能
    def new_row(self):
        print(self.var_name.get())
        print(self.name)
        if str(self.var_name.get()) in self.name:
            messagebox.showinfo('警告！', '该商品已存在！')
        else:
            if self.var_name.get() != '' and self.var_price.get() != '' and self.var_number.get() != '' and self.var_yno.get() != '' and self.var_gno.get() != '' and self.var_saletime.get() != '':
				#连接数据库
                db = conn()
                #获取游标、数据
                cursor = db.cursor()
                
                sql = "INSERT INTO 商品销售表 \
				       VALUES ('%s', '%s', '%s', '%s','%s','%s')" % \
					  (self.var_name.get(), self.var_price.get(), self.var_number.get(), self.var_yno.get(),self.var_gno.get(),self.var_saletime.get())  # SQL 插入语句
                try:
                    cursor.execute(sql)  # 执行sql语句
                    db.commit()  # 提交到数据库执行
                except:
                    db.rollback()  # 发生错误时回滚
                    messagebox.showinfo('警告！', '数据库连接失败！')
                    db.close()  # 关闭数据库连接
 
                self.name.append(self.var_name.get())
                self.price.append(self.var_price.get())
                self.number.append(self.var_number.get())
                self.yno.append(self.var_yno.get())
                self.gno.append(self.var_gno.get())
                self.saletime.append(self.var_saletime.get())
                self.tree.insert('', len(self.name) - 1, values=(
                self.name[len(self.name) - 1], self.price[len(self.name) - 1], self.number[len(self.name) - 1],
                self.yno[len(self.name) - 1],self.gno[len(self.name) - 1],self.saletime[len(self.name) - 1]))
                self.tree.update()
                messagebox.showinfo('提示！', '插入成功！')
            else:
                messagebox.showinfo('警告！', '请填写商品信息')
    #修改功能
    def updata_row(self):
        res = messagebox.askyesnocancel('警告！', '是否更新所填数据？')
        if res == True:
			#连接数据库
            db = conn()
            #获取游标、数据
            cursor = db.cursor()
            sql = "UPDATE 商品销售表 SET 商品名称 = '%s', 商品价格 = '%s', 销售数量 = '%s', 用户编号 = '%s' ,顾客编号 = '%s',销售时间 = '%s' where 商品名称 = '%s'" % (self.var_name.get(), self.var_price.get(), self.var_number.get(), self.var_yno.get(),self.var_gno.get(),self.var_saletime.get(),self.id1)  # SQL 插入语句
            try:
                cursor.execute(sql)  # 执行sql语句
                db.commit()  # 提交到数据库执行
                messagebox.showinfo('提示！', '更新成功！')
            except:
                db.rollback()  # 发生错误时回滚
                messagebox.showinfo('警告！', '更新失败，数据库连接失败！')
            db.close()  # 关闭数据库连接

            name_index = self.name.index(self.row_info[0])
            self.price[name_index] = self.var_price.get()
            self.number[name_index] = self.var_number.get()
            self.yno[name_index] = self.var_yno.get()
            self.gno[name_index] = self.var_gno.get()
            self.saletime[name_index] = self.var_saletime.get()

            self.tree.item(self.tree.selection()[0], values=(
                    self.var_name.get(), self.var_price.get(), self.var_number.get(),
                    self.var_yno.get(),self.var_gno.get(),self.var_saletime.get()))  # 修改对于行信息

	# 删除功能
    def del_row(self):
        res = messagebox.askyesnocancel('警告！', '是否删除所选数据？')
        if res == True:
            print(self.row_info[0])  # 鼠标选中的名称
            print(self.tree.selection()[0])  # 行号
            print(self.tree.get_children())  # 所有行
			#连接数据库
            db = conn()
            #获取游标、数据
            cursor = db.cursor()
            sql = "delete from 商品销售表 where 商品名称 = '%s'" % (self.row_info[0]) # SQL 插入语句
            try:
                cursor.execute(sql)  # 执行sql语句
                db.commit()  # 提交到数据库执行
                messagebox.showinfo('提示！', '删除成功！')
            except:
                db.rollback()  # 发生错误时回滚
                messagebox.showinfo('警告！', '删除失败，数据库连接失败！')
            db.close()  # 关闭数据库连接
 
            name_index = self.name.index(self.row_info[0])
            print(name_index)
            del self.name[name_index]
            del self.price[name_index]
            del self.number[name_index]
            del self.yno[name_index]
            del self.gno[name_index]
            del self.saletime[name_index]
            self.tree.delete(self.tree.selection()[0])  # 删除所选行
            print(self.tree.get_children())
    
    #提交数据到库存表  
    def putin(self):
        res = messagebox.askyesnocancel('警告！', '是否确定提交数据？')
        if res == True:
            #连接数据库
            db = conn()
            #获取游标、数据
            cursor = db.cursor()
            sql="update 商品库存表 set 商品数量=y.商品数量-j.销售数量 from 商品库存表 as y,商品销售表 as j where y.商品名称=j.商品名称"
            sql2="update 仓库表 set 仓库大小=10000-y.商品数量 from 商品库存表 as y,仓库表 as c where y.仓库号=c.仓库号"
            try:
                cursor.execute(sql)  # 执行sql语句
                cursor.execute(sql2)  # 执行sql语句
                db.commit()  # 提交到数据库执行
                messagebox.showinfo('提示！', '提交成功！')
            except:
                db.rollback()  # 发生错误时回滚
                messagebox.showinfo('警告！', '提交失败，数据库连接失败！')
            db.close()  # 关闭数据库连接
    

    def back(self):
        All_admin(self.window)   # 进入管理员子菜单操作界面 

#商品库存管理
class Commodity_inventory:
    def __init__(self, parent_window):
        parent_window.destroy() # 自定销毁上一个界面
        self.window = tk.Tk()  # 初始框的声明
        self.window.title('商品库存管理界面')
        self.window.geometry("760x637+250+15")	# 初始窗口在屏幕中的位置
        self.frame_left_top = tk.Frame(width=400, height=260)	# 指定框架，在窗口上可以显示，这里指定四个框架	
        self.frame_right_top = tk.Frame(width=250, height=250)
        self.frame_center = tk.Frame(width=740, height=270)
        self.frame_bottom = tk.Frame(width=650, height=70)
        
        # 定义下方中心列表区域
        self.columns = ("商品编号", "商品名称","商品数量","商品价格","供应商编号","进货日期","截止日期","仓库号")
        self.tree = ttk.Treeview(self.frame_center, show="headings", height=16, columns=self.columns)
        # 添加竖直滚动条
        self.vbar = ttk.Scrollbar(self.frame_center, orient="vertical", command=self.tree.yview)
		# 定义树形结构与滚动条
        self.tree.configure(yscrollcommand=self.vbar.set)

 
		# 表格的标题
        self.tree.column("商品编号", width=80, anchor='center')
        self.tree.column("商品名称", width=80, anchor='center')
        self.tree.column("商品数量", width=80, anchor='center')
        self.tree.column("商品价格", width=80, anchor='center')
        self.tree.column("供应商编号", width=80, anchor='center')
        self.tree.column("进货日期", width=80, anchor='center')
        self.tree.column("截止日期", width=80, anchor='center')
        self.tree.column("仓库号", width=80, anchor='center')
 
		# grid方法将tree和vbar进行布局
        self.tree.grid(row=0, column=0, sticky="NSEW")
        self.vbar.grid(row=0, column=1, sticky="NS")
	
		# 定义几个数组，为中间的那个大表格做一些准备
        self.sno = []
        self.name = []
        self.number = []
        self.price = []
        self.gno = []
        self.stime = []
        self.ltime = []
        self.warehouse = []
        
        #连接数据库
        db = conn()
        #获取游标、数据
        cur = db.cursor()
        sql = "SELECT * FROM 商品库存表 "
        try:
			# 执行SQL语句
            cur.execute(sql)
			# 获取所有记录列表
            results = cur.fetchall()
            for row in results:
                self.sno.append(row[0])
                self.name.append(row[1].encode('latin-1').decode('gbk'))
                self.number.append(row[2])
                self.price.append(row[3])
                self.gno.append(row[4])
                self.stime.append(row[5])
                self.ltime.append(row[6])
                self.warehouse.append(row[7])
        except:
            messagebox.showinfo('警告！', '数据库连接失败！')
        db.close()# 关闭数据库连接
        
        print("test***********************")
        for i in range(len(self.name)):  # 写入数据
            self.tree.insert('', i, values=(self.sno[i], self.name[i], self.number[i],self.price[i],self.gno[i],self.stime[i],self.ltime[i],self.warehouse[i]))

        for col in self.columns:  # 绑定函数，使表头可排序(这里的command=lambda _col=col还不是太懂)
            self.tree.heading(col, text=col, command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))
 
		# 定义顶部区域
		# 定义左上方区域
        self.top_title = tk.Label(self.frame_left_top, text="商品库存信息:", font=('Verdana', 15))
        self.top_title.grid(row=0, column=0, columnspan=2, sticky="NSEW", padx=40, pady=5)   # NSEW表示允许组件向4个方向都可以拉伸

		# 定义下方区域
        self.chaxun = tk.StringVar()
        self.right_bottom_gender_entry = tk.Entry(self.frame_bottom, textvariable=self.chaxun, font=('Verdana', 15))
        self.right_bottom_button = ttk.Button(self.frame_bottom, text='商品名称查询', width=18, command=self.put_data)
        self.right_bottom_button.grid(row=0, column=0, padx=18, pady=18)  # 位置设置
        self.right_bottom_gender_entry.grid(row=0, column=1)
 
        self.left_top_frame = tk.Frame(self.frame_left_top)
        self.var_sno = tk.StringVar()  
        self.var_name = tk.StringVar()  
        self.var_number = tk.StringVar()  
        self.var_price = tk.StringVar()  
        self.var_gno = tk.StringVar()
        self.var_stime = tk.StringVar()
        self.var_ltime = tk.StringVar()
        self.var_warehouse = tk.StringVar()
		# 商品编号
        self.right_top_id_label = tk.Label(self.frame_left_top, text="商品编号: ", font=('Verdana', 11))
        self.right_top_id_entry = tk.Entry(self.frame_left_top, textvariable=self.var_sno, font=('Verdana', 14))
        self.right_top_id_label.grid(row=1, column=0)
        self.right_top_id_entry.grid(row=1, column=1)
		# 商品名称
        self.right_top_price_label = tk.Label(self.frame_left_top, text="商品名称：", font=('Verdana', 11))
        self.right_top_price_entry = tk.Entry(self.frame_left_top, textvariable=self.var_name, font=('Verdana', 14))
        self.right_top_price_label.grid(row=2, column=0)  # 位置设置
        self.right_top_price_entry.grid(row=2, column=1)
		# 商品数量
        self.right_top_number_label = tk.Label(self.frame_left_top, text="商品数量：", font=('Verdana', 11))
        self.right_top_number_entry = tk.Entry(self.frame_left_top, textvariable=self.var_number,font=('Verdana', 14))
        self.right_top_number_label.grid(row=3, column=0)  # 位置设置
        self.right_top_number_entry.grid(row=3, column=1)
		# 商品价格
        self.right_top_yno_label = tk.Label(self.frame_left_top, text="商品价格：", font=('Verdana', 11))
        self.right_top_yno_entry = tk.Entry(self.frame_left_top, textvariable=self.var_price, font=('Verdana', 14))
        self.right_top_yno_label.grid(row=4, column=0)  # 位置设置
        self.right_top_yno_entry.grid(row=4, column=1)
        # 供应商编号
        self.right_top_gno_label = tk.Label(self.frame_left_top, text="供应商编号：", font=('Verdana', 11))
        self.right_top_gno_entry = tk.Entry(self.frame_left_top, textvariable=self.var_gno, font=('Verdana', 14))
        self.right_top_gno_label.grid(row=5, column=0)  # 位置设置
        self.right_top_gno_entry.grid(row=5, column=1)
        # 进货时间
        self.right_top_saletime_label = tk.Label(self.frame_left_top, text="进货日期：", font=('Verdana', 11))
        self.right_top_saletime_entry = tk.Entry(self.frame_left_top, textvariable=self.var_stime, font=('Verdana', 14))
        self.right_top_saletime_label.grid(row=6, column=0)  # 位置设置
        self.right_top_saletime_entry.grid(row=6, column=1)
         # 截至时间
        self.right_top_saletime_label = tk.Label(self.frame_left_top, text="截止日期：", font=('Verdana', 11))
        self.right_top_saletime_entry = tk.Entry(self.frame_left_top, textvariable=self.var_ltime, font=('Verdana', 14))
        self.right_top_saletime_label.grid(row=7, column=0)  # 位置设置
        self.right_top_saletime_entry.grid(row=7, column=1)
        
        self.right_top_saletime_label = tk.Label(self.frame_left_top, text="仓库号：", font=('Verdana', 11))
        self.right_top_saletime_entry = tk.Entry(self.frame_left_top, textvariable=self.var_warehouse, font=('Verdana', 14))
        self.right_top_saletime_label.grid(row=8, column=0)  # 位置设置
        self.right_top_saletime_entry.grid(row=8, column=1)
 
		# 定义右上方区域
        self.right_top_title = tk.Label(self.frame_right_top, text="操作：", font=('Verdana', 17))
        self.tree.bind('<Button-1>', self.click)  # 左键获取位置(tree.bind可以绑定一系列的事件，可以搜索ttk相关参数查看)
        self.right_top_button1 = ttk.Button(self.frame_right_top, text='新建商品信息', width=20, command=self.new_row)
        self.right_top_button2 = ttk.Button(self.frame_right_top, text='更新选中商品信息', width=20,command=self.updata_row)
        self.right_top_button3 = ttk.Button(self.frame_right_top, text='删除选中商品信息', width=20,command=self.del_row)
        self.right_top_button4 = ttk.Button(self.frame_right_top, text='提交数据', width=20,command=self.putin)

		# 右上角按钮的位置设置
        self.right_top_title.grid(row=1, column=0, pady=10)
        self.right_top_button1.grid(row=2, column=0, padx=20, pady=10)
        self.right_top_button2.grid(row=3, column=0, padx=20, pady=10)
        self.right_top_button3.grid(row=4, column=0, padx=20, pady=10)
        self.right_top_button4.grid(row=5, column=0, padx=20, pady=10)
 
		# 整体区域定位，利用了Frame和grid进行布局
        self.frame_left_top.grid(row=0, column=0, padx=2, pady=5)
        self.frame_right_top.grid(row=0, column=1, padx=30, pady=30)
        self.frame_center.grid(row=1, column=0, columnspan=2, padx=3, pady=5)
        self.frame_bottom.grid(row=2, column=0, columnspan=2)
 
		# 设置固定组件，(0)就是将组件进行了固定
        self.frame_left_top.grid_propagate(0)
        self.frame_right_top.grid_propagate(0)
        self.frame_center.grid_propagate(0)
        self.frame_bottom.grid_propagate(0)
 
        self.frame_left_top.tkraise() # 开始显示主菜单，tkraise()提高z轴的顺序（不太懂）
        self.frame_right_top.tkraise() # 开始显示主菜单
        self.frame_center.tkraise() # 开始显示主菜单
        self.frame_bottom.tkraise() # 开始显示主菜单
 
        self.window.protocol("WM_DELETE_WINDOW", self.back)  # 捕捉右上角关闭点击，执行back方法
        self.window.mainloop()  # 进入消息循环

	# 将查到的信息放到中间的表格中
    def put_data(self):
        self.delButton()	# 先将表格内的内容全部清空
        self.bottom_name=self.right_bottom_gender_entry.get()
        if self.bottom_name=='':
            for i in range(len(self.name)):  # 写入数据
                self.tree.insert('', i, values=(self.sno[i], self.name[i], self.number[i],self.price[i],self.gno[i],self.stime[i],self.ltime[i],self.warehouse[i]))
            for col in self.columns:  # 绑定函数，使表头可排序(这里的command=lambda _col=col还不是太懂)
                self.tree.heading(col, text=col, command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))
        else:
            try:
                name_index=self.name.index(self.bottom_name)
                self.tree.insert('', name_index, values=(
                    self.sno[name_index], self.name[name_index], self.number[name_index],
                    self.price[name_index],self.gno[name_index],self.stime[name_index],self.ltime[name_index],self.warehouse[name_index]))
                self.tree.update()
                for col in self.columns:  # 绑定函数，使表头可排序
                    self.tree.heading(col, text=col,
                                  command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))
            except:
                messagebox.showinfo('警告！', '商品不存在！')
        
	# 清空表格中的所有信息
    def delButton(self):
        x=self.tree.get_children()
        for item in x:
            self.tree.delete(item)


	# 在表格上的点击事件，这里是作用就是一点击表格就可以将信息直接写到左上角的框框中
    def click(self, event):
        self.col = self.tree.identify_column(event.x)  # 通过tree.identify_column()函数可以直接获取到列
        self.row = self.tree.identify_row(event.y)  # 行
 
        print(self.col)
        print(self.row)
        self.row_info = self.tree.item(self.row, "values")
        self.var_sno.set(self.row_info[0])
        self.var_name.set(self.row_info[1])
        self.var_number.set(self.row_info[2])
        self.var_price.set(self.row_info[3])
        self.var_gno.set(self.row_info[4])
        self.var_stime.set(self.row_info[5])
        self.var_ltime.set(self.row_info[6])
        self.var_warehouse.set(self.row_info[7])
        self.right_top_id_entry = tk.Entry(self.frame_left_top, state='disabled', textvariable=self.var_name, font=('Verdana', 15))
 
	# 点击中间的表格的表头，可以将那一列进行排序
    def tree_sort_column(self, tv, col, reverse):  # Treeview、列名、排列方式
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)  # 排序方式
        for index, (val, k) in enumerate(l):  # 根据排序后索引移动
            tv.move(k, '', index)
        tv.heading(col, command=lambda: self.tree_sort_column(tv, col, not reverse))  # 重写标题，使之成为再点倒序的标题
    #添加功能
    def new_row(self):
        print(self.var_name.get())
        print(self.name)
        if str(self.var_name.get()) in self.name:
            messagebox.showinfo('警告！', '该商品已存在！')
        else:
            if self.var_sno.get() != '' and self.var_name.get() != '' and self.var_number.get() != '' and self.var_price.get() != '' and self.var_gno.get() != '' and self.var_stime.get() != '' and self.var_ltime.get() != '' and self.var_warehouse.get() != '':
				#连接数据库
                db = conn()
                #获取游标、数据
                cursor = db.cursor()
                
                sql = "INSERT INTO 商品库存表 \
				       VALUES ('%s', '%s', '%s', '%s','%s','%s','%s','%s')" % \
					  (self.var_sno.get(), self.var_name.get(), self.var_number.get(), self.var_price.get(),self.var_gno.get(),self.var_stime.get(),self.var_ltime.get(),self.var_warehouse.get())  # SQL 插入语句
                try:
                    cursor.execute(sql)  # 执行sql语句
                    db.commit()  # 提交到数据库执行
                except:
                    db.rollback()  # 发生错误时回滚
                    messagebox.showinfo('警告！', '数据库连接失败！')
                    db.close()  # 关闭数据库连接
 
                self.sno.append(self.var_sno.get())
                self.name.append(self.var_name.get())
                self.number.append(self.var_number.get())
                self.price.append(self.var_price.get())
                self.gno.append(self.var_gno.get())
                self.stime.append(self.var_stime.get())
                self.ltime.append(self.var_ltime.get())
                self.warehouse.append(self.var_warehouse.get())
                self.tree.insert('', len(self.name) - 1, values=(
                self.sno[len(self.name) - 1], self.name[len(self.name) - 1], self.number[len(self.name) - 1],
                self.price[len(self.name) - 1],self.gno[len(self.name) - 1],self.stime[len(self.name) - 1],self.ltime[len(self.name) - 1],self.warehouse[len(self.name) - 1]))
                self.tree.update()
                messagebox.showinfo('提示！', '插入成功！')
            else:
                messagebox.showinfo('警告！', '请填写商品信息')
    #修改功能
    def updata_row(self):
        res = messagebox.askyesnocancel('警告！', '是否更新所填数据？')
        if res == True:
			#连接数据库
            db = conn()
            #获取游标、数据
            cursor = db.cursor()
            sql = "UPDATE 商品库存表 SET 商品名称 = '%s', 商品数量 = '%s', 商品价格 = '%s' ,供应商编号 = '%s',进货日期 = '%s' ,截止日期 = '%s' ,仓库号 = '%s' where 商品编号 = '%s'" % (self.var_name.get(), self.var_number.get(), self.var_price.get(), self.var_gno.get(),self.var_stime.get(),self.var_ltime.get(),self.var_warehouse.get(),self.var_sno.get())  # SQL 插入语句
            print(self.sno)
            try:
                cursor.execute(sql)  # 执行sql语句
                db.commit()  # 提交到数据库执行
                messagebox.showinfo('提示！', '更新成功！')
            except:
                db.rollback()  # 发生错误时回滚
                messagebox.showinfo('警告！', '更新失败，数据库连接失败！')
            db.close()  # 关闭数据库连接


            sno_index = self.sno.index(self.row_info[0])
            self.name[sno_index] = self.var_name.get()
            self.number[sno_index] = self.var_number.get()
            self.price[sno_index] = self.var_price.get()
            self.gno[sno_index] = self.var_gno.get()
            self.stime[sno_index] = self.var_stime.get()
            self.ltime[sno_index] = self.var_ltime.get()
            self.warehouse[sno_index] = self.var_warehouse.get()

            self.tree.item(self.tree.selection()[0], values=(
                    self.var_sno.get(), self.var_name.get(), self.var_number.get(),
                    self.var_price.get(),self.var_gno.get(),self.var_stime.get(),self.var_ltime.get(),self.var_warehouse.get()))  # 修改对于行信息

	# 删除功能
    def del_row(self):
        res = messagebox.askyesnocancel('警告！', '是否删除所选数据？')
        if res == True:
            print(self.row_info[0])  # 鼠标选中的名称
            print(self.tree.selection()[0])  # 行号
            print(self.tree.get_children())  # 所有行
			#连接数据库
            db = conn()
            #获取游标、数据
            cursor = db.cursor()
            sql = "delete from 商品库存表 where 商品编号 = '%s'" % (self.row_info[0]) # SQL 插入语句
            try:
                cursor.execute(sql)  # 执行sql语句
                db.commit()  # 提交到数据库执行
                messagebox.showinfo('提示！', '删除成功！')
            except:
                db.rollback()  # 发生错误时回滚
                messagebox.showinfo('警告！', '删除失败，数据库连接失败！')
            db.close()  # 关闭数据库连接
 
            sno_index = self.sno.index(self.row_info[0])
            print(sno_index)
            del self.sno[sno_index]
            del self.name[sno_index]
            del self.number[sno_index]
            del self.price[sno_index]
            del self.gno[sno_index]
            del self.stime[sno_index]
            del self.ltime[sno_index]
            del self.warehouse[sno_index]
            self.tree.delete(self.tree.selection()[0])  # 删除所选行
            print(self.tree.get_children())
    
    #提交数据到库存表  
    def putin(self):
        res = messagebox.askyesnocancel('警告！', '是否确定提交数据？')
        if res == True:
            #连接数据库
            db = conn()
            #获取游标、数据
            cursor = db.cursor()
            sql="update 仓库表 set 仓库大小=10000-y.商品数量 from 商品库存表 as y,仓库表 as c where y.仓库号=c.仓库号"
            try:
                cursor.execute(sql)  # 执行sql语句
                db.commit()  # 提交到数据库执行
                messagebox.showinfo('提示！', '提交成功！')
            except:
                db.rollback()  # 发生错误时回滚
                messagebox.showinfo('警告！', '提交失败，数据库连接失败！')
            db.close()  # 关闭数据库连接

    def back(self):
        All_admin(self.window)   # 进入管理员子菜单操作界面 

#原材料库存管理
class Material_inventory:
    def __init__(self, parent_window):
        parent_window.destroy() # 自定销毁上一个界面
        self.window = tk.Tk()  # 初始框的声明
        self.window.title('原材料库存管理界面')
        self.window.geometry("760x637+250+15")	# 初始窗口在屏幕中的位置
        self.frame_left_top = tk.Frame(width=400, height=260)	# 指定框架，在窗口上可以显示，这里指定四个框架	
        self.frame_right_top = tk.Frame(width=250, height=250)
        self.frame_center = tk.Frame(width=740, height=270)
        self.frame_bottom = tk.Frame(width=650, height=70)
        
        # 定义下方中心列表区域
        self.columns = ("原材料编号", "原材料名称","原材料数量","原材料价格","供应商编号","进货日期","截止日期","仓库号")
        self.tree = ttk.Treeview(self.frame_center, show="headings", height=16, columns=self.columns)
        # 添加竖直滚动条
        self.vbar = ttk.Scrollbar(self.frame_center, orient="vertical", command=self.tree.yview)
		# 定义树形结构与滚动条
        self.tree.configure(yscrollcommand=self.vbar.set)

 
		# 表格的标题
        self.tree.column("原材料编号", width=80, anchor='center')
        self.tree.column("原材料名称", width=80, anchor='center')
        self.tree.column("原材料数量", width=80, anchor='center')
        self.tree.column("原材料价格", width=80, anchor='center')
        self.tree.column("供应商编号", width=80, anchor='center')
        self.tree.column("进货日期", width=80, anchor='center')
        self.tree.column("截止日期", width=80, anchor='center')
        self.tree.column("仓库号", width=80, anchor='center')
 
		# grid方法将tree和vbar进行布局
        self.tree.grid(row=0, column=0, sticky="NSEW")
        self.vbar.grid(row=0, column=1, sticky="NS")
	
		# 定义几个数组，为中间的那个大表格做一些准备
        self.sno = []
        self.name = []
        self.number = []
        self.price = []
        self.gno = []
        self.stime = []
        self.ltime = []
        self.warehouse = []
        
        #连接数据库
        db = conn()
        #获取游标、数据
        cur = db.cursor()
        sql = "SELECT * FROM 原材料库存表 "
        try:
			# 执行SQL语句
            cur.execute(sql)
			# 获取所有记录列表
            results = cur.fetchall()
            for row in results:
                self.sno.append(row[0])
                self.name.append(row[1].encode('latin-1').decode('gbk'))
                self.number.append(row[2])
                self.price.append(row[3])
                self.gno.append(row[4])
                self.stime.append(row[5])
                self.ltime.append(row[6])
                self.warehouse.append(row[7])
        except:
            messagebox.showinfo('警告！', '数据库连接失败！')
        db.close()# 关闭数据库连接
        
        print("test***********************")
        for i in range(len(self.name)):  # 写入数据
            self.tree.insert('', i, values=(self.sno[i], self.name[i], self.number[i],self.price[i],self.gno[i],self.stime[i],self.ltime[i],self.warehouse[i]))

        for col in self.columns:  # 绑定函数，使表头可排序(这里的command=lambda _col=col还不是太懂)
            self.tree.heading(col, text=col, command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))
 
		# 定义顶部区域
		# 定义左上方区域
        self.top_title = tk.Label(self.frame_left_top, text="原材料库存信息:", font=('Verdana', 15))
        self.top_title.grid(row=0, column=0, columnspan=2, sticky="NSEW", padx=40, pady=5)   # NSEW表示允许组件向4个方向都可以拉伸

		# 定义下方区域
        self.chaxun = tk.StringVar()
        self.right_bottom_gender_entry = tk.Entry(self.frame_bottom, textvariable=self.chaxun, font=('Verdana', 15))
        self.right_bottom_button = ttk.Button(self.frame_bottom, text='原材料名称查询', width=18, command=self.put_data)
        self.right_bottom_button.grid(row=0, column=0, padx=18, pady=18)  # 位置设置
        self.right_bottom_gender_entry.grid(row=0, column=1)
 
        self.left_top_frame = tk.Frame(self.frame_left_top)
        self.var_sno = tk.StringVar()  
        self.var_name = tk.StringVar()  
        self.var_number = tk.StringVar()  
        self.var_price = tk.StringVar()  
        self.var_gno = tk.StringVar()
        self.var_stime = tk.StringVar()
        self.var_ltime = tk.StringVar()
        self.var_warehouse = tk.StringVar()
		# 商品编号
        self.right_top_id_label = tk.Label(self.frame_left_top, text="原材料编号: ", font=('Verdana', 11))
        self.right_top_id_entry = tk.Entry(self.frame_left_top, textvariable=self.var_sno, font=('Verdana', 14))
        self.right_top_id_label.grid(row=1, column=0)
        self.right_top_id_entry.grid(row=1, column=1)
		# 商品名称
        self.right_top_price_label = tk.Label(self.frame_left_top, text="原材料名称：", font=('Verdana', 11))
        self.right_top_price_entry = tk.Entry(self.frame_left_top, textvariable=self.var_name, font=('Verdana', 14))
        self.right_top_price_label.grid(row=2, column=0)  # 位置设置
        self.right_top_price_entry.grid(row=2, column=1)
		# 商品数量
        self.right_top_number_label = tk.Label(self.frame_left_top, text="原材料数量：", font=('Verdana', 11))
        self.right_top_number_entry = tk.Entry(self.frame_left_top, textvariable=self.var_number,font=('Verdana', 14))
        self.right_top_number_label.grid(row=3, column=0)  # 位置设置
        self.right_top_number_entry.grid(row=3, column=1)
		# 商品价格
        self.right_top_yno_label = tk.Label(self.frame_left_top, text="原材料价格：", font=('Verdana', 11))
        self.right_top_yno_entry = tk.Entry(self.frame_left_top, textvariable=self.var_price, font=('Verdana', 14))
        self.right_top_yno_label.grid(row=4, column=0)  # 位置设置
        self.right_top_yno_entry.grid(row=4, column=1)
        # 供应商编号
        self.right_top_gno_label = tk.Label(self.frame_left_top, text="供应商编号：", font=('Verdana', 11))
        self.right_top_gno_entry = tk.Entry(self.frame_left_top, textvariable=self.var_gno, font=('Verdana', 14))
        self.right_top_gno_label.grid(row=5, column=0)  # 位置设置
        self.right_top_gno_entry.grid(row=5, column=1)
        # 进货时间
        self.right_top_saletime_label = tk.Label(self.frame_left_top, text="进货日期：", font=('Verdana', 11))
        self.right_top_saletime_entry = tk.Entry(self.frame_left_top, textvariable=self.var_stime, font=('Verdana', 14))
        self.right_top_saletime_label.grid(row=6, column=0)  # 位置设置
        self.right_top_saletime_entry.grid(row=6, column=1)
         # 截至时间
        self.right_top_saletime_label = tk.Label(self.frame_left_top, text="截止日期：", font=('Verdana', 11))
        self.right_top_saletime_entry = tk.Entry(self.frame_left_top, textvariable=self.var_ltime, font=('Verdana', 14))
        self.right_top_saletime_label.grid(row=7, column=0)  # 位置设置
        self.right_top_saletime_entry.grid(row=7, column=1)
        
        self.right_top_saletime_label = tk.Label(self.frame_left_top, text="仓库号：", font=('Verdana', 11))
        self.right_top_saletime_entry = tk.Entry(self.frame_left_top, textvariable=self.var_warehouse, font=('Verdana', 14))
        self.right_top_saletime_label.grid(row=8, column=0)  # 位置设置
        self.right_top_saletime_entry.grid(row=8, column=1)
 
		# 定义右上方区域
        self.right_top_title = tk.Label(self.frame_right_top, text="操作：", font=('Verdana', 17))
        self.tree.bind('<Button-1>', self.click)  # 左键获取位置(tree.bind可以绑定一系列的事件，可以搜索ttk相关参数查看)
        self.right_top_button1 = ttk.Button(self.frame_right_top, text='新建原材料信息', width=20, command=self.new_row)
        self.right_top_button2 = ttk.Button(self.frame_right_top, text='更新选中原材料信息', width=20,command=self.updata_row)
        self.right_top_button3 = ttk.Button(self.frame_right_top, text='删除选中原材料信息', width=20,command=self.del_row)
        self.right_top_button4 = ttk.Button(self.frame_right_top, text='提交数据', width=20,command=self.putin)

		# 右上角按钮的位置设置
        self.right_top_title.grid(row=1, column=0, pady=10)
        self.right_top_button1.grid(row=2, column=0, padx=20, pady=10)
        self.right_top_button2.grid(row=3, column=0, padx=20, pady=10)
        self.right_top_button3.grid(row=4, column=0, padx=20, pady=10)
        self.right_top_button4.grid(row=5, column=0, padx=20, pady=10)
 
		# 整体区域定位，利用了Frame和grid进行布局
        self.frame_left_top.grid(row=0, column=0, padx=2, pady=5)
        self.frame_right_top.grid(row=0, column=1, padx=30, pady=30)
        self.frame_center.grid(row=1, column=0, columnspan=2, padx=3, pady=5)
        self.frame_bottom.grid(row=2, column=0, columnspan=2)
 
		# 设置固定组件，(0)就是将组件进行了固定
        self.frame_left_top.grid_propagate(0)
        self.frame_right_top.grid_propagate(0)
        self.frame_center.grid_propagate(0)
        self.frame_bottom.grid_propagate(0)
 
        self.frame_left_top.tkraise() # 开始显示主菜单，tkraise()提高z轴的顺序（不太懂）
        self.frame_right_top.tkraise() # 开始显示主菜单
        self.frame_center.tkraise() # 开始显示主菜单
        self.frame_bottom.tkraise() # 开始显示主菜单
 
        self.window.protocol("WM_DELETE_WINDOW", self.back)  # 捕捉右上角关闭点击，执行back方法
        self.window.mainloop()  # 进入消息循环

	# 将查到的信息放到中间的表格中
    def put_data(self):
        self.delButton()	# 先将表格内的内容全部清空
        self.bottom_name=self.right_bottom_gender_entry.get()
        if self.bottom_name=='':
            for i in range(len(self.name)):  # 写入数据
                self.tree.insert('', i, values=(self.sno[i], self.name[i], self.number[i],self.price[i],self.gno[i],self.stime[i],self.ltime[i],self.warehouse[i]))
            for col in self.columns:  # 绑定函数，使表头可排序(这里的command=lambda _col=col还不是太懂)
                self.tree.heading(col, text=col, command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))
        else:
            try:
                name_index=self.name.index(self.bottom_name)
                self.tree.insert('', name_index, values=(
                    self.sno[name_index], self.name[name_index], self.number[name_index],
                    self.price[name_index],self.gno[name_index],self.stime[name_index],self.ltime[name_index],self.warehouse[name_index]))
                self.tree.update()
                for col in self.columns:  # 绑定函数，使表头可排序
                    self.tree.heading(col, text=col,
                                  command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))
            except:
                messagebox.showinfo('警告！', '原材料不存在！')
        
	# 清空表格中的所有信息
    def delButton(self):
        x=self.tree.get_children()
        for item in x:
            self.tree.delete(item)


	# 在表格上的点击事件，这里是作用就是一点击表格就可以将信息直接写到左上角的框框中
    def click(self, event):
        self.col = self.tree.identify_column(event.x)  # 通过tree.identify_column()函数可以直接获取到列
        self.row = self.tree.identify_row(event.y)  # 行
 
        print(self.col)
        print(self.row)
        self.row_info = self.tree.item(self.row, "values")
        self.var_sno.set(self.row_info[0])
        self.var_name.set(self.row_info[1])
        self.var_number.set(self.row_info[2])
        self.var_price.set(self.row_info[3])
        self.var_gno.set(self.row_info[4])
        self.var_stime.set(self.row_info[5])
        self.var_ltime.set(self.row_info[6])
        self.var_warehouse.set(self.row_info[7])
        self.right_top_id_entry = tk.Entry(self.frame_left_top, state='disabled', textvariable=self.var_name, font=('Verdana', 15))
 
	# 点击中间的表格的表头，可以将那一列进行排序
    def tree_sort_column(self, tv, col, reverse):  # Treeview、列名、排列方式
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)  # 排序方式
        for index, (val, k) in enumerate(l):  # 根据排序后索引移动
            tv.move(k, '', index)
        tv.heading(col, command=lambda: self.tree_sort_column(tv, col, not reverse))  # 重写标题，使之成为再点倒序的标题
    #添加功能
    def new_row(self):
        print(self.var_name.get())
        print(self.name)
        if str(self.var_name.get()) in self.name:
            messagebox.showinfo('警告！', '该商品已存在！')
        else:
            if self.var_sno.get() != '' and self.var_name.get() != '' and self.var_number.get() != '' and self.var_price.get() != '' and self.var_gno.get() != '' and self.var_stime.get() != '' and self.var_ltime.get() != '' and self.var_warehouse.get() != '':
				#连接数据库
                db = conn()
                #获取游标、数据
                cursor = db.cursor()
                
                sql = "INSERT INTO 原材料库存表 \
				       VALUES ('%s', '%s', '%s', '%s','%s','%s','%s','%s')" % \
					  (self.var_sno.get(), self.var_name.get(), self.var_number.get(), self.var_price.get(),self.var_gno.get(),self.var_stime.get(),self.var_ltime.get(),self.var_warehouse.get())  # SQL 插入语句
                try:
                    cursor.execute(sql)  # 执行sql语句
                    db.commit()  # 提交到数据库执行
                except:
                    db.rollback()  # 发生错误时回滚
                    messagebox.showinfo('警告！', '数据库连接失败！')
                    db.close()  # 关闭数据库连接
 
                self.sno.append(self.var_sno.get())
                self.name.append(self.var_name.get())
                self.number.append(self.var_number.get())
                self.price.append(self.var_price.get())
                self.gno.append(self.var_gno.get())
                self.stime.append(self.var_stime.get())
                self.ltime.append(self.var_ltime.get())
                self.warehouse.append(self.var_warehouse.get())
                self.tree.insert('', len(self.name) - 1, values=(
                self.sno[len(self.name) - 1], self.name[len(self.name) - 1], self.number[len(self.name) - 1],
                self.price[len(self.name) - 1],self.gno[len(self.name) - 1],self.stime[len(self.name) - 1],self.ltime[len(self.name) - 1],self.warehouse[len(self.name) - 1]))
                self.tree.update()
                messagebox.showinfo('提示！', '插入成功！')
            else:
                messagebox.showinfo('警告！', '请填写商品信息')
    #修改功能
    def updata_row(self):
        res = messagebox.askyesnocancel('警告！', '是否更新所填数据？')
        if res == True:
			#连接数据库
            db = conn()
            #获取游标、数据
            cursor = db.cursor()
            sql = "UPDATE 原材料库存表 SET 原材料名称 = '%s', 原材料数量 = '%s', 原材料价格 = '%s' ,供应商编号 = '%s',进货日期 = '%s' ,截止日期 = '%s' ,仓库号 = '%s' where 原材料编号 = '%s'" % (self.var_name.get(), self.var_number.get(), self.var_price.get(), self.var_gno.get(),self.var_stime.get(),self.var_ltime.get(),self.var_warehouse.get(),self.var_sno.get())  # SQL 插入语句
            try:
                cursor.execute(sql)  # 执行sql语句
                db.commit()  # 提交到数据库执行
                messagebox.showinfo('提示！', '更新成功！')
            except:
                db.rollback()  # 发生错误时回滚
                messagebox.showinfo('警告！', '更新失败，数据库连接失败！')
            db.close()  # 关闭数据库连接


            sno_index = self.sno.index(self.row_info[0])
            self.name[sno_index] = self.var_name.get()
            self.number[sno_index] = self.var_number.get()
            self.price[sno_index] = self.var_price.get()
            self.gno[sno_index] = self.var_gno.get()
            self.stime[sno_index] = self.var_stime.get()
            self.ltime[sno_index] = self.var_ltime.get()
            self.warehouse[sno_index] = self.var_warehouse.get()

            self.tree.item(self.tree.selection()[0], values=(
                    self.var_sno.get(), self.var_name.get(), self.var_number.get(),
                    self.var_price.get(),self.var_gno.get(),self.var_stime.get(),self.var_ltime.get(),self.var_warehouse.get()))  # 修改对于行信息

	# 删除功能
    def del_row(self):
        res = messagebox.askyesnocancel('警告！', '是否删除所选数据？')
        if res == True:
            print(self.row_info[0])  # 鼠标选中的名称
            print(self.tree.selection()[0])  # 行号
            print(self.tree.get_children())  # 所有行
			#连接数据库
            db = conn()
            #获取游标、数据
            cursor = db.cursor()
            sql = "delete from 原材料库存表 where 原材料编号 = '%s'" % (self.row_info[0]) # SQL 插入语句
            try:
                cursor.execute(sql)  # 执行sql语句
                db.commit()  # 提交到数据库执行
                messagebox.showinfo('提示！', '删除成功！')
            except:
                db.rollback()  # 发生错误时回滚
                messagebox.showinfo('警告！', '删除失败，数据库连接失败！')
            db.close()  # 关闭数据库连接
 
            sno_index = self.sno.index(self.row_info[0])
            print(sno_index)
            del self.sno[sno_index]
            del self.name[sno_index]
            del self.number[sno_index]
            del self.price[sno_index]
            del self.gno[sno_index]
            del self.stime[sno_index]
            del self.ltime[sno_index]
            del self.warehouse[sno_index]
            self.tree.delete(self.tree.selection()[0])  # 删除所选行
            print(self.tree.get_children())
            
    #提交数据到库存表  
    def putin(self):
        res = messagebox.askyesnocancel('警告！', '是否确定提交数据？')
        if res == True:
            #连接数据库
            db = conn()
            #获取游标、数据
            cursor = db.cursor()
            sql="update 仓库表 set 仓库大小=10000-y.原材料数量 from 原材料库存表 as y,仓库表 as c where y.仓库号=c.仓库号"
            try:
                cursor.execute(sql)  # 执行sql语句
                db.commit()  # 提交到数据库执行
                messagebox.showinfo('提示！', '提交成功！')
            except:
                db.rollback()  # 发生错误时回滚
                messagebox.showinfo('警告！', '提交失败，数据库连接失败！')
            db.close()  # 关闭数据库连接

    def back(self):
        All_admin(self.window)   # 进入管理员子菜单操作界面 


#建立仓库管理类
class WarehouseManage:
    def __init__(self,parent_window):
        parent_window.destroy() # 自定销毁上一个界面
        self.window = tk.Tk()  # 初始框的声明
        self.window.title('仓库管理界面')
        self.window.geometry("700x600+250+15")	# 初始窗口在屏幕中的位置
        self.frame_left_top = tk.Frame(width=300, height=200)	# 指定框架，在窗口上可以显示，这里指定四个框架	
        self.frame_right_top = tk.Frame(width=250, height=200)
        self.frame_center = tk.Frame(width=650, height=250)
        self.frame_bottom = tk.Frame(width=650, height=70)
        
        # 定义下方中心列表区域
        self.columns = ("仓库号", "仓库名称","仓库大小","仓库地址")
        self.tree = ttk.Treeview(self.frame_center, show="headings", height=16, columns=self.columns)
        # 添加竖直滚动条
        self.vbar = ttk.Scrollbar(self.frame_center, orient="vertical", command=self.tree.yview)
		# 定义树形结构与滚动条
        self.tree.configure(yscrollcommand=self.vbar.set)

		# 定义id1为修改id时的暂存变量，这个是为了更新信息而设计的
        self.id1 = 0
 
		# 表格的标题
        self.tree.column("仓库号", width=130, anchor='center')
        self.tree.column("仓库名称", width=130, anchor='center')
        self.tree.column("仓库大小", width=130, anchor='center')
        self.tree.column("仓库地址", width=150, anchor='center')
 
		# grid方法将tree和vbar进行布局
        self.tree.grid(row=0, column=0, sticky="NSEW")
        self.vbar.grid(row=0, column=1, sticky="NS")
	
		# 定义几个数组，为中间的那个大表格做一些准备
        self.cno = []
        self.name = []
        self.size = []
        self.place = []
        
        #连接数据库
        db = conn()
        #获取游标、数据
        cur = db.cursor()
        sql = "SELECT * FROM 仓库表 "
        try:
			# 执行SQL语句
            cur.execute(sql)
			# 获取所有记录列表
            results = cur.fetchall()
            for row in results:
                self.cno.append(row[0])
                self.name.append(row[1].encode('latin-1').decode('gbk'))
                self.size.append(row[2])
                self.place.append(row[3].encode('latin-1').decode('gbk'))
        except:
            messagebox.showinfo('警告！', '数据库连接失败！')
        db.close()# 关闭数据库连接
        
        print("test***********************")
        for i in range(len(self.name)):  # 写入数据
            self.tree.insert('', i, values=(self.cno[i], self.name[i], self.size[i],self.place[i]))

        for col in self.columns:  # 绑定函数，使表头可排序(这里的command=lambda _col=col还不是太懂)
            self.tree.heading(col, text=col, command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))
 
		# 定义顶部区域
		# 定义左上方区域
        self.top_title = tk.Label(self.frame_left_top, text="仓库信息:", font=('Verdana', 15))
        self.top_title.grid(row=0, column=0, columnspan=2, sticky="NSEW", padx=40, pady=5)   # NSEW表示允许组件向4个方向都可以拉伸

		# 定义下方区域
        self.chaxun = tk.StringVar()
        self.right_bottom_gender_entry = tk.Entry(self.frame_bottom, textvariable=self.chaxun, font=('Verdana', 15))
        self.right_bottom_button = ttk.Button(self.frame_bottom, text='仓库名称查询', width=18, command=self.put_data)
        self.right_bottom_button.grid(row=0, column=0, padx=18, pady=18)  # 位置设置
        self.right_bottom_gender_entry.grid(row=0, column=1)
 
        self.left_top_frame = tk.Frame(self.frame_left_top)
        self.var_name = tk.StringVar()  
        self.var_cno = tk.StringVar()  
        self.var_size = tk.StringVar()  
        self.var_place = tk.StringVar()  

		# 商品名称
        self.right_top_id_label = tk.Label(self.frame_left_top, text="仓库号: ", font=('Verdana', 11))
        self.right_top_id_entry = tk.Entry(self.frame_left_top, textvariable=self.var_cno, font=('Verdana', 15))
        self.right_top_id_label.grid(row=1, column=0)
        self.right_top_id_entry.grid(row=1, column=1)
		# 商品价格
        self.right_top_price_label = tk.Label(self.frame_left_top, text="仓库名称", font=('Verdana', 11))
        self.right_top_price_entry = tk.Entry(self.frame_left_top, textvariable=self.var_name, font=('Verdana', 15))
        self.right_top_price_label.grid(row=2, column=0)  # 位置设置
        self.right_top_price_entry.grid(row=2, column=1)
		# 销售数量
        self.right_top_number_label = tk.Label(self.frame_left_top, text="仓库大小", font=('Verdana', 11))
        self.right_top_number_entry = tk.Entry(self.frame_left_top, textvariable=self.var_size,font=('Verdana', 15))
        self.right_top_number_label.grid(row=3, column=0)  # 位置设置
        self.right_top_number_entry.grid(row=3, column=1)
		# 用户编号
        self.right_top_yno_label = tk.Label(self.frame_left_top, text="仓库地址", font=('Verdana', 11))
        self.right_top_yno_entry = tk.Entry(self.frame_left_top, textvariable=self.var_place, font=('Verdana', 15))
        self.right_top_yno_label.grid(row=4, column=0)  # 位置设置
        self.right_top_yno_entry.grid(row=4, column=1)
 
		# 定义右上方区域
        self.right_top_title = tk.Label(self.frame_right_top, text="操作：", font=('Verdana', 17))
        self.tree.bind('<Button-1>', self.click)  # 左键获取位置(tree.bind可以绑定一系列的事件，可以搜索ttk相关参数查看)
        self.right_top_button1 = ttk.Button(self.frame_right_top, text='新建仓库信息', width=20, command=self.new_row)
        self.right_top_button2 = ttk.Button(self.frame_right_top, text='更新选中仓库信息', width=20,command=self.updata_row)
        self.right_top_button3 = ttk.Button(self.frame_right_top, text='删除选中仓库信息', width=20,command=self.del_row)

		# 右上角按钮的位置设置
        self.right_top_title.grid(row=1, column=0, pady=10)
        self.right_top_button1.grid(row=2, column=0, padx=20, pady=10)
        self.right_top_button2.grid(row=3, column=0, padx=20, pady=10)
        self.right_top_button3.grid(row=4, column=0, padx=20, pady=10)
 
		# 整体区域定位，利用了Frame和grid进行布局
        self.frame_left_top.grid(row=0, column=0, padx=2, pady=5)
        self.frame_right_top.grid(row=0, column=1, padx=30, pady=30)
        self.frame_center.grid(row=1, column=0, columnspan=2, padx=3, pady=5)
        self.frame_bottom.grid(row=2, column=0, columnspan=2)
 
		# 设置固定组件，(0)就是将组件进行了固定
        self.frame_left_top.grid_propagate(0)
        self.frame_right_top.grid_propagate(0)
        self.frame_center.grid_propagate(0)
        self.frame_bottom.grid_propagate(0)
 
        self.frame_left_top.tkraise() # 开始显示主菜单，tkraise()提高z轴的顺序（不太懂）
        self.frame_right_top.tkraise() # 开始显示主菜单
        self.frame_center.tkraise() # 开始显示主菜单
        self.frame_bottom.tkraise() # 开始显示主菜单
 
        self.window.protocol("WM_DELETE_WINDOW", self.back)  # 捕捉右上角关闭点击，执行back方法
        self.window.mainloop()  # 进入消息循环

	# 将查到的信息放到中间的表格中
    def put_data(self):
        self.delButton()	# 先将表格内的内容全部清空
        self.bottom_name=self.right_bottom_gender_entry.get()
        if self.bottom_name=='':
            for i in range(len(self.name)):  # 写入数据
                self.tree.insert('', i, values=(self.cno[i], self.name[i], self.size[i],self.place[i]))
            for col in self.columns:  # 绑定函数，使表头可排序(这里的command=lambda _col=col还不是太懂)
                self.tree.heading(col, text=col, command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))
        else:
            try:
                name_index=self.name.index(self.bottom_name)
                self.tree.insert('', name_index, values=(
                    self.cno[name_index], self.name[name_index], self.size[name_index],
                    self.place[name_index]))
                self.tree.update()
                for col in self.columns:  # 绑定函数，使表头可排序
                    self.tree.heading(col, text=col,
                                  command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))
            except:
                messagebox.showinfo('警告！', '仓库不存在！')
        
	# 清空表格中的所有信息
    def delButton(self):
        x=self.tree.get_children()
        for item in x:
            self.tree.delete(item)


	# 在表格上的点击事件，这里是作用就是一点击表格就可以将信息直接写到左上角的框框中
    def click(self, event):
        self.col = self.tree.identify_column(event.x)  # 通过tree.identify_column()函数可以直接获取到列
        self.row = self.tree.identify_row(event.y)  # 行
 
        print(self.col)
        print(self.row)
        self.row_info = self.tree.item(self.row, "values")
        self.var_name.set(self.row_info[1])
        self.var_cno.set(self.row_info[0])
        self.id1 = self.var_cno.get()
        self.var_size.set(self.row_info[2])
        self.var_place.set(self.row_info[3])
        self.right_top_id_entry = tk.Entry(self.frame_left_top, state='disabled', textvariable=self.var_name, font=('Verdana', 15))
 
	# 点击中间的表格的表头，可以将那一列进行排序
    def tree_sort_column(self, tv, col, reverse):  # Treeview、列名、排列方式
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)  # 排序方式
        for index, (val, k) in enumerate(l):  # 根据排序后索引移动
            tv.move(k, '', index)
        tv.heading(col, command=lambda: self.tree_sort_column(tv, col, not reverse))  # 重写标题，使之成为再点倒序的标题
    #添加功能
    def new_row(self):
        print(self.var_name.get())
        print(self.name)
        if str(self.var_name.get()) in self.name:
            messagebox.showinfo('警告！', '该仓库已存在！')
        else:
            if self.var_cno.get() != '' and self.var_name.get() != '' and self.var_size.get() != '' and self.var_place.get() != '' :
				#连接数据库
                db = conn()
                #获取游标、数据
                cursor = db.cursor()
                
                sql = "INSERT INTO 仓库表 \
				       VALUES ('%s', '%s', '%s', '%s')" % \
					  (self.var_cno.get(), self.var_name.get(), self.var_size.get(), self.var_place.get())  # SQL 插入语句
                try:
                    cursor.execute(sql)  # 执行sql语句
                    db.commit()  # 提交到数据库执行
                except:
                    db.rollback()  # 发生错误时回滚
                    messagebox.showinfo('警告！', '数据库连接失败！')
                    db.close()  # 关闭数据库连接
 
                self.name.append(self.var_name.get())
                self.cno.append(self.var_cno.get())
                self.size.append(self.var_size.get())
                self.place.append(self.var_plcae.get())
                self.tree.insert('', len(self.name) - 1, values=(
                self.cno[len(self.name) - 1], self.name[len(self.name) - 1], self.size[len(self.name) - 1],
                self.place[len(self.name) - 1]))
                self.tree.update()
                messagebox.showinfo('提示！', '插入成功！')
            else:
                messagebox.showinfo('警告！', '请填写仓库信息')
    #修改功能
    def updata_row(self):
        res = messagebox.askyesnocancel('警告！', '是否更新所填数据？')
        if res == True:
			#连接数据库
            db = conn()
            #获取游标、数据
            cursor = db.cursor()
            sql = "UPDATE 仓库表 SET 仓库名称 = '%s', 仓库大小 = '%s', 仓库地址 = '%s' where 仓库号 = '%s'" % (self.var_name.get(), self.var_size.get(), self.var_place.get(),self.id1)  # SQL 插入语句
            try:
                cursor.execute(sql)  # 执行sql语句
                db.commit()  # 提交到数据库执行
                messagebox.showinfo('提示！', '更新成功！')
            except:
                db.rollback()  # 发生错误时回滚
                messagebox.showinfo('警告！', '更新失败，数据库连接失败！')
            db.close()  # 关闭数据库连接

            cno_index = self.cno.index(self.row_info[0])
            self.name[cno_index] = self.var_name.get()
            self.size[cno_index] = self.var_size.get()
            self.place[cno_index] = self.var_place.get()
            self.tree.item(self.tree.selection()[0], values=(
                    self.var_cno.get(), self.var_name.get(), self.var_size.get(),
                    self.var_place.get()))  # 修改对于行信息

	# 删除功能
    def del_row(self):
        res = messagebox.askyesnocancel('警告！', '是否删除所选数据？')
        if res == True:
            print(self.row_info[0])  # 鼠标选中的名称
            print(self.tree.selection()[0])  # 行号
            print(self.tree.get_children())  # 所有行
			#连接数据库
            db = conn()
            #获取游标、数据
            cursor = db.cursor()
            sql = "delete from 仓库表 where 仓库号 = '%s'" % (self.row_info[0]) # SQL 插入语句
            try:
                cursor.execute(sql)  # 执行sql语句
                db.commit()  # 提交到数据库执行
                messagebox.showinfo('提示！', '删除成功！')
            except:
                db.rollback()  # 发生错误时回滚
                messagebox.showinfo('警告！', '删除失败，数据库连接失败！')
            db.close()  # 关闭数据库连接
 
            cno_index = self.cno.index(self.row_info[0])
            del self.cno[cno_index]
            del self.name[cno_index]
            del self.size[cno_index]
            del self.place[cno_index]
            self.tree.delete(self.tree.selection()[0])  # 删除所选行
            print(self.tree.get_children())
    

    def back(self):
        All_admin(self.window)   # 进入管理员子菜单操作界面 


#建立进货管理类
class ProcurementManage:
    def __init__(self,parent_window):
        parent_window.destroy() # 自定销毁上一个界面
        self.window = tk.Tk()  # 初始框的声明
        self.window.title('进货管理界面')
        self.window.geometry("760x637+250+15")	# 初始窗口在屏幕中的位置
        self.frame_left_top = tk.Frame(width=400, height=260)	# 指定框架，在窗口上可以显示，这里指定四个框架	
        self.frame_right_top = tk.Frame(width=250, height=250)
        self.frame_center = tk.Frame(width=740, height=270)
        self.frame_bottom = tk.Frame(width=650, height=70)
        
         # 定义下方中心列表区域
        self.columns = ("供应商编号", "验收人编号","原材料名称","原材料数量","原材料价格","进货日期","入库号")
        self.tree = ttk.Treeview(self.frame_center, show="headings", height=16, columns=self.columns)
        # 添加竖直滚动条
        self.vbar = ttk.Scrollbar(self.frame_center, orient="vertical", command=self.tree.yview)
		# 定义树形结构与滚动条
        self.tree.configure(yscrollcommand=self.vbar.set)

		# 定义id1为修改id时的暂存变量，这个是为了更新信息而设计的
        self.id1 = 0
 
		# 表格的标题
        self.tree.column("供应商编号", width=90, anchor='center')
        self.tree.column("验收人编号", width=90, anchor='center')
        self.tree.column("原材料名称", width=90, anchor='center')
        self.tree.column("原材料数量", width=90, anchor='center')
        self.tree.column("原材料价格", width=90, anchor='center')
        self.tree.column("进货日期", width=90, anchor='center')
        self.tree.column("入库号", width=90, anchor='center')
 
		# grid方法将tree和vbar进行布局
        self.tree.grid(row=0, column=0, sticky="NSEW")
        self.vbar.grid(row=0, column=1, sticky="NS")
	
		# 定义几个数组，为中间的那个大表格做一些准备
        self.gno = []
        self.yno = []
        self.name = []
        self.number = []
        self.price = []
        self.time = []
        self.warehouse=[]
        
        #连接数据库
        db = conn()
        #获取游标、数据
        cur = db.cursor()
        sql = "SELECT * FROM 进货表 "
        try:
			# 执行SQL语句
            cur.execute(sql)
			# 获取所有记录列表
            results = cur.fetchall()
            for row in results:
                self.gno.append(row[0])
                self.yno.append(row[1])
                self.name.append(row[2].encode('latin-1').decode('gbk'))
                self.number.append(row[3])
                self.price.append(row[4])
                self.time.append(row[5])
                self.warehouse.append(row[6])
        except:
            messagebox.showinfo('警告！', '数据库连接失败！')
        db.close()# 关闭数据库连接
        
        print("test***********************")
        for i in range(len(self.name)):  # 写入数据
            self.tree.insert('', i, values=(self.gno[i], self.yno[i], self.name[i],self.number[i],self.price[i],self.time[i],self.warehouse[i]))

        for col in self.columns:  # 绑定函数，使表头可排序(这里的command=lambda _col=col还不是太懂)
            self.tree.heading(col, text=col, command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))
 
		# 定义顶部区域
		# 定义左上方区域
        self.top_title = tk.Label(self.frame_left_top, text="进货单信息:", font=('Verdana', 15))
        self.top_title.grid(row=0, column=0, columnspan=2, sticky="NSEW", padx=40, pady=5)   # NSEW表示允许组件向4个方向都可以拉伸

		# 定义下方区域
        self.chaxun = tk.StringVar()
        self.right_bottom_gender_entry = tk.Entry(self.frame_bottom, textvariable=self.chaxun, font=('Verdana', 15))
        self.right_bottom_button = ttk.Button(self.frame_bottom, text='原材料名称查询', width=18, command=self.put_data)
        self.right_bottom_button.grid(row=0, column=0, padx=18, pady=18)  # 位置设置
        self.right_bottom_gender_entry.grid(row=0, column=1)
 
        self.left_top_frame = tk.Frame(self.frame_left_top)
        self.var_name = tk.StringVar()  
        self.var_price = tk.StringVar()  
        self.var_number = tk.StringVar()  
        self.var_yno = tk.StringVar()  
        self.var_gno = tk.StringVar()
        self.var_time = tk.StringVar()
        self.var_warehouse = tk.StringVar()
        
        self.right_top_id_label = tk.Label(self.frame_left_top, text="供应商编号: ", font=('Verdana', 11))
        self.right_top_id_entry = tk.Entry(self.frame_left_top, textvariable=self.var_gno, font=('Verdana', 15))
        self.right_top_id_label.grid(row=1, column=0)
        self.right_top_id_entry.grid(row=1, column=1)

        self.right_top_price_label = tk.Label(self.frame_left_top, text="验收人编号：", font=('Verdana', 11))
        self.right_top_price_entry = tk.Entry(self.frame_left_top, textvariable=self.var_yno, font=('Verdana', 15))
        self.right_top_price_label.grid(row=2, column=0)  # 位置设置
        self.right_top_price_entry.grid(row=2, column=1)

        self.right_top_number_label = tk.Label(self.frame_left_top, text="原材料名称：", font=('Verdana', 11))
        self.right_top_number_entry = tk.Entry(self.frame_left_top, textvariable=self.var_name,font=('Verdana', 15))
        self.right_top_number_label.grid(row=3, column=0)  # 位置设置
        self.right_top_number_entry.grid(row=3, column=1)

        self.right_top_yno_label = tk.Label(self.frame_left_top, text="原材料数量：", font=('Verdana', 11))
        self.right_top_yno_entry = tk.Entry(self.frame_left_top, textvariable=self.var_number, font=('Verdana', 15))
        self.right_top_yno_label.grid(row=4, column=0)  # 位置设置
        self.right_top_yno_entry.grid(row=4, column=1)

        self.right_top_gno_label = tk.Label(self.frame_left_top, text="原材料价格：", font=('Verdana', 11))
        self.right_top_gno_entry = tk.Entry(self.frame_left_top, textvariable=self.var_price, font=('Verdana', 15))
        self.right_top_gno_label.grid(row=5, column=0)  # 位置设置
        self.right_top_gno_entry.grid(row=5, column=1)

        self.right_top_saletime_label = tk.Label(self.frame_left_top, text="进货日期：", font=('Verdana', 11))
        self.right_top_saletime_entry = tk.Entry(self.frame_left_top, textvariable=self.var_time, font=('Verdana', 15))
        self.right_top_saletime_label.grid(row=6, column=0)  # 位置设置
        self.right_top_saletime_entry.grid(row=6, column=1)

        self.right_top_saletime_label = tk.Label(self.frame_left_top, text="入库号：", font=('Verdana', 11))
        self.right_top_saletime_entry = tk.Entry(self.frame_left_top, textvariable=self.var_warehouse, font=('Verdana', 15))
        self.right_top_saletime_label.grid(row=7, column=0)  # 位置设置
        self.right_top_saletime_entry.grid(row=7, column=1)
 
		# 定义右上方区域
        self.right_top_title = tk.Label(self.frame_right_top, text="操作：", font=('Verdana', 17))
        self.tree.bind('<Button-1>', self.click)  # 左键获取位置(tree.bind可以绑定一系列的事件，可以搜索ttk相关参数查看)
        self.right_top_button1 = ttk.Button(self.frame_right_top, text='新建商品信息', width=20, command=self.new_row)
        self.right_top_button2 = ttk.Button(self.frame_right_top, text='更新选中商品信息', width=20,command=self.updata_row)
        self.right_top_button3 = ttk.Button(self.frame_right_top, text='删除选中商品信息', width=20,command=self.del_row)
        self.right_top_button4 = ttk.Button(self.frame_right_top, text='提交数据', width=20,command=self.putin)

		# 右上角按钮的位置设置
        self.right_top_title.grid(row=1, column=0, pady=10)
        self.right_top_button1.grid(row=2, column=0, padx=20, pady=10)
        self.right_top_button2.grid(row=3, column=0, padx=20, pady=10)
        self.right_top_button3.grid(row=4, column=0, padx=20, pady=10)
        self.right_top_button4.grid(row=5, column=0, padx=20, pady=10)
 
		# 整体区域定位，利用了Frame和grid进行布局
        self.frame_left_top.grid(row=0, column=0, padx=2, pady=5)
        self.frame_right_top.grid(row=0, column=1, padx=30, pady=30)
        self.frame_center.grid(row=1, column=0, columnspan=2, padx=3, pady=5)
        self.frame_bottom.grid(row=2, column=0, columnspan=2)
 
		# 设置固定组件，(0)就是将组件进行了固定
        self.frame_left_top.grid_propagate(0)
        self.frame_right_top.grid_propagate(0)
        self.frame_center.grid_propagate(0)
        self.frame_bottom.grid_propagate(0)
 
        self.frame_left_top.tkraise() # 开始显示主菜单，tkraise()提高z轴的顺序（不太懂）
        self.frame_right_top.tkraise() # 开始显示主菜单
        self.frame_center.tkraise() # 开始显示主菜单
        self.frame_bottom.tkraise() # 开始显示主菜单
 
        self.window.protocol("WM_DELETE_WINDOW", self.back)  # 捕捉右上角关闭点击，执行back方法
        self.window.mainloop()  # 进入消息循环

	# 将查到的信息放到中间的表格中
    def put_data(self):
        self.delButton()	# 先将表格内的内容全部清空
        self.bottom_name=self.right_bottom_gender_entry.get()
        if self.bottom_name=='':
            for i in range(len(self.name)):  # 写入数据
                self.tree.insert('', i, values=(self.gno[i], self.yno[i], self.name[i],self.number[i],self.price[i],self.time[i],self.warehouse[i]))
            for col in self.columns:  # 绑定函数，使表头可排序(这里的command=lambda _col=col还不是太懂)
                self.tree.heading(col, text=col, command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))
        else:
            try:
                name_index=self.name.index(self.bottom_name)
                self.tree.insert('', name_index, values=(
                    self.gno[name_index], self.yno[name_index], self.name[name_index],
                    self.number[name_index],self.price[name_index],self.time[name_index],self.warehouse[name_index]))
                self.tree.update()
                for col in self.columns:  # 绑定函数，使表头可排序
                    self.tree.heading(col, text=col,
                                  command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))
            except:
                messagebox.showinfo('警告！', '原材料不存在！')
        
	# 清空表格中的所有信息
    def delButton(self):
        x=self.tree.get_children()
        for item in x:
            self.tree.delete(item)


	# 在表格上的点击事件，这里是作用就是一点击表格就可以将信息直接写到左上角的框框中
    def click(self, event):
        self.col = self.tree.identify_column(event.x)  # 通过tree.identify_column()函数可以直接获取到列
        self.row = self.tree.identify_row(event.y)  # 行
 
        print(self.col)
        print(self.row)
        self.row_info = self.tree.item(self.row, "values")
        self.var_gno.set(self.row_info[0])
        self.var_yno.set(self.row_info[1])
        self.var_name.set(self.row_info[2])
        self.id1 = self.var_name.get()
        self.var_number.set(self.row_info[3])
        self.var_price.set(self.row_info[4])
        self.var_time.set(self.row_info[5])
        self.var_warehouse.set(self.row_info[6])
        self.right_top_id_entry = tk.Entry(self.frame_left_top, state='disabled', textvariable=self.var_name, font=('Verdana', 15))
 
	# 点击中间的表格的表头，可以将那一列进行排序
    def tree_sort_column(self, tv, col, reverse):  # Treeview、列名、排列方式
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)  # 排序方式
        for index, (val, k) in enumerate(l):  # 根据排序后索引移动
            tv.move(k, '', index)
        tv.heading(col, command=lambda: self.tree_sort_column(tv, col, not reverse))  # 重写标题，使之成为再点倒序的标题
    #添加功能
    def new_row(self):
        print(self.var_name.get())
        print(self.name)
        if str(self.var_name.get()) in self.name:
            messagebox.showinfo('警告！', '该原材料已存在！')
        else:
            if self.var_name.get() != '' and self.var_price.get() != '' and self.var_number.get() != '' and self.var_yno.get() != '' and self.var_gno.get() != '' and self.var_time.get() != '' and self.var_warehouse.get() != '':
				#连接数据库
                db = conn()
                #获取游标、数据
                cursor = db.cursor()
                
                sql = "INSERT INTO 进货表 \
				       VALUES ('%s', '%s', '%s', '%s','%s','%s','%s')" % \
					  (self.var_gno.get(), self.var_yno.get(), self.var_name.get(), self.var_number.get(),self.var_price.get(),self.var_time.get(),self.var_warehouse.get())  # SQL 插入语句
                try:
                    cursor.execute(sql)  # 执行sql语句
                    db.commit()  # 提交到数据库执行
                except:
                    db.rollback()  # 发生错误时回滚
                    messagebox.showinfo('警告！', '数据库连接失败！')
                    db.close()  # 关闭数据库连接
 
                self.name.append(self.var_name.get())
                self.price.append(self.var_price.get())
                self.number.append(self.var_number.get())
                self.yno.append(self.var_yno.get())
                self.gno.append(self.var_gno.get())
                self.time.append(self.var_time.get())
                self.warehouse.append(self.var_warehouse.get())
                self.tree.insert('', len(self.name) - 1, values=(
                self.gno[len(self.name) - 1], self.yno[len(self.name) - 1], self.name[len(self.name) - 1],
                self.number[len(self.name) - 1],self.price[len(self.name) - 1],self.time[len(self.name) - 1],self.warehouse[len(self.warehouse) - 1]))
                self.tree.update()
                messagebox.showinfo('提示！', '插入成功！')
            else:
                messagebox.showinfo('警告！', '请填写商品信息')
    #修改功能
    def updata_row(self):
        res = messagebox.askyesnocancel('警告！', '是否更新所填数据？')
        if res == True:
			#连接数据库
            db = conn()
            #获取游标、数据
            cursor = db.cursor()
            sql = "UPDATE 进货表 SET 供应商编号 = '%s', 验收人编号 = '%s', 原材料数量 = '%s', 原材料价格 = '%s' ,进货日期 = '%s',入库号 = '%s' where 原材料名称 = '%s'" % (self.var_gno.get(), self.var_yno.get(), self.var_number.get(), self.var_price.get(),self.var_time.get(),self.var_warehouse.get(),self.id1)  # SQL 插入语句
            try:
                cursor.execute(sql)  # 执行sql语句
                db.commit()  # 提交到数据库执行
                messagebox.showinfo('提示！', '更新成功！')
            except:
                db.rollback()  # 发生错误时回滚
                messagebox.showinfo('警告！', '更新失败，数据库连接失败！')
            db.close()  # 关闭数据库连接

            name_index = self.name.index(self.row_info[2])
            self.gno[name_index] = self.var_gno.get()
            self.yno[name_index] = self.var_yno.get()
            self.number[name_index] = self.var_number.get()
            self.price[name_index] = self.var_price.get()
            self.time[name_index] = self.var_time.get()
            self.warehouse[name_index] = self.var_warehouse.get()

            self.tree.item(self.tree.selection()[0], values=(
                    self.var_gno.get(), self.var_yno.get(), self.var_name.get(),
                    self.var_number.get(),self.var_price.get(),self.var_time.get(),self.var_warehouse.get()))  # 修改对于行信息

	# 删除功能
    def del_row(self):
        res = messagebox.askyesnocancel('警告！', '是否删除所选数据？')
        if res == True:
            print(self.row_info[0])  # 鼠标选中的名称
            print(self.tree.selection()[0])  # 行号
            print(self.tree.get_children())  # 所有行
			#连接数据库
            db = conn()
            #获取游标、数据
            cursor = db.cursor()
            sql = "delete from 进货表 where 原材料名称 = '%s'" % (self.row_info[2]) # SQL 插入语句
            try:
                cursor.execute(sql)  # 执行sql语句
                db.commit()  # 提交到数据库执行
                messagebox.showinfo('提示！', '删除成功！')
            except:
                db.rollback()  # 发生错误时回滚
                messagebox.showinfo('警告！', '删除失败，数据库连接失败！')
            db.close()  # 关闭数据库连接
 
            name_index = self.name.index(self.row_info[2])
            print(name_index)
            del self.name[name_index]
            del self.price[name_index]
            del self.number[name_index]
            del self.yno[name_index]
            del self.gno[name_index]
            del self.time[name_index]
            del self.warehouse[name_index]
            self.tree.delete(self.tree.selection()[0])  # 删除所选行
            print(self.tree.get_children())

    #提交数据到库存表  
    def putin(self):
        res = messagebox.askyesnocancel('警告！', '是否确定提交数据？')
        if res == True:
            #连接数据库
            db = conn()
            #获取游标、数据
            cursor = db.cursor()
            sql="update 原材料库存表 set 供应商编号=j.供应商编号,原材料数量=y.原材料数量+j.原材料数量,原材料价格=j.原材料价格,进货日期=j.进货日期,仓库号=j.入库号 from 原材料库存表 as y,进货表 as j where y.原材料名称=j.原材料名称"
            sql2="update 仓库表 set 仓库大小=10000-y.原材料数量 from 原材料库存表 as y,仓库表 as c where y.仓库号=c.仓库号"
            try:
                cursor.execute(sql)  # 执行sql语句
                cursor.execute(sql2)  # 执行sql语句
                db.commit()  # 提交到数据库执行
                messagebox.showinfo('提示！', '提交成功！')
            except:
                db.rollback()  # 发生错误时回滚
                messagebox.showinfo('警告！', '提交失败，数据库连接失败！')
            db.close()  # 关闭数据库连接
                
    def back(self):
        All_admin(self.window)   # 进入管理员子菜单操作界面 


#建立供应商资料管理类
class DataManage:
    def __init__(self,parent_window):
        parent_window.destroy() # 自定销毁上一个界面
        self.window = tk.Tk()  # 初始框的声明
        self.window.title('供应商资料界面')
        self.window.geometry("760x637+250+15")	# 初始窗口在屏幕中的位置
        self.frame_left_top = tk.Frame(width=400, height=250)	# 指定框架，在窗口上可以显示，这里指定四个框架	
        self.frame_right_top = tk.Frame(width=250, height=250)
        self.frame_center = tk.Frame(width=740, height=270)
        self.frame_bottom = tk.Frame(width=650, height=70)
        
        # 定义下方中心列表区域
        self.columns = ("供应商编号", "供应商名称","供应商地址","电话","开户银行","生产商品","邮政编码")
        self.tree = ttk.Treeview(self.frame_center, show="headings", height=16, columns=self.columns)
        # 添加竖直滚动条
        self.vbar = ttk.Scrollbar(self.frame_center, orient="vertical", command=self.tree.yview)
		# 定义树形结构与滚动条
        self.tree.configure(yscrollcommand=self.vbar.set)

		# 定义id1为修改id时的暂存变量，这个是为了更新信息而设计的
        self.id1 = 0
 
		# 表格的标题
        self.tree.column("供应商编号", width=100, anchor='center')
        self.tree.column("供应商名称", width=100, anchor='center')
        self.tree.column("供应商地址", width=130, anchor='center')
        self.tree.column("电话", width=100, anchor='center')
        self.tree.column("开户银行", width=100, anchor='center')
        self.tree.column("生产商品", width=100, anchor='center')
        self.tree.column("邮政编码", width=100, anchor='center')
 
		# grid方法将tree和vbar进行布局
        self.tree.grid(row=0, column=0, sticky="NSEW")
        self.vbar.grid(row=0, column=1, sticky="NS")
	
		# 定义几个数组，为中间的那个大表格做一些准备
        self.gno = []
        self.name = []
        self.place = []
        self.phone = []
        self.bank = []
        self.commodity = []
        self.code = []
        
        #连接数据库
        db = conn()
        #获取游标、数据
        cur = db.cursor()
        sql = "SELECT * FROM 供应商表 "
        try:
			# 执行SQL语句
            cur.execute(sql)
			# 获取所有记录列表
            results = cur.fetchall()
            for row in results:
                self.gno.append(row[0])
                self.name.append(row[1].encode('latin-1').decode('gbk'))
                self.place.append(row[2].encode('latin-1').decode('gbk'))
                self.phone.append(row[3])
                self.bank.append(row[4].encode('latin-1').decode('gbk'))
                self.commodity.append(row[5].encode('latin-1').decode('gbk'))
                self.code.append(row[6])
        except:
            messagebox.showinfo('警告！', '数据库连接失败！')
        db.close()# 关闭数据库连接
        
        print("test***********************")
        for i in range(len(self.name)):  # 写入数据
            self.tree.insert('', i, values=(self.gno[i], self.name[i], self.place[i],self.phone[i],self.bank[i],self.commodity[i],self.code[i]))

        for col in self.columns:  # 绑定函数，使表头可排序(这里的command=lambda _col=col还不是太懂)
            self.tree.heading(col, text=col, command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))
 
		# 定义顶部区域
		# 定义左上方区域
        self.top_title = tk.Label(self.frame_left_top, text="供应商信息:", font=('Verdana', 15))
        self.top_title.grid(row=0, column=0, columnspan=2, sticky="NSEW", padx=40, pady=5)   # NSEW表示允许组件向4个方向都可以拉伸

		# 定义下方区域
        self.chaxun = tk.StringVar()
        self.right_bottom_gender_entry = tk.Entry(self.frame_bottom, textvariable=self.chaxun, font=('Verdana', 15))
        self.right_bottom_button = ttk.Button(self.frame_bottom, text='供应商名称查询', width=18, command=self.put_data)
        self.right_bottom_button.grid(row=0, column=0, padx=18, pady=18)  # 位置设置
        self.right_bottom_gender_entry.grid(row=0, column=1)
 
        self.left_top_frame = tk.Frame(self.frame_left_top)
        self.var_gno = tk.StringVar()  
        self.var_name = tk.StringVar()  
        self.var_place = tk.StringVar()  
        self.var_phone = tk.StringVar()  
        self.var_bank = tk.StringVar()
        self.var_commodity = tk.StringVar()
        self.var_code = tk.StringVar()
		
        self.right_top_id_label = tk.Label(self.frame_left_top, text="供应商编号: ", font=('Verdana', 11))
        self.right_top_id_entry = tk.Entry(self.frame_left_top, textvariable=self.var_gno, font=('Verdana', 15))
        self.right_top_id_label.grid(row=1, column=0)
        self.right_top_id_entry.grid(row=1, column=1)
		
        self.right_top_price_label = tk.Label(self.frame_left_top, text="供应商名称：", font=('Verdana', 11))
        self.right_top_price_entry = tk.Entry(self.frame_left_top, textvariable=self.var_name, font=('Verdana', 15))
        self.right_top_price_label.grid(row=2, column=0)  # 位置设置
        self.right_top_price_entry.grid(row=2, column=1)
		
        self.right_top_number_label = tk.Label(self.frame_left_top, text="供应商地址：", font=('Verdana', 11))
        self.right_top_number_entry = tk.Entry(self.frame_left_top, textvariable=self.var_place,font=('Verdana', 15))
        self.right_top_number_label.grid(row=3, column=0)  # 位置设置
        self.right_top_number_entry.grid(row=3, column=1)
		
        self.right_top_yno_label = tk.Label(self.frame_left_top, text="电话：", font=('Verdana', 11))
        self.right_top_yno_entry = tk.Entry(self.frame_left_top, textvariable=self.var_phone, font=('Verdana', 15))
        self.right_top_yno_label.grid(row=4, column=0)  # 位置设置
        self.right_top_yno_entry.grid(row=4, column=1)
        
        self.right_top_gno_label = tk.Label(self.frame_left_top, text="开户银行：", font=('Verdana', 11))
        self.right_top_gno_entry = tk.Entry(self.frame_left_top, textvariable=self.var_bank, font=('Verdana', 15))
        self.right_top_gno_label.grid(row=5, column=0)  # 位置设置
        self.right_top_gno_entry.grid(row=5, column=1)
        
        self.right_top_saletime_label = tk.Label(self.frame_left_top, text="生产商品：", font=('Verdana', 11))
        self.right_top_saletime_entry = tk.Entry(self.frame_left_top, textvariable=self.var_commodity, font=('Verdana', 15))
        self.right_top_saletime_label.grid(row=6, column=0)  # 位置设置
        self.right_top_saletime_entry.grid(row=6, column=1)
        
        self.right_top_saletime_label = tk.Label(self.frame_left_top, text="邮政编码：", font=('Verdana', 11))
        self.right_top_saletime_entry = tk.Entry(self.frame_left_top, textvariable=self.var_code, font=('Verdana', 15))
        self.right_top_saletime_label.grid(row=7, column=0)  # 位置设置
        self.right_top_saletime_entry.grid(row=7, column=1)
 
		# 定义右上方区域
        self.right_top_title = tk.Label(self.frame_right_top, text="操作：", font=('Verdana', 17))
        self.tree.bind('<Button-1>', self.click)  # 左键获取位置(tree.bind可以绑定一系列的事件，可以搜索ttk相关参数查看)
        self.right_top_button1 = ttk.Button(self.frame_right_top, text='新建供应商信息', width=20, command=self.new_row)
        self.right_top_button2 = ttk.Button(self.frame_right_top, text='更新选中供应商信息', width=20,command=self.updata_row)
        self.right_top_button3 = ttk.Button(self.frame_right_top, text='删除选中供应商信息', width=20,command=self.del_row)

		# 右上角按钮的位置设置
        self.right_top_title.grid(row=1, column=0, pady=10)
        self.right_top_button1.grid(row=2, column=0, padx=20, pady=10)
        self.right_top_button2.grid(row=3, column=0, padx=20, pady=10)
        self.right_top_button3.grid(row=4, column=0, padx=20, pady=10)
 
		# 整体区域定位，利用了Frame和grid进行布局
        self.frame_left_top.grid(row=0, column=0, padx=2, pady=5)
        self.frame_right_top.grid(row=0, column=1, padx=30, pady=30)
        self.frame_center.grid(row=1, column=0, columnspan=2, padx=3, pady=5)
        self.frame_bottom.grid(row=2, column=0, columnspan=2)
 
		# 设置固定组件，(0)就是将组件进行了固定
        self.frame_left_top.grid_propagate(0)
        self.frame_right_top.grid_propagate(0)
        self.frame_center.grid_propagate(0)
        self.frame_bottom.grid_propagate(0)
 
        self.frame_left_top.tkraise() # 开始显示主菜单，tkraise()提高z轴的顺序（不太懂）
        self.frame_right_top.tkraise() # 开始显示主菜单
        self.frame_center.tkraise() # 开始显示主菜单
        self.frame_bottom.tkraise() # 开始显示主菜单
 
        self.window.protocol("WM_DELETE_WINDOW", self.back)  # 捕捉右上角关闭点击，执行back方法
        self.window.mainloop()  # 进入消息循环

	# 将查到的信息放到中间的表格中
    def put_data(self):
        self.delButton()	# 先将表格内的内容全部清空
        self.bottom_name=self.right_bottom_gender_entry.get()
        if self.bottom_name=='':
            for i in range(len(self.name)):  # 写入数据
                self.tree.insert('', i, values=(self.gno[i], self.name[i], self.place[i],self.phone[i],self.bank[i],self.commodity[i],self.code[i]))
            for col in self.columns:  # 绑定函数，使表头可排序(这里的command=lambda _col=col还不是太懂)
                self.tree.heading(col, text=col, command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))
        else:
            try:
                name_index=self.name.index(self.bottom_name)
                self.tree.insert('', name_index, values=(
                    self.gno[name_index], self.name[name_index], self.place[name_index],
                    self.phone[name_index],self.bank[name_index],self.commodity[name_index]))
                self.tree.update()
                for col in self.columns:  # 绑定函数，使表头可排序
                    self.tree.heading(col, text=col,
                                  command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))
            except:
                messagebox.showinfo('警告！', '供应商不存在！')
        
	# 清空表格中的所有信息
    def delButton(self):
        x=self.tree.get_children()
        for item in x:
            self.tree.delete(item)


	# 在表格上的点击事件，这里是作用就是一点击表格就可以将信息直接写到左上角的框框中
    def click(self, event):
        self.col = self.tree.identify_column(event.x)  # 通过tree.identify_column()函数可以直接获取到列
        self.row = self.tree.identify_row(event.y)  # 行
 
        print(self.col)
        print(self.row)
        self.row_info = self.tree.item(self.row, "values")
        self.var_gno.set(self.row_info[0])
        self.id1 = self.var_gno.get()
        self.var_name.set(self.row_info[1])
        self.var_place.set(self.row_info[2])
        self.var_phone.set(self.row_info[3])
        self.var_bank.set(self.row_info[4])
        self.var_commodity.set(self.row_info[5])
        self.var_code.set(self.row_info[6])
        self.right_top_id_entry = tk.Entry(self.frame_left_top, state='disabled', textvariable=self.var_name, font=('Verdana', 15))
 
	# 点击中间的表格的表头，可以将那一列进行排序
    def tree_sort_column(self, tv, col, reverse):  # Treeview、列名、排列方式
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)  # 排序方式
        for index, (val, k) in enumerate(l):  # 根据排序后索引移动
            tv.move(k, '', index)
        tv.heading(col, command=lambda: self.tree_sort_column(tv, col, not reverse))  # 重写标题，使之成为再点倒序的标题
    #添加功能
    def new_row(self):
        print(self.var_name.get())
        print(self.name)
        if str(self.var_name.get()) in self.name:
            messagebox.showinfo('警告！', '该供应商已存在！')
        else:
            if self.var_gno.get() != '' and self.var_name.get() != '' and self.var_place.get() != '' and self.var_phone.get() != '' and self.var_bank.get() != '' and self.var_commodity.get() != '' and self.var_code.get() != '':
				#连接数据库
                db = conn()
                #获取游标、数据
                cursor = db.cursor()
                
                sql = "INSERT INTO 供应商表 \
				       VALUES ('%s', '%s', '%s', '%s','%s','%s','%s')" % \
					  (self.var_gno.get(), self.var_name.get(), self.var_place.get(), self.var_phone.get(),self.var_bank.get(),self.var_commodity.get(),self.var_code.get())  # SQL 插入语句
                try:
                    cursor.execute(sql)  # 执行sql语句
                    db.commit()  # 提交到数据库执行
                except:
                    db.rollback()  # 发生错误时回滚
                    messagebox.showinfo('警告！', '数据库连接失败！')
                    db.close()  # 关闭数据库连接
 
                self.name.append(self.var_name.get())
                self.gno.append(self.var_gno.get())
                self.place.append(self.var_place.get())
                self.phone.append(self.var_phone.get())
                self.bank.append(self.var_bank.get())
                self.commodity.append(self.var_commodity.get())
                self.code.append(self.var_code.get())
                self.tree.insert('', len(self.name) - 1, values=(
                self.gno[len(self.name) - 1], self.name[len(self.name) - 1], self.place[len(self.name) - 1],
                self.phone[len(self.name) - 1],self.bank[len(self.name) - 1],self.commodity[len(self.name) - 1],self.code[len(self.name) - 1]))
                self.tree.update()
                messagebox.showinfo('提示！', '插入成功！')
            else:
                messagebox.showinfo('警告！', '请填写供应商信息')
    #修改功能
    def updata_row(self):
        res = messagebox.askyesnocancel('警告！', '是否更新所填数据？')
        if res == True:
			#连接数据库
            db = conn()
            #获取游标、数据
            cursor = db.cursor()
            sql = "UPDATE 供应商表 SET 供应商名称 = '%s', 供应商地址 = '%s', 电话 = '%s', 开户银行 = '%s' ,生产商品 = '%s',邮政编码 = '%s' where 供应商编号 = '%s'" % (self.var_name.get(), self.var_place.get(), self.var_phone.get(), self.var_bank.get(),self.var_commodity.get(),self.var_code.get(),self.id1)  # SQL 插入语句
            try:
                cursor.execute(sql)  # 执行sql语句
                db.commit()  # 提交到数据库执行
                messagebox.showinfo('提示！', '更新成功！')
            except:
                db.rollback()  # 发生错误时回滚
                messagebox.showinfo('警告！', '更新失败，数据库连接失败！')
            db.close()  # 关闭数据库连接

            gno_index = self.gno.index(self.row_info[0])
            self.name[gno_index] = self.var_name.get()
            self.place[gno_index] = self.var_place.get()
            self.phone[gno_index] = self.var_phone.get()
            self.bank[gno_index] = self.var_bank.get()
            self.commodity[gno_index] = self.var_commodity.get()
            self.code[gno_index] = self.var_code.get()

            self.tree.item(self.tree.selection()[0], values=(
                    self.var_gno.get(), self.var_name.get(), self.var_place.get(),
                    self.var_phone.get(),self.var_bank.get(),self.var_commodity.get(),self.var_code.get()))  # 修改对于行信息

	# 删除功能
    def del_row(self):
        res = messagebox.askyesnocancel('警告！', '是否删除所选数据？')
        if res == True:
            print(self.row_info[0])  # 鼠标选中的名称
            print(self.tree.selection()[0])  # 行号
            print(self.tree.get_children())  # 所有行
			#连接数据库
            db = conn()
            #获取游标、数据
            cursor = db.cursor()
            sql = "delete from 供应商表 where 供应商编号 = '%s'" % (self.row_info[0]) # SQL 插入语句
            try:
                cursor.execute(sql)  # 执行sql语句
                db.commit()  # 提交到数据库执行
                messagebox.showinfo('提示！', '删除成功！')
            except:
                db.rollback()  # 发生错误时回滚
                messagebox.showinfo('警告！', '删除失败，数据库连接失败！')
            db.close()  # 关闭数据库连接
 
            gno_index = self.gno.index(self.row_info[0])
            del self.gno[gno_index]
            del self.name[gno_index]
            del self.place[gno_index]
            del self.phone[gno_index]
            del self.bank[gno_index]
            del self.commodity[gno_index]
            del self.code[gno_index]
            self.tree.delete(self.tree.selection()[0])  # 删除所选行
            print(self.tree.get_children())

    def back(self):
        All_admin(self.window)   # 进入管理员子菜单操作界面 


#建立系统管理类
class AuthorityManage:
    def __init__(self,parent_window):
        parent_window.destroy() # 自定销毁上一个界面
        self.window = tk.Tk()  # 初始框的声明
        self.window.title('系统管理界面')
        self.window.geometry("760x637+250+15")	# 初始窗口在屏幕中的位置
        self.frame_left_top = tk.Frame(width=400, height=300)	# 指定框架，在窗口上可以显示，这里指定四个框架	
        self.frame_right_top = tk.Frame(width=250, height=250)
        self.frame_center = tk.Frame(width=740, height=250)
        self.frame_bottom = tk.Frame(width=650, height=70)
        
        # 定义下方中心列表区域
        self.columns = ("用户编号", "姓名","性别","电话","工龄","生日日期","用户类型","管理权限","密码")
        self.tree = ttk.Treeview(self.frame_center, show="headings", height=16, columns=self.columns)
        # 添加竖直滚动条
        self.vbar = ttk.Scrollbar(self.frame_center, orient="vertical", command=self.tree.yview)
		# 定义树形结构与滚动条
        self.tree.configure(yscrollcommand=self.vbar.set)

 
		# 表格的标题
        self.tree.column("用户编号", width=80, anchor='center')
        self.tree.column("姓名", width=80, anchor='center')
        self.tree.column("性别", width=80, anchor='center')
        self.tree.column("电话", width=80, anchor='center')
        self.tree.column("工龄", width=80, anchor='center')
        self.tree.column("生日日期", width=80, anchor='center')
        self.tree.column("用户类型", width=80, anchor='center')
        self.tree.column("管理权限", width=80, anchor='center')
        self.tree.column("密码", width=80, anchor='center')
 
		# grid方法将tree和vbar进行布局
        self.tree.grid(row=0, column=0, sticky="NSEW")
        self.vbar.grid(row=0, column=1, sticky="NS")
	
		# 定义几个数组，为中间的那个大表格做一些准备
        self.yno = []
        self.name = []
        self.sex = []
        self.phone = []
        self.age = []
        self.birthday = []
        self.kind = []
        self.qx = []
        self.password = []
        self.id=0
        
        #连接数据库
        db = conn()
        #获取游标、数据
        cur = db.cursor()
        sql = "SELECT y.用户编号,姓名,性别,电话,工龄,生日日期,用户类型,管理权限,密码 FROM 用户表 as y left join 权限表 as q on y.用户编号=q.用户编号 left join 登录表 as d on y.用户编号=d.用户编号"
        try:
			# 执行SQL语句
            cur.execute(sql)
			# 获取所有记录列表
            results = cur.fetchall()
            for row in results:
                self.yno.append(row[0])
                self.name.append(row[1].encode('latin-1').decode('gbk'))
                self.sex.append(row[2].encode('latin-1').decode('gbk'))
                self.phone.append(row[3])
                self.age.append(row[4])
                self.birthday.append(row[5])
                self.kind.append(row[6].encode('latin-1').decode('gbk'))
                self.qx.append(row[7])
                self.password.append(row[8])
        except:
            messagebox.showinfo('警告！', '数据库连接失败！')
        db.close()# 关闭数据库连接
        
        print("test***********************")
        for i in range(len(self.name)):  # 写入数据
            self.tree.insert('', i, values=(self.yno[i], self.name[i], self.sex[i],self.phone[i],self.age[i],self.birthday[i],self.kind[i],self.qx[i],self.password[i]))

        for col in self.columns:  # 绑定函数，使表头可排序(这里的command=lambda _col=col还不是太懂)
            self.tree.heading(col, text=col, command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))
 
		# 定义顶部区域
		# 定义左上方区域
        self.top_title = tk.Label(self.frame_left_top, text="用户信息:", font=('Verdana', 15))
        self.top_title.grid(row=0, column=0, columnspan=2, sticky="NSEW", padx=40, pady=5)   # NSEW表示允许组件向4个方向都可以拉伸

		# 定义下方区域
        self.chaxun = tk.StringVar()
        self.right_bottom_gender_entry = tk.Entry(self.frame_bottom, textvariable=self.chaxun, font=('Verdana', 15))
        self.right_bottom_button = ttk.Button(self.frame_bottom, text='用户名称查询', width=18, command=self.put_data)
        self.right_bottom_button.grid(row=0, column=0, padx=18, pady=18)  # 位置设置
        self.right_bottom_gender_entry.grid(row=0, column=1)
 
        self.left_top_frame = tk.Frame(self.frame_left_top)
        self.var_yno = tk.StringVar()  
        self.var_name = tk.StringVar()  
        self.var_sex = tk.StringVar()  
        self.var_phone = tk.StringVar()  
        self.var_age = tk.StringVar()
        self.var_birthday = tk.StringVar()
        self.var_kind = tk.StringVar()
        self.var_qx = tk.StringVar()
        self.var_password = tk.StringVar()
        
        self.right_top_id_label = tk.Label(self.frame_left_top, text="用户编号: ", font=('Verdana', 11))
        self.right_top_id_entry = tk.Entry(self.frame_left_top, textvariable=self.var_yno, font=('Verdana', 14))
        self.right_top_id_label.grid(row=1, column=0)
        self.right_top_id_entry.grid(row=1, column=1)
		
        self.right_top_price_label = tk.Label(self.frame_left_top, text="姓名:", font=('Verdana', 11))
        self.right_top_price_entry = tk.Entry(self.frame_left_top, textvariable=self.var_name, font=('Verdana', 14))
        self.right_top_price_label.grid(row=2, column=0)  # 位置设置
        self.right_top_price_entry.grid(row=2, column=1)
		
        self.right_top_number_label = tk.Label(self.frame_left_top, text="性别:", font=('Verdana', 11))
        self.right_top_number_entry = tk.Entry(self.frame_left_top, textvariable=self.var_sex,font=('Verdana', 14))
        self.right_top_number_label.grid(row=3, column=0)  # 位置设置
        self.right_top_number_entry.grid(row=3, column=1)
		
        self.right_top_yno_label = tk.Label(self.frame_left_top, text="电话:", font=('Verdana', 11))
        self.right_top_yno_entry = tk.Entry(self.frame_left_top, textvariable=self.var_phone, font=('Verdana', 14))
        self.right_top_yno_label.grid(row=4, column=0)  # 位置设置
        self.right_top_yno_entry.grid(row=4, column=1)
        
        self.right_top_gno_label = tk.Label(self.frame_left_top, text="工龄:", font=('Verdana', 11))
        self.right_top_gno_entry = tk.Entry(self.frame_left_top, textvariable=self.var_age, font=('Verdana', 14))
        self.right_top_gno_label.grid(row=5, column=0)  # 位置设置
        self.right_top_gno_entry.grid(row=5, column=1)
        
        self.right_top_saletime_label = tk.Label(self.frame_left_top, text="生日日期:", font=('Verdana', 11))
        self.right_top_saletime_entry = tk.Entry(self.frame_left_top, textvariable=self.var_birthday, font=('Verdana', 14))
        self.right_top_saletime_label.grid(row=6, column=0)  # 位置设置
        self.right_top_saletime_entry.grid(row=6, column=1)
         
        self.right_top_saletime_label = tk.Label(self.frame_left_top, text="用户类型:", font=('Verdana', 11))
        self.right_top_saletime_entry = tk.Entry(self.frame_left_top, textvariable=self.var_kind, font=('Verdana', 14))
        self.right_top_saletime_label.grid(row=7, column=0)  # 位置设置
        self.right_top_saletime_entry.grid(row=7, column=1)
        
        self.right_top_saletime_label = tk.Label(self.frame_left_top, text="管理权限:", font=('Verdana', 11))
        self.right_top_saletime_entry = tk.Entry(self.frame_left_top, textvariable=self.var_qx, font=('Verdana', 14))
        self.right_top_saletime_label.grid(row=8, column=0)  # 位置设置
        self.right_top_saletime_entry.grid(row=8, column=1)
        
        self.right_top_saletime_label = tk.Label(self.frame_left_top, text="登录密码:", font=('Verdana', 11))
        self.right_top_saletime_entry = tk.Entry(self.frame_left_top, textvariable=self.var_password, font=('Verdana', 14))
        self.right_top_saletime_label.grid(row=9, column=0)  # 位置设置
        self.right_top_saletime_entry.grid(row=9, column=1)
 
		# 定义右上方区域
        self.right_top_title = tk.Label(self.frame_right_top, text="操作：", font=('Verdana', 17))
        self.tree.bind('<Button-1>', self.click)  # 左键获取位置(tree.bind可以绑定一系列的事件，可以搜索ttk相关参数查看)
        self.right_top_button1 = ttk.Button(self.frame_right_top, text='新建用户信息', width=20, command=self.new_row)
        self.right_top_button2 = ttk.Button(self.frame_right_top, text='更新选中用户信息', width=20,command=self.updata_row)
        self.right_top_button3 = ttk.Button(self.frame_right_top, text='删除选中用户信息', width=20,command=self.del_row)

		# 右上角按钮的位置设置
        self.right_top_title.grid(row=1, column=0, pady=10)
        self.right_top_button1.grid(row=2, column=0, padx=20, pady=10)
        self.right_top_button2.grid(row=3, column=0, padx=20, pady=10)
        self.right_top_button3.grid(row=4, column=0, padx=20, pady=10)
 
		# 整体区域定位，利用了Frame和grid进行布局
        self.frame_left_top.grid(row=0, column=0, padx=2, pady=5)
        self.frame_right_top.grid(row=0, column=1, padx=30, pady=30)
        self.frame_center.grid(row=1, column=0, columnspan=2, padx=3, pady=5)
        self.frame_bottom.grid(row=2, column=0, columnspan=2)
 
		# 设置固定组件，(0)就是将组件进行了固定
        self.frame_left_top.grid_propagate(0)
        self.frame_right_top.grid_propagate(0)
        self.frame_center.grid_propagate(0)
        self.frame_bottom.grid_propagate(0)
 
        self.frame_left_top.tkraise() # 开始显示主菜单，tkraise()提高z轴的顺序（不太懂）
        self.frame_right_top.tkraise() # 开始显示主菜单
        self.frame_center.tkraise() # 开始显示主菜单
        self.frame_bottom.tkraise() # 开始显示主菜单
 
        self.window.protocol("WM_DELETE_WINDOW", self.back)  # 捕捉右上角关闭点击，执行back方法
        self.window.mainloop()  # 进入消息循环

	# 将查到的信息放到中间的表格中
    def put_data(self):
        self.delButton()	# 先将表格内的内容全部清空
        self.bottom_name=self.right_bottom_gender_entry.get()
        if self.bottom_name=='':
            for i in range(len(self.name)):  # 写入数据
                self.tree.insert('', i, values=(self.yno[i], self.name[i], self.sex[i],self.phone[i],self.age[i],self.birthday[i],self.kind[i],self.qx[i],self.password[i]))
            for col in self.columns:  # 绑定函数，使表头可排序(这里的command=lambda _col=col还不是太懂)
                self.tree.heading(col, text=col, command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))
        else:
            try:
                name_index=self.name.index(self.bottom_name)
                self.tree.insert('', name_index, values=(
                    self.yno[name_index], self.name[name_index], self.sex[name_index],self.phone[name_index],
                    self.age[name_index],self.birthday[name_index],self.kind[name_index],self.qx[name_index],self.password[name_index]))
                self.tree.update()
                for col in self.columns:  # 绑定函数，使表头可排序
                    self.tree.heading(col, text=col,
                                  command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))
            except:
                messagebox.showinfo('警告！', '用户不存在！')
        
	# 清空表格中的所有信息
    def delButton(self):
        x=self.tree.get_children()
        for item in x:
            self.tree.delete(item)


	# 在表格上的点击事件，这里是作用就是一点击表格就可以将信息直接写到左上角的框框中
    def click(self, event):
        self.col = self.tree.identify_column(event.x)  # 通过tree.identify_column()函数可以直接获取到列
        self.row = self.tree.identify_row(event.y)  # 行
 
        print(self.col)
        print(self.row)
        self.row_info = self.tree.item(self.row, "values")
        self.var_yno.set(self.row_info[0])
        self.id=self.var_yno.get()
        self.var_name.set(self.row_info[1])
        self.var_sex.set(self.row_info[2])
        self.var_phone.set(self.row_info[3])
        self.var_age.set(self.row_info[4])
        self.var_birthday.set(self.row_info[5])
        self.var_kind.set(self.row_info[6])
        self.var_qx.set(self.row_info[7])
        self.var_password.set(self.row_info[8])
        self.right_top_id_entry = tk.Entry(self.frame_left_top, state='disabled', textvariable=self.var_name, font=('Verdana', 15))
 
	# 点击中间的表格的表头，可以将那一列进行排序
    def tree_sort_column(self, tv, col, reverse):  # Treeview、列名、排列方式
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)  # 排序方式
        for index, (val, k) in enumerate(l):  # 根据排序后索引移动
            tv.move(k, '', index)
        tv.heading(col, command=lambda: self.tree_sort_column(tv, col, not reverse))  # 重写标题，使之成为再点倒序的标题
    #添加功能
    def new_row(self):
        print(self.var_name.get())
        print(self.name)
        if str(self.var_name.get()) in self.name:
            messagebox.showinfo('警告！', '该用户已存在！')
        else:
            if self.var_yno.get() != '' and self.var_name.get() != '' and self.var_sex.get() != '' and self.var_phone.get() != '' and self.var_age.get() != '' and self.var_birthday.get() != '' and self.var_kind.get() != '' and self.var_qx.get() != '' and self.var_password.get() != '':
				#连接数据库
                db = conn()
                #获取游标、数据
                cursor = db.cursor()
                
                sql = "INSERT INTO 用户表 VALUES ('%s', '%s', '%s', '%s','%s','%s')" % \
					  (self.var_yno.get(), self.var_name.get(), self.var_sex.get(), self.var_phone.get(),self.var_age.get(),self.var_birthday.get())  # SQL 插入语句
                sql2 = "INSERT INTO 权限表 VALUES ('%s', '%s', '%s')" % \
					  (self.var_yno.get(), self.var_kind.get(), self.var_qx.get())  # SQL 插入语句
                sql3 = "INSERT INTO 登录表 VALUES ('%s', '%s')" % \
					  (self.var_yno.get(), self.var_password.get())  # SQL 插入语句
                try:
                    cursor.execute(sql)  # 执行sql语句
                    cursor.execute(sql2)  # 执行sql语句
                    cursor.execute(sql3)  # 执行sql语句
                    db.commit()  # 提交到数据库执行
                except:
                    db.rollback()  # 发生错误时回滚
                    messagebox.showinfo('警告！', '数据库连接失败！')
                    db.close()  # 关闭数据库连接
 
                self.yno.append(self.var_yno.get())
                self.name.append(self.var_name.get())
                self.sex.append(self.var_sex.get())
                self.phone.append(self.var_phone.get())
                self.age.append(self.var_age.get())
                self.birthday.append(self.var_birthday.get())
                self.kind.append(self.var_kind.get())
                self.qx.append(self.var_qx.get())
                self.password.append(self.var_password.get())
                self.tree.insert('', len(self.name) - 1, values=(
                self.yno[len(self.name) - 1], self.name[len(self.name) - 1], self.sex[len(self.name) - 1],self.phone[len(self.name) - 1],
                self.age[len(self.name) - 1],self.birthday[len(self.name) - 1],self.kind[len(self.name) - 1],self.qx[len(self.name) - 1],self.password[len(self.name) - 1]))
                self.tree.update()
                messagebox.showinfo('提示！', '插入成功！')
            else:
                messagebox.showinfo('警告！', '请填写用户信息')
    #修改功能
    def updata_row(self):
        res = messagebox.askyesnocancel('警告！', '是否更新所填数据？')
        if res == True:
			#连接数据库
            db = conn()
            #获取游标、数据
            cursor = db.cursor()
            sql = "update 用户表 set 性别='%s',电话='%s',工龄='%s',生日日期='%s' where 用户编号='%s'" % \
					  (self.var_sex.get(), self.var_phone.get(),self.var_age.get(),self.var_birthday.get(),self.id)  # SQL 插入语句
            sql2 = "update 权限表 set 用户类型='%s',管理权限='%s' where 用户编号='%s'" % \
					  (self.var_kind.get(), self.var_qx.get(),self.id)  # SQL 插入语句
            sql3 = "update 登录表 set 密码='%s' where 用户编号='%s'" % \
					  (self.var_password.get(),self.id)  # SQL 插入语句
            try:
                cursor.execute(sql)  # 执行sql语句
                cursor.execute(sql2)  # 执行sql语句
                cursor.execute(sql3)  # 执行sql语句
                db.commit()  # 提交到数据库执行
                messagebox.showinfo('提示！', '更新成功！')
            except:
                db.rollback()  # 发生错误时回滚
                messagebox.showinfo('警告！', '更新失败，数据库连接失败！')
            db.close()  # 关闭数据库连接


            yno_index = self.yno.index(self.row_info[0])
            self.sex[yno_index] = self.var_sex.get()
            self.phone[yno_index] = self.var_phone.get()
            self.age[yno_index] = self.var_age.get()
            self.birthday[yno_index] = self.var_birthday.get()
            self.kind[yno_index] = self.var_kind.get()
            self.qx[yno_index] = self.var_qx.get()
            self.password[yno_index] = self.var_password.get()

            self.tree.item(self.tree.selection()[0], values=(
                    self.var_yno.get(), self.var_name.get(), self.var_sex.get(),
                    self.var_phone.get(),self.var_age.get(),self.var_birthday.get(),self.var_kind.get(),self.var_qx.get(),self.var_password.get()))  # 修改对于行信息

	# 删除功能
    def del_row(self):
        res = messagebox.askyesnocancel('警告！', '是否删除所选数据？')
        if res == True:
            print(self.row_info[0])  # 鼠标选中的名称
            print(self.tree.selection()[0])  # 行号
            print(self.tree.get_children())  # 所有行
			#连接数据库
            db = conn()
            #获取游标、数据
            cursor = db.cursor()
            sql = "delete from 用户表 where 用户编号 = '%s'" % (self.row_info[0]) # SQL 插入语句
            sql2 = "delete from 权限表 where 用户编号 = '%s'" % (self.row_info[0]) # SQL 插入语句
            sql3 = "delete from 登录表 where 用户编号 = '%s'" % (self.row_info[0]) # SQL 插入语句
            try:
                cursor.execute(sql)  # 执行sql语句
                cursor.execute(sql2)  # 执行sql语句
                cursor.execute(sql3)  # 执行sql语句
                db.commit()  # 提交到数据库执行
                messagebox.showinfo('提示！', '删除成功！')
            except:
                db.rollback()  # 发生错误时回滚
                messagebox.showinfo('警告！', '删除失败，数据库连接失败！')
            db.close()  # 关闭数据库连接
 
            yno_index = self.yno.index(self.row_info[0])
            del self.yno[yno_index]
            del self.name[yno_index]
            del self.sex[yno_index]
            del self.phone[yno_index]
            del self.age[yno_index]
            del self.birthday[yno_index]
            del self.kind[yno_index]
            del self.qx[yno_index]
            del self.password[yno_index]
            self.tree.delete(self.tree.selection()[0])  # 删除所选行
            print(self.tree.get_children())

    def back(self):
        All_admin(self.window)   # 进入管理员子菜单操作界面 


# 购买操作界面
class BuyManage:
    def __init__(self,parent_window):
        parent_window.destroy() # 自定销毁上一个界面
        self.window = tk.Tk()  # 初始框的声明
        self.window.title('购买操作界面')
        self.window.geometry("600x500+250+15")	# 初始窗口在屏幕中的位置
        self.frame_left_top = tk.Frame(width=380, height=130)	# 指定框架，在窗口上可以显示，这里指定四个框架	
        self.frame_right_top = tk.Frame(width=250, height=130)
        self.frame_center = tk.Frame(width=600, height=250)
        self.frame_bottom = tk.Frame(width=600, height=70)
        
        # 定义下方中心列表区域
        self.columns = ("商品名称", "商品价格","商品数量")
        self.tree = ttk.Treeview(self.frame_center, show="headings", height=16, columns=self.columns)
        # 添加竖直滚动条
        self.vbar = ttk.Scrollbar(self.frame_center, orient="vertical", command=self.tree.yview)
		# 定义树形结构与滚动条
        self.tree.configure(yscrollcommand=self.vbar.set)
        
        # 表格的标题
        self.tree.column("商品名称", width=130, anchor='center')
        self.tree.column("商品价格", width=130, anchor='center')
        self.tree.column("商品数量", width=130, anchor='center')

		# grid方法将tree和vbar进行布局
        self.tree.grid(row=0, column=0, sticky="NSEW")
        self.vbar.grid(row=0, column=1, sticky="NS")
	
		# 定义几个数组，为中间的那个大表格做一些准备
        self.name = []
        self.price = []
        self.number = []
        
        #连接数据库
        db = conn()
        #获取游标、数据
        cur = db.cursor()
        sql = "SELECT * FROM 商品信息表 "
        try:
			# 执行SQL语句
            cur.execute(sql)
			# 获取所有记录列表
            results = cur.fetchall()
            for row in results:
                self.name.append(row[1].encode('latin-1').decode('gbk'))
                self.price.append(row[2])
                self.number.append(row[3])
        except:
            messagebox.showinfo('警告！', '数据库连接失败！')
            db.close()# 关闭数据库连接
        print("test***********************")
        for i in range(len(self.name)): # 写入数据
            self.tree.insert('', i, values=(self.name[i], self.price[i], self.number[i]))
        
        for col in self.columns: # 绑定函数，使表头可排序(这里的command=lambda _col=col还不是太懂)
            self.tree.heading(col, text=col, command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))
 
		# 定义顶部区域
		# 定义左上方区域
        self.top_title = tk.Label(self.frame_left_top, text="商品信息:", font=('Verdana', 15))
        self.top_title.grid(row=0, column=0, columnspan=2, sticky="NSEW", padx=40, pady=5)   # NSEW表示允许组件向4个方向都可以拉伸

		# 定义下方区域
        self.chaxun = tk.StringVar()
        self.right_bottom_gender_entry = tk.Entry(self.frame_bottom, textvariable=self.chaxun, font=('Verdana', 15))
        self.right_bottom_button = ttk.Button(self.frame_bottom, text='商品名称查询', width=18, command=self.put_data)
        self.right_bottom_button.grid(row=0, column=0, padx=18, pady=18)  # 位置设置
        self.right_bottom_gender_entry.grid(row=0, column=1)
 
        self.left_top_frame = tk.Frame(self.frame_left_top)
        self.var_name = tk.StringVar()  
        self.var_price = tk.StringVar()  
        self.var_number = tk.StringVar()  
        
		# 商品名称
        self.right_top_id_label = tk.Label(self.frame_left_top, text="商品名称: ", font=('Verdana', 11))
        self.right_top_id_entry = tk.Entry(self.frame_left_top, textvariable=self.var_name, font=('Verdana', 15))
        self.right_top_id_label.grid(row=1, column=0)
        self.right_top_id_entry.grid(row=1, column=1)
		# 商品价格
        self.right_top_price_label = tk.Label(self.frame_left_top, text="商品价格：", font=('Verdana', 11))
        self.right_top_price_entry = tk.Entry(self.frame_left_top, textvariable=self.var_price, font=('Verdana', 15))
        self.right_top_price_label.grid(row=2, column=0)  # 位置设置
        self.right_top_price_entry.grid(row=2, column=1)
		# 销售数量
        self.right_top_number_label = tk.Label(self.frame_left_top, text="购买数量：", font=('Verdana', 11))
        self.right_top_number_entry = tk.Entry(self.frame_left_top, textvariable=self.var_number,font=('Verdana', 15))
        self.right_top_number_label.grid(row=3, column=0)  # 位置设置
        self.right_top_number_entry.grid(row=3, column=1)

		# 定义右上方区域
        self.right_top_title = tk.Label(self.frame_right_top, text="购买操作：", font=('Verdana', 17))
        self.tree.bind('<Button-1>', self.click)  # 左键获取位置(tree.bind可以绑定一系列的事件，可以搜索ttk相关参数查看)
        self.right_top_button1 = ttk.Button(self.frame_right_top, text='购买商品', width=20, command=self.new_row)
        self.right_top_button2 = ttk.Button(self.frame_right_top, text='提交订单并进入付款界面', width=20, command=lambda: BuyminManage(self.window))
		# 右上角按钮的位置设置
        self.right_top_title.grid(row=1, column=0, pady=6)
        self.right_top_button1.grid(row=2, column=0, padx=17, pady=8)
        self.right_top_button2.grid(row=3, column=0, padx=17, pady=8)
		# 整体区域定位，利用了Frame和grid进行布局
        self.frame_left_top.grid(row=0, column=0, padx=2, pady=5)
        self.frame_right_top.grid(row=0, column=1, padx=30, pady=30)
        self.frame_center.grid(row=1, column=0, columnspan=2, padx=3, pady=5)
        self.frame_bottom.grid(row=2, column=0, columnspan=2)
 
		# 设置固定组件，(0)就是将组件进行了固定
        self.frame_left_top.grid_propagate(0)
        self.frame_right_top.grid_propagate(0)
        self.frame_center.grid_propagate(0)
        self.frame_bottom.grid_propagate(0)
 
        self.frame_left_top.tkraise() # 开始显示主菜单，tkraise()提高z轴的顺序（不太懂）
        self.frame_right_top.tkraise() # 开始显示主菜单
        self.frame_center.tkraise() # 开始显示主菜单
        self.frame_bottom.tkraise() # 开始显示主菜单
 
        self.window.protocol("WM_DELETE_WINDOW", self.back)  # 捕捉右上角关闭点击，执行back方法
        self.window.mainloop()  # 进入消息循环

	# 将查到的信息放到中间的表格中
    def put_data(self):
        self.delButton()	# 先将表格内的内容全部清空
        self.bottom_name=self.right_bottom_gender_entry.get()
        if self.bottom_name=='':
            for i in range(len(self.name)):  # 写入数据
                self.tree.insert('', i, values=(self.name[i], self.price[i], self.number[i]))
            for col in self.columns:  # 绑定函数，使表头可排序(这里的command=lambda _col=col还不是太懂)
                self.tree.heading(col, text=col, command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))
        else:
            try:
                name_index=self.name.index(self.bottom_name)
                self.tree.insert('', name_index, values=(
                    self.name[name_index], self.price[name_index], self.number[name_index]))
                self.tree.update()
                for col in self.columns:  # 绑定函数，使表头可排序
                    self.tree.heading(col, text=col,
                                  command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))
            except:
                messagebox.showinfo('警告！', '商品不存在！')
         
	# 清空表格中的所有信息
    def delButton(self):
        x=self.tree.get_children()
        for item in x:
            self.tree.delete(item)


	# 在表格上的点击事件，这里是作用就是一点击表格就可以将信息直接写到左上角的框框中
    def click(self, event):
        self.col = self.tree.identify_column(event.x)  # 通过tree.identify_column()函数可以直接获取到列
        self.row = self.tree.identify_row(event.y)  # 行
        
        self.row_info = self.tree.item(self.row, "values")
        self.var_name.set(self.row_info[0])
        self.var_price.set(self.row_info[1])
        self.var_number.set(self.row_info[2])
        self.right_top_id_entry = tk.Entry(self.frame_left_top, state='disabled', textvariable=self.var_name, font=('Verdana', 15))
 
	# 点击中间的表格的表头，可以将那一列进行排序
    def tree_sort_column(self, tv, col, reverse):  # Treeview、列名、排列方式
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)  # 排序方式
        for index, (val, k) in enumerate(l):  # 根据排序后索引移动
            tv.move(k, '', index)
        tv.heading(col, command=lambda: self.tree_sort_column(tv, col, not reverse))  # 重写标题，使之成为再点倒序的标题
    #添加功能
    def new_row(self):
        if self.var_name.get() != '' and self.var_price.get() != '' and self.var_number.get() != '' :
            #连接数据库
            db = conn()
            #获取游标、数据
            cursor = db.cursor()
            curr_time = datetime.datetime.now()#获取当前时间
            time_str = curr_time.strftime("%Y-%m-%d")#转化为2000-02-02形式
            sql = "INSERT INTO 商品销售表 (商品名称,商品价格,销售数量,销售时间)\
    				       VALUES ('%s', '%s', '%s','%s')" % \
    					  (self.var_name.get(), self.var_price.get(), self.var_number.get(),time_str)  # SQL 插入语句
            try:
                cursor.execute(sql)  # 执行sql语句
                db.commit()  # 提交到数据库执行
                messagebox.showinfo('提示！', '购买成功！')
            except:
                db.rollback()  # 发生错误时回滚
                messagebox.showinfo('警告！', '数据库连接失败！')
                db.close()  # 关闭数据库连接
            
        else:
            messagebox.showinfo('警告！', '请填写商品信息')
        
    def back(self):
        all_admin(self.window)   # 进入管理员子菜单操作界面 
    


# 收付款操作界面
class BuyminManage:
    def __init__(self,parent_window):
        parent_window.destroy() # 自定销毁上一个界面
        self.window = tk.Tk()  # 初始框的声明
        self.window.title('收付款操作界面')
        self.window.geometry("760x637+250+15")	# 初始窗口在屏幕中的位置
        self.frame_left_top = tk.Frame(width=400, height=270)	# 指定框架，在窗口上可以显示，这里指定四个框架	
        self.frame_right_top = tk.Frame(width=250, height=270)
        self.frame_center = tk.Frame(width=700, height=240)
        self.frame_bottom = tk.Frame(width=650, height=70)
        
        # 定义下方中心列表区域
        self.columns = ("商品名称", "商品价格","销售数量","用户编号","顾客编号","销售时间")
        self.tree = ttk.Treeview(self.frame_center, show="headings", height=16, columns=self.columns)
        # 添加竖直滚动条
        self.vbar = ttk.Scrollbar(self.frame_center, orient="vertical", command=self.tree.yview)
		# 定义树形结构与滚动条
        self.tree.configure(yscrollcommand=self.vbar.set)

		# 定义id1为修改id时的暂存变量，这个是为了更新信息而设计的
        self.id1 = 0
 
		# 表格的标题
        self.tree.column("商品名称", width=100, anchor='center')
        self.tree.column("商品价格", width=100, anchor='center')
        self.tree.column("销售数量", width=100, anchor='center')
        self.tree.column("用户编号", width=100, anchor='center')
        self.tree.column("顾客编号", width=100, anchor='center')
        self.tree.column("销售时间", width=100, anchor='center')
 
		# grid方法将tree和vbar进行布局
        self.tree.grid(row=0, column=0, sticky="NSEW")
        self.vbar.grid(row=0, column=1, sticky="NS")
	
		# 定义几个数组，为中间的那个大表格做一些准备
        self.name = []
        self.price = []
        self.number = []
        self.yno = []
        self.gno = []
        self.saletime = []       
        self.sum=0
        
        #连接数据库
        db = conn()
        #获取游标、数据
        cur = db.cursor()
        sql = "SELECT * FROM 商品销售表 "
        try:
			# 执行SQL语句
            cur.execute(sql)
			# 获取所有记录列表
            results = cur.fetchall()
            for row in results:
                self.name.append(row[0].encode('latin-1').decode('gbk'))
                self.price.append(row[1])
                self.number.append(row[2])
                self.yno.append(row[3])
                self.gno.append(row[4])
                self.saletime.append(row[5])
        except:
            messagebox.showinfo('警告！', '数据库连接失败！')
            db.close()# 关闭数据库连接
        print("test***********************")
        for i in range(len(self.name)): # 写入数据
            self.tree.insert('', i, values=(self.name[i], self.price[i], self.number[i],self.yno[i],self.gno[i],self.saletime[i]))
        
        for col in self.columns: # 绑定函数，使表头可排序(这里的command=lambda _col=col还不是太懂)
            self.tree.heading(col, text=col, command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))
 
		# 定义顶部区域
		# 定义左上方区域
        self.top_title = tk.Label(self.frame_left_top, text="商品购买信息:", font=('Verdana', 15))
        self.top_title.grid(row=0, column=0, columnspan=2, sticky="NSEW", padx=40, pady=5)   # NSEW表示允许组件向4个方向都可以拉伸

		# 定义下方区域
        self.chaxun = tk.StringVar()
        self.right_bottom_gender_entry = tk.Entry(self.frame_bottom, textvariable=self.chaxun, font=('Verdana', 15))
        self.right_bottom_button = ttk.Button(self.frame_bottom, text='商品名称查询', width=18, command=self.put_data)
        self.right_bottom_button.grid(row=0, column=0, padx=18, pady=18)  # 位置设置
        self.right_bottom_gender_entry.grid(row=0, column=1)
 
        self.left_top_frame = tk.Frame(self.frame_left_top)
        self.var_name = tk.StringVar()  
        self.var_price = tk.StringVar()  
        self.var_number = tk.StringVar()  
        self.var_yno = tk.StringVar()  
        self.var_gno = tk.StringVar()
        self.var_saletime = tk.StringVar()
        self.var_getmoney= tk.StringVar()
		# 商品名称
        self.right_top_id_label = tk.Label(self.frame_left_top, text="商品名称: ", font=('Verdana', 11))
        self.right_top_id_entry = tk.Entry(self.frame_left_top, textvariable=self.var_name, font=('Verdana', 15))
        self.right_top_id_label.grid(row=1, column=0)
        self.right_top_id_entry.grid(row=1, column=1)
		# 商品价格
        self.right_top_price_label = tk.Label(self.frame_left_top, text="商品价格：", font=('Verdana', 11))
        self.right_top_price_entry = tk.Entry(self.frame_left_top, textvariable=self.var_price, font=('Verdana', 15))
        self.right_top_price_label.grid(row=2, column=0)  # 位置设置
        self.right_top_price_entry.grid(row=2, column=1)
		# 销售数量
        self.right_top_number_label = tk.Label(self.frame_left_top, text="销售数量：", font=('Verdana', 11))
        self.right_top_number_entry = tk.Entry(self.frame_left_top, textvariable=self.var_number,font=('Verdana', 15))
        self.right_top_number_label.grid(row=3, column=0)  # 位置设置
        self.right_top_number_entry.grid(row=3, column=1)
		# 用户编号
        self.right_top_yno_label = tk.Label(self.frame_left_top, text="用户编号：", font=('Verdana', 11))
        self.right_top_yno_entry = tk.Entry(self.frame_left_top, textvariable=self.var_yno, font=('Verdana', 15))
        self.right_top_yno_label.grid(row=4, column=0)  # 位置设置
        self.right_top_yno_entry.grid(row=4, column=1)
        # 顾客编号
        self.right_top_gno_label = tk.Label(self.frame_left_top, text="顾客编号：", font=('Verdana', 11))
        self.right_top_gno_entry = tk.Entry(self.frame_left_top, textvariable=self.var_gno, font=('Verdana', 15))
        self.right_top_gno_label.grid(row=5, column=0)  # 位置设置
        self.right_top_gno_entry.grid(row=5, column=1)
        # 销售时间
        self.right_top_saletime_label = tk.Label(self.frame_left_top, text="销售时间：", font=('Verdana', 11))
        self.right_top_saletime_entry = tk.Entry(self.frame_left_top, textvariable=self.var_saletime, font=('Verdana', 15))
        self.right_top_saletime_label.grid(row=6, column=0)  # 位置设置
        self.right_top_saletime_entry.grid(row=6, column=1)
        # 总价
        self.right_top_money_label = tk.Label(self.frame_left_top, text="总价：", font=('Verdana', 11))
        self.right_top_money_label1 = tk.Label(self.frame_left_top, text='', font=('Verdana', 11))#将计算出来的总价输入到
        self.right_top_money_label.grid(row=7, column=0)  # 位置设置
        self.right_top_money_label1.grid(row=7, column=1)
        # 实收
        self.right_top_getmoney_label = tk.Label(self.frame_left_top, text="实收：", font=('Verdana', 11))
        self.right_top_getmoney_entry = tk.Entry(self.frame_left_top, textvariable=self.var_getmoney, font=('Verdana', 11))#将计算出来的总价输入到
        self.right_top_getmoney_label.grid(row=8, column=0)  # 位置设置
        self.right_top_getmoney_entry.grid(row=8, column=1)

		# 定义右上方区域
        self.right_top_title = tk.Label(self.frame_right_top, text="购买操作：", font=('Verdana', 15))
        self.tree.bind('<Button-1>', self.click)  # 左键获取位置(tree.bind可以绑定一系列的事件，可以搜索ttk相关参数查看)
        self.right_top_button1 = ttk.Button(self.frame_right_top, text='新建商品购买信息', width=17, command=self.new_row)
        self.right_top_button2 = ttk.Button(self.frame_right_top, text='更新选中商品信息', width=17,command=self.updata_row)
        self.right_top_button3 = ttk.Button(self.frame_right_top, text='删除选中商品信息', width=17,command=self.del_row)
        self.right_top_button4 = ttk.Button(self.frame_right_top, text='计算总价', width=17,command=self.pay_row)
        self.right_top_button5 = ttk.Button(self.frame_right_top, text='提交订单并打印发票', width=17,command=self.putfa_row)
        self.right_top_button6 = ttk.Button(self.frame_right_top, text='清空订单', width=17,command=self.delete_row)
		# 右上角按钮的位置设置
        self.right_top_title.grid(row=1, column=0, pady=6)
        self.right_top_button1.grid(row=2, column=0, padx=20, pady=6)
        self.right_top_button2.grid(row=3, column=0, padx=20, pady=6)
        self.right_top_button3.grid(row=4, column=0, padx=20, pady=6)
        self.right_top_button4.grid(row=5, column=0, padx=20, pady=6)
        self.right_top_button5.grid(row=6, column=0, padx=20, pady=6)
        self.right_top_button6.grid(row=7, column=0, padx=20, pady=6)
		# 整体区域定位，利用了Frame和grid进行布局
        self.frame_left_top.grid(row=0, column=0, padx=2, pady=5)
        self.frame_right_top.grid(row=0, column=1, padx=30, pady=30)
        self.frame_center.grid(row=1, column=0, columnspan=2, padx=3, pady=5)
        self.frame_bottom.grid(row=2, column=0, columnspan=2)
 
		# 设置固定组件，(0)就是将组件进行了固定
        self.frame_left_top.grid_propagate(0)
        self.frame_right_top.grid_propagate(0)
        self.frame_center.grid_propagate(0)
        self.frame_bottom.grid_propagate(0)
 
        self.frame_left_top.tkraise() # 开始显示主菜单，tkraise()提高z轴的顺序（不太懂）
        self.frame_right_top.tkraise() # 开始显示主菜单
        self.frame_center.tkraise() # 开始显示主菜单
        self.frame_bottom.tkraise() # 开始显示主菜单
 
        self.window.protocol("WM_DELETE_WINDOW", self.back)  # 捕捉右上角关闭点击，执行back方法
        self.window.mainloop()  # 进入消息循环

	# 将查到的信息放到中间的表格中
    def put_data(self):
        self.delButton()	# 先将表格内的内容全部清空
        self.bottom_name=self.right_bottom_gender_entry.get()
        if self.bottom_name=='':
            for i in range(len(self.name)):  # 写入数据
                self.tree.insert('', i, values=(self.name[i], self.price[i], self.number[i],self.yno[i],self.gno[i],self.saletime[i]))
            for col in self.columns:  # 绑定函数，使表头可排序(这里的command=lambda _col=col还不是太懂)
                self.tree.heading(col, text=col, command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))
        else:
            try:
                name_index=self.name.index(self.bottom_name)
                self.tree.insert('', name_index, values=(
                    self.name[name_index], self.price[name_index], self.number[name_index],
                    self.yno[name_index],self.gno[name_index],self.saletime[name_index]))
                self.tree.update()
                for col in self.columns:  # 绑定函数，使表头可排序
                    self.tree.heading(col, text=col,
                                  command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))
            except:
                messagebox.showinfo('警告！', '商品不存在！')
         
	# 清空表格中的所有信息
    def delButton(self):
        x=self.tree.get_children()
        for item in x:
            self.tree.delete(item)


	# 在表格上的点击事件，这里是作用就是一点击表格就可以将信息直接写到左上角的框框中
    def click(self, event):
        self.col = self.tree.identify_column(event.x)  # 通过tree.identify_column()函数可以直接获取到列
        self.row = self.tree.identify_row(event.y)  # 行
 
        print(self.col)
        print(self.row)
        self.row_info = self.tree.item(self.row, "values")
        self.var_name.set(self.row_info[0])
        self.id1 = self.var_name.get()
        self.var_price.set(self.row_info[1])
        self.var_number.set(self.row_info[2])
        self.var_yno.set(self.row_info[3])
        self.var_gno.set(self.row_info[4])
        self.var_saletime.set(self.row_info[5])
        self.right_top_id_entry = tk.Entry(self.frame_left_top, state='disabled', textvariable=self.var_name, font=('Verdana', 15))
 
	# 点击中间的表格的表头，可以将那一列进行排序
    def tree_sort_column(self, tv, col, reverse):  # Treeview、列名、排列方式
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)  # 排序方式
        for index, (val, k) in enumerate(l):  # 根据排序后索引移动
            tv.move(k, '', index)
        tv.heading(col, command=lambda: self.tree_sort_column(tv, col, not reverse))  # 重写标题，使之成为再点倒序的标题
    #添加功能
    def new_row(self):
        if self.var_name.get() != '' and self.var_price.get() != '' and self.var_number.get() != '' and self.var_yno.get() != '' and self.var_gno.get() != '' and self.var_saletime.get() != '':
            #连接数据库
            db = conn()
            #获取游标、数据
            cursor = db.cursor()
            
            sql = "INSERT INTO 商品销售表 \
    				       VALUES ('%s', '%s', '%s', '%s','%s','%s')" % \
    					  (self.var_name.get(), self.var_price.get(), self.var_number.get(), self.var_yno.get(),self.var_gno.get(),self.var_saletime.get())  # SQL 插入语句
            try:
                cursor.execute(sql)  # 执行sql语句
                db.commit()  # 提交到数据库执行
            except:
                db.rollback()  # 发生错误时回滚
                messagebox.showinfo('警告！', '数据库连接失败！')
                db.close()  # 关闭数据库连接
            
            self.name.append(self.var_name.get())
            self.price.append(self.var_price.get())
            self.number.append(self.var_number.get())
            self.yno.append(self.var_yno.get())
            self.gno.append(self.var_gno.get())
            self.saletime.append(self.var_saletime.get())
            self.tree.insert('', len(self.name) - 1, values=(
            self.name[len(self.name) - 1], self.price[len(self.name) - 1], self.number[len(self.name) - 1],
            self.yno[len(self.name) - 1],self.gno[len(self.name) - 1],self.saletime[len(self.name) - 1]))
            self.tree.update()
            messagebox.showinfo('提示！', '插入成功！')
        else:
            messagebox.showinfo('警告！', '请填写商品信息')
    #修改功能
    def updata_row(self):
        res = messagebox.askyesnocancel('警告！', '是否更新所填数据？')
        if res == True:
			#连接数据库
            db = conn()
            #获取游标、数据
            cursor = db.cursor()
            sql = "UPDATE 商品销售表 SET 商品价格 = '%s', 销售数量 = '%s', 用户编号 = '%s' ,顾客编号 = '%s',销售时间 = '%s' where 商品名称 = '%s'" % (self.var_price.get(), self.var_number.get(), self.var_yno.get(),self.var_gno.get(),self.var_saletime.get(),self.id1)  # SQL 插入语句
            try:
                cursor.execute(sql)  # 执行sql语句
                db.commit()  # 提交到数据库执行
                messagebox.showinfo('提示！', '更新成功！')
            except:
                db.rollback()  # 发生错误时回滚
                messagebox.showinfo('警告！', '更新失败，数据库连接失败！')
            db.close()  # 关闭数据库连接

            name_index = self.name.index(self.row_info[0])
            self.price[name_index] = self.var_price.get()
            self.number[name_index] = self.var_number.get()
            self.yno[name_index] = self.var_yno.get()
            self.gno[name_index] = self.var_gno.get()
            self.saletime[name_index] = self.var_saletime.get()

            self.tree.item(self.tree.selection()[0], values=(
                    self.var_name.get(), self.var_price.get(), self.var_number.get(),
                    self.var_yno.get(),self.var_gno.get(),self.var_saletime.get()))  # 修改对于行信息

	# 删除功能
    def del_row(self):
        res = messagebox.askyesnocancel('警告！', '是否删除所选数据？')
        if res == True:
            print(self.row_info[0])  # 鼠标选中的名称
            print(self.tree.selection()[0])  # 行号
            print(self.tree.get_children())  # 所有行
			#连接数据库
            db = conn()
            #获取游标、数据
            cursor = db.cursor()
            sql = "delete from 商品销售表 where 商品名称 = '%s'" % (self.row_info[0]) # SQL 插入语句
            try:
                cursor.execute(sql)  # 执行sql语句
                db.commit()  # 提交到数据库执行
                messagebox.showinfo('提示！', '删除成功！')
            except:
                db.rollback()  # 发生错误时回滚
                messagebox.showinfo('警告！', '删除失败，数据库连接失败！')
                db.close()  # 关闭数据库连接
            name_index = self.name.index(self.row_info[0])
            print(name_index)
            del self.name[name_index]
            del self.price[name_index]
            del self.number[name_index]
            del self.yno[name_index]
            del self.gno[name_index]
            del self.saletime[name_index]
            self.tree.delete(self.tree.selection()[0])  # 删除所选行
            print(self.tree.get_children())
    
    #计算购物总价钱
    def pay_row(self):
        self.sum=0
        total=[]
         #连接数据库
        db = conn()
        #获取游标、数据
        cur = db.cursor()
        sql = "SELECT 商品价格 FROM 商品销售表 "
        try:
			# 执行SQL语句
            cur.execute(sql)
			# 获取所有记录列表
            results = cur.fetchall()
            for row in results:
                total.append(row[0])
        except:
            messagebox.showinfo('警告！', '数据库连接失败！')
            db.close()# 关闭数据库连接
        for s in total:#通过计算商品数量列表与价格列表一一对应相乘累加求得总价
            self.sum=s+self.sum
        self.right_top_money_label1.config(text=self.sum)#将计算的总价输入到总价标签处

    #打印数据发票
    def putfa_row(self):
        res = messagebox.askyesnocancel('警告！', '是否确定提交订单？')
        if res == True:
            #连接数据库
            db = conn()
            #获取游标、数据
            cursor = db.cursor()
            print(self.name)
            for i in range(len(self.name)):
                sql="insert into 顾客表 (顾客编号,商品名称,购货数量,购货日期,商品价格) values('%s','%s','%s','%s','%s')" %\
                (self.gno[i],self.name[i],self.number[i],self.saletime[i],self.price[i])
                
                try:
                    cursor.execute(sql)  # 执行sql语句
                    db.commit()  # 提交到数据库执行
                except:
                    db.rollback()  # 发生错误时回滚
                    messagebox.showinfo('警告！', '提交失败，数据库连接失败！')
                    break
            try:
                sql2="update 商品库存表 set 商品数量=k.商品数量-x.销售数量 from 商品库存表 as k,商品销售表 as x where k.商品名称=x.商品名称"
                cursor.execute(sql2)  # 执行sql语句
                db.commit()  # 提交到数据库执行
                messagebox.showinfo('提示！', '提交成功！')
            except:
                db.rollback()  # 发生错误时回滚
                messagebox.showinfo('警告！', '提交失败，数据库连接失败！')
            
            db.close()  # 关闭数据库连接
            
            self.windowfa=tk.Toplevel()#创建一个子窗口
            self.windowfa.title('小票打印界面')
            self.windowfa.geometry("330x400+300+40")#始窗口在屏幕中的位置
            curr_time = datetime.datetime.now()#获取当前时间
            self.time_str = curr_time.strftime("%Y-%m-%d")#转化为2000-02-02形式
            print(self.name)
            list1=[]
            for i in range(len(self.name)):
                l=[]
                l.append(self.name[i])
                l.append(str(self.number[i]))
                l.append(str(self.price[i])) #将三个列表换成['冰箱','2','3000',...]
                list1.append(l)
            string_0=[]
            string_0.append("购物小票\n")#添加元素
            string_0.append("购买商品   购买数量   商品单价")#添加元素
            for j in list1:
                string_0.append('\t'.join(j))
            string_0.append('--------------------------------\n')
            str3="收款员工编号：%s"%(self.yno[0])
            str4="总金额：%s元"%(self.sum)
            str5="顾客付款：%s元"%(self.var_getmoney.get())
            str6="付款时间：%s"%(self.time_str)
            string_0.append(str3)
            string_0.append(str4)
            string_0.append(str5)
            string_0.append(str6)
            list3='\n'.join(string_0)#以\n换行来输出每个元素
            shuchu= tk.Label(self.windowfa, text=list3, font=('Verdana', 13))#数据以便签的形式打印在子窗口
            shuchu.place(x=40,y=50)    
            self.windowfa.mainloop()
            
    def delete_row(self):
        res = messagebox.askyesnocancel('警告！', '是否清空订单？')
        if res == True:
            #连接数据库
            db = conn()
            #获取游标、数据
            cursor = db.cursor()
            try:
                sql="delete from 商品销售表"
                cursor.execute(sql)  # 执行sql语句
                db.commit()  # 提交到数据库执行
                messagebox.showinfo('提示！', '删除成功！')
                self.delButton() #清空表格
            except:
                db.rollback()  # 发生错误时回滚
                messagebox.showinfo('警告！', '删除失败，数据库连接失败！')
            db.close()  # 关闭数据库连接
        
    def back(self):
        all_admin(self.window)   # 进入管理员子菜单操作界面 


#客户信息管理
class Dataclient:
    def __init__(self,parent_window):
        parent_window.destroy() # 自定销毁上一个界面
        self.window = tk.Tk()  # 初始框的声明
        self.window.title('顾客信息管理界面')
        self.window.geometry("760x637+250+15") # 初始窗口在屏幕中的位置
        self.frame_left_top = tk.Frame(width=400, height=260) # 指定框架，在窗口上可以显示，这里指定四个框架 
        self.frame_right_top = tk.Frame(width=250, height=250)
        self.frame_center = tk.Frame(width=740, height=270)
        self.frame_bottom = tk.Frame(width=650, height=70)
        # 定义下方中心列表区域
        self.columns = ("顾客编号", "姓名","电话","商品名称","购货数量","购货日期","商品价格")
        self.tree = ttk.Treeview(self.frame_center, show="headings", height=16, columns=self.columns)
        # 添加竖直滚动条
        self.vbar = ttk.Scrollbar(self.frame_center, orient="vertical", command=self.tree.yview)
        # 定义树形结构与滚动条
        self.tree.configure(yscrollcommand=self.vbar.set)
        
        # 表格的标题
        self.tree.column("顾客编号", width=80, anchor='center')
        self.tree.column("姓名", width=80, anchor='center')
        self.tree.column("电话", width=80, anchor='center')
        self.tree.column("商品名称", width=80, anchor='center')
        self.tree.column("购货数量", width=80, anchor='center')
        self.tree.column("购货日期", width=80, anchor='center')
        self.tree.column("商品价格", width=80, anchor='center')
        # grid方法将tree和vbar进行布局
        self.tree.grid(row=0, column=0, sticky="NSEW")
        self.vbar.grid(row=0, column=1, sticky="NS")
        # 定义几个数组，为中间的那个大表格做一些准备
        self.sno = []
        self.buyname = []
        self.phone = []
        self.number = []
        self.shopname = []
        self.buytime = []
        self.price = []
        #连接数据库
        db = conn()
        #获取游标、数据
        cur = db.cursor()
        sql = "SELECT * FROM 顾客表 "
        try:
            # 执行SQL语句
            cur.execute(sql)
            # 获取所有记录列表
            results = cur.fetchall()
            for row in results:
                self.sno.append(row[0])
                if row[1]==None:
                    self.buyname.append(row[1])
                else:
                    self.buyname.append(row[1].encode('latin-1').decode('gbk'))
                self.phone.append(row[2])
                self.number.append(row[4])
                self.shopname.append(row[3].encode('latin-1').decode('gbk'))
                self.buytime.append(row[5])
                self.price.append(row[6])
        except:
            messagebox.showinfo('警告！', '数据库连接失败！')
            db.close()# 关闭数据库连接
        print("test***********************")
        for i in range(len(self.sno)): # 写入数据
            self.tree.insert('', i, values=(self.sno[i], self.buyname[i], self.phone[i],self.shopname[i],self.number[i],self.buytime[i],self.price[i]))
        
        for col in self.columns: # 绑定函数，使表头可排序(这里的command=lambda _col=col还不是太懂)
            self.tree.heading(col, text=col, command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))
        # 定义顶部区域
        # 定义左上方区域
        self.top_title = tk.Label(self.frame_left_top, text="顾客信息:", font=('Verdana', 15))
        self.top_title.grid(row=0, column=0, columnspan=2, sticky="NSEW", padx=40, pady=5) # NSEW表示允许组件向4个方向都可以拉伸
        
        # 定义下方区域
        self.chaxun = tk.StringVar()
        self.right_bottom_gender_entry = tk.Entry(self.frame_bottom, textvariable=self.chaxun, font=('Verdana', 15))
        self.right_bottom_button = ttk.Button(self.frame_bottom, text='顾客名字查询', width=18, command=self.put_data)
        self.right_bottom_button.grid(row=0, column=0, padx=18, pady=18) # 位置设置
        self.right_bottom_gender_entry.grid(row=0, column=1)
        self.left_top_frame = tk.Frame(self.frame_left_top)
        self.var_sno = tk.StringVar() 
        self.var_buyname = tk.StringVar() 
        self.var_phone = tk.StringVar() 
        self.var_number = tk.StringVar() 
        self.var_shopname = tk.StringVar()
        self.var_buytime = tk.StringVar()
        self.var_price = tk.StringVar()
        # 顾客编号
        self.right_top_id_label = tk.Label(self.frame_left_top, text="顾客编号: ", font=('Verdana', 11))
        self.right_top_id_entry = tk.Entry(self.frame_left_top, textvariable=self.var_sno, font=('Verdana', 14))
        self.right_top_id_label.grid(row=1, column=0)
        self.right_top_id_entry.grid(row=1, column=1)
        # 姓名
        self.right_top_price_label = tk.Label(self.frame_left_top, text="姓名：", font=('Verdana', 11))
        self.right_top_price_entry = tk.Entry(self.frame_left_top, textvariable=self.var_buyname, font=('Verdana', 14))
        self.right_top_price_label.grid(row=2, column=0) # 位置设置
        self.right_top_price_entry.grid(row=2, column=1)
        # 电话
        self.right_top_number_label = tk.Label(self.frame_left_top, text="电话：", font=('Verdana', 11))
        self.right_top_number_entry = tk.Entry(self.frame_left_top, textvariable=self.var_phone,font=('Verdana', 14))
        self.right_top_number_label.grid(row=3, column=0) # 位置设置
        self.right_top_number_entry.grid(row=3, column=1)
        # 商品名称
        self.right_top_yno_label = tk.Label(self.frame_left_top, text="商品名称：", font=('Verdana', 11))
        self.right_top_yno_entry = tk.Entry(self.frame_left_top, textvariable=self.var_shopname, font=('Verdana', 14))
        self.right_top_yno_label.grid(row=4, column=0) # 位置设置
        self.right_top_yno_entry.grid(row=4, column=1)
        # 购货数量
        self.right_top_gno_label = tk.Label(self.frame_left_top, text="购货数量：", font=('Verdana', 11))
        self.right_top_gno_entry = tk.Entry(self.frame_left_top, textvariable=self.var_number, font=('Verdana', 14))
        self.right_top_gno_label.grid(row=5, column=0) # 位置设置
        self.right_top_gno_entry.grid(row=5, column=1)
        # 购货日期
        self.right_top_saletime_label = tk.Label(self.frame_left_top, text="购货日期：", font=('Verdana', 11))
        self.right_top_saletime_entry = tk.Entry(self.frame_left_top, textvariable=self.var_buytime, font=('Verdana', 14))
        self.right_top_saletime_label.grid(row=6, column=0) # 位置设置
        self.right_top_saletime_entry.grid(row=6, column=1)
        # 商品价格
        self.right_top_saletime_label = tk.Label(self.frame_left_top, text="商品价格：", font=('Verdana', 11))
        self.right_top_saletime_entry = tk.Entry(self.frame_left_top, textvariable=self.var_price, font=('Verdana', 14))
        self.right_top_saletime_label.grid(row=7, column=0) # 位置设置
        self.right_top_saletime_entry.grid(row=7, column=1)

        # 定义右上方区域
        self.right_top_title = tk.Label(self.frame_right_top, text="操作：", font=('Verdana', 17))
        self.tree.bind('<Button-1>', self.click) # 左键获取位置(tree.bind可以绑定一系列的事件，可以搜索ttk相关参数查看)
        self.right_top_button1 = ttk.Button(self.frame_right_top, text='新建顾客信息', width=20, command=self.new_row)
        self.right_top_button2 = ttk.Button(self.frame_right_top, text='更新选中顾客信息', width=20,command=self.updata_row)
        self.right_top_button3 = ttk.Button(self.frame_right_top, text='删除选中顾客信息', width=20,command=self.del_row)
        self.right_top_button4 = ttk.Button(self.frame_right_top, text='清空顾客信息', width=20,command=self.delete_row)
        
        # 右上角按钮的位置设置
        self.right_top_title.grid(row=1, column=0, pady=10)
        self.right_top_button1.grid(row=2, column=0, padx=20, pady=10)
        self.right_top_button2.grid(row=3, column=0, padx=20, pady=10)
        self.right_top_button3.grid(row=4, column=0, padx=20, pady=10)
        self.right_top_button4.grid(row=4, column=0, padx=20, pady=10)
        # 整体区域定位，利用了Frame和grid进行布局
        self.frame_left_top.grid(row=0, column=0, padx=2, pady=5)
        self.frame_right_top.grid(row=0, column=1, padx=30, pady=30)
        self.frame_center.grid(row=1, column=0, columnspan=2, padx=3, pady=5)
        self.frame_bottom.grid(row=2, column=0, columnspan=2)
        # 设置固定组件，(0)就是将组件进行了固定
        self.frame_left_top.grid_propagate(0)
        self.frame_right_top.grid_propagate(0)
        self.frame_center.grid_propagate(0)
        self.frame_bottom.grid_propagate(0)
        self.frame_left_top.tkraise() # 开始显示主菜单，tkraise()提高z轴的顺序（不太懂）
        self.frame_right_top.tkraise() # 开始显示主菜单
        self.frame_center.tkraise() # 开始显示主菜单
        self.frame_bottom.tkraise() # 开始显示主菜单
        self.window.protocol("WM_DELETE_WINDOW", self.back) # 捕捉右上角关闭点击，执行back方法
        self.window.mainloop() # 进入消息循环
        
    # 将查到的信息放到中间的表格中
    def put_data(self):
        self.delButton() # 先将表格内的内容全部清空
        self.bottom_name=self.right_bottom_gender_entry.get()
        if self.bottom_name=='':
            for i in range(len(self.buyname)): # 写入数据
                self.tree.insert('', i, values=(self.sno[i], self.buyname[i],self.phone[i],self.shopname[i],self.number[i],self.buytime[i],self.price[i]))
            for col in self.columns: # 绑定函数，使表头可排序(这里的command=lambda _col=col还不是太懂)
                self.tree.heading(col, text=col, command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))
        else:
            try:
                name_index=self.buyname.index(self.bottom_name)
                self.tree.insert('', name_index, values=(
                self.sno[name_index], self.buyname[name_index], self.phone[name_index],
                self.number[name_index],self.shopname[name_index],self.buytime[name_index],self.price[name_index]))
                self.tree.update()
                for col in self.columns: # 绑定函数，使表头可排序
                    self.tree.heading(col, text=col,
                                      command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))
            except:
                messagebox.showinfo('警告！', '顾客不存在！')
    # 清空表格中的所有信息
    def delButton(self):
        x=self.tree.get_children()
        for item in x:
            self.tree.delete(item)
        
    # 在表格上的点击事件，这里是作用就是一点击表格就可以将信息直接写到左上角的框框中
    def click(self, event):
        self.col = self.tree.identify_column(event.x) # 通过tree.identify_column()函数可以直接获取到列
        self.row = self.tree.identify_row(event.y) # 行
        print(self.col)
        print(self.row)
        self.row_info = self.tree.item(self.row, "values")
        self.var_sno.set(self.row_info[0])
        self.var_buyname.set(self.row_info[1])
        self.var_phone.set(self.row_info[2])
        self.var_number.set(self.row_info[4])
        self.var_shopname.set(self.row_info[3])
        self.var_buytime.set(self.row_info[5])
        self.var_price.set(self.row_info[6])
        self.right_top_id_entry = tk.Entry(self.frame_left_top, state='disabled', textvariable=self.var_buyname, font=('Verdana', 15))
    # 点击中间的表格的表头，可以将那一列进行排序
    def tree_sort_column(self, tv, col, reverse): # Treeview、列名、排列方式
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse) # 排序方式
        for index, (val, k) in enumerate(l): # 根据排序后索引移动
            tv.move(k, '', index)
            tv.heading(col, command=lambda: self.tree_sort_column(tv, col, not reverse)) # 重写标题，使之成为再点倒序的标题
    #添加功能
    def new_row(self):
        print(self.var_buyname.get())
        if str(self.var_buyname.get()) in self.buyname:
            messagebox.showinfo('警告！', '该顾客已存在！')
        else:
            if self.var_sno.get() != '' and self.var_buyname.get() != '' and self.var_phone.get() != '' and self.var_shopname.get() != '' and self.var_number.get() != '' and self.var_buytime.get() != '' and self.var_price.get() != '' :
                #连接数据库
                db = conn()
                #获取游标、数据
                cursor = db.cursor()
                sql = "INSERT INTO 顾客表 \
                VALUES ('%s', '%s', '%s', '%s','%s','%s','%s')" % \
                (self.var_sno.get(), self.var_buyname.get(), self.var_phone.get(),self.var_shopname.get(), self.var_number.get(),self.var_buytime.get(),self.var_price.get()) # SQL 插入语句
                try:
                    cursor.execute(sql) # 执行sql语句
                    db.commit() # 提交到数据库执行
                except:
                    db.rollback() # 发生错误时回滚
                    messagebox.showinfo('警告！', '数据库连接失败！')
                    db.close() # 关闭数据库连接
                self.sno.append(self.var_sno.get())
                self.buyname.append(self.var_buyname.get())
                self.phone.append(self.var_phone.get())
                self.number.append(self.var_number.get())
                self.shopname.append(self.var_shopname.get())
                self.buytime.append(self.var_buytime.get())
                self.price.append(self.var_price.get())
                self.tree.insert('', len(self.buyname) - 1, values=(
                self.sno[len(self.buyname) - 1], self.buyname[len(self.buyname) - 1], self.phone[len(self.buyname) - 1],
                self.shopname[len(self.buyname) - 1],self.number[len(self.buyname) - 1],self.buytime[len(self.buyname) - 1],self.price[len(self.buyname) - 1]))
                self.tree.update()
                messagebox.showinfo('提示！', '插入成功！')
            else:
                messagebox.showinfo('警告！', '请填写顾客信息')
    #修改功能
    def updata_row(self):
        res = messagebox.askyesnocancel('警告！', '是否更新所填数据？')
        if res == True:
            #连接数据库
            db = conn()
            #获取游标、数据
            cursor = db.cursor()
            sql = "UPDATE 顾客表 SET 姓名 = '%s', 电话 = '%s' ,商品名称 = '%s',购货数量 = '%s' ,购货日期 = '%s' ,商品价格 = '%s' where 顾客编号 = '%s'" % (self.var_buyname.get(), self.var_phone.get(), self.var_shopname.get(), self.var_number.get(),self.var_buytime.get(),self.var_price.get(),self.var_sno.get()) # SQL 插入语句
            try:
                cursor.execute(sql) # 执行sql语句
                db.commit() # 提交到数据库执行
                messagebox.showinfo('提示！', '更新成功！')
            except:
                db.rollback() # 发生错误时回滚
                messagebox.showinfo('警告！', '更新失败，数据库连接失败！')
                db.close() # 关闭数据库连接
        
        sno_index = self.sno.index(self.row_info[0])
        self.buyname[sno_index] = self.var_buyname.get()
        self.number[sno_index] = self.var_number.get()
        self.price[sno_index] = self.var_price.get()
        self.buytime[sno_index] = self.var_buytime.get()
        self.shopname[sno_index] = self.var_shopname.get()
        self.phone[sno_index] = self.var_phone.get()
        
        self.tree.item(self.tree.selection()[0], values=(
        self.var_sno.get(), self.var_buyname.get(), self.var_phone.get(),
        self.var_shopname.get(),self.var_number.get(),self.var_buytime.get(),self.var_price.get())) # 修改对于行信息
        
    # 删除功能
    def del_row(self):
        res = messagebox.askyesnocancel('警告！', '是否删除所选数据？')
        if res == True:
            print(self.row_info[0]) # 鼠标选中的名称
            print(self.tree.selection()[0]) # 行号
            print(self.tree.get_children()) # 所有行
            #连接数据库
            db = conn()
            #获取游标、数据
            cursor = db.cursor()
            sql = "delete from 顾客表 where 顾客编号 = '%s'" % (self.row_info[0]) # SQL 插入语句
            try:
                cursor.execute(sql) # 执行sql语句
                db.commit() # 提交到数据库执行
                messagebox.showinfo('提示！', '删除成功！')
            except:
                db.rollback() # 发生错误时回滚
                messagebox.showinfo('警告！', '删除失败，数据库连接失败！')
                db.close() # 关闭数据库连接
            sno_index = self.sno.index(self.row_info[0])
            print(sno_index)
            del self.sno[sno_index]
            del self.buyname[sno_index]
            del self.phone[sno_index]
            del self.shopname[sno_index]
            del self.number[sno_index]
            del self.buytime[sno_index]
            del self.price[sno_index]
            self.tree.delete(self.tree.selection()[0]) # 删除所选行
            print(self.tree.get_children())
            
    def delete_row(self):
        res = messagebox.askyesnocancel('警告！', '是否清空订单？')
        if res == True:
            #连接数据库
            db = conn()
            #获取游标、数据
            cursor = db.cursor()
            try:
                sql="delete from 顾客表"
                cursor.execute(sql)  # 执行sql语句
                db.commit()  # 提交到数据库执行
                messagebox.showinfo('提示！', '删除成功！')
                self.delButton() #清空表格
            except:
                db.rollback()  # 发生错误时回滚
                messagebox.showinfo('警告！', '删除失败，数据库连接失败！')
            db.close()  # 关闭数据库连接
        
    def back(self):
        all_admin(self.window) # 进入员工子菜单操作界面 

if __name__ == '__main__':
	# 实例化Application
	window = tk.Tk()
	AdminPage(window)
