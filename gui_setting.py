# -*- coding: utf-8 -*-
"""
形态学操作就是改变物体的形状，如腐蚀使物体"变瘦"，膨胀使物体"变胖"
先腐蚀后膨胀会分离物体，所以叫开运算，常用来去除小区域物体
先膨胀后腐蚀会消除物体内的小洞，所以叫闭运算
img_path = asksaveasfilename(initialdir = file_path,
                      filetypes=[("jpg格式","jpg"), ("png格式","png"), ("bmp格式","bmp")],
                      parent = self.root,
                      title = '保存图片')
"""
import tkinter.messagebox as messagebox
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
from tkinter.filedialog import askopenfilename, asksaveasfilename
import cv2
import numpy as np
import time

file_path = os.path.dirname(__file__)
WIN_WIDTH = 700
WIN_HEIGHT = 400

class Image_sys():
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('700x400+80+80')
        self.root.title('图像技术实践大作业')  # 设置窗口标题
        # self.root.iconbitmap('icon/icon.ico')  # 设置窗口图标
        # 调用方法会禁止根窗体改变大小
        self.root.resizable(True, True)

        menubar = tk.Menu(self.root)  # 创建主菜单栏 (Menu)
        self.root.config(menu=menubar)

        self.save_image = None

        # 创建文件下拉菜单
        # 文件菜单下 tearoff=0 表示有没有分隔符，默认为有分隔符
        file_menu = tk.Menu(menubar, tearoff=0)
        # 为顶级菜单实例添加菜单，并级联相应的子菜单实例
        menubar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="导入图像文件", command=self.open_file)
        file_menu.add_command(label="保存生成图像文件",command=self.save_file)
        file_menu.add_command(label="清除生成图像", command=self.recover)
        file_menu.add_command(label="清除所有文件", command=self.clear)
        file_menu.add_command(label="退出程序", command=self.exit_sys)

        # 形态学
        morph_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="形态学", menu=morph_menu)
        morph_menu.add_command(label="腐蚀", command=self.mor_corrosion)
        morph_menu.add_command(label="膨胀", command=self.mor_expand)
        morph_menu.add_command(label="开运算", command=self.mor_open_operation)
        morph_menu.add_command(label="闭运算", command=self.mor_close_operation)

        # 缩放
        scale_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="缩放", menu=scale_menu)
        scale_menu.add_command(label="放大PyrUp", command=self.scale_pyrup)
        scale_menu.add_command(label="缩小PyrDown", command=self.scale_pyrdown)
        scale_menu.add_command(label="放大Resize", command=self.scale_zoom_in)
        scale_menu.add_command(label="缩小Resize", command=self.scale_zoom_out)

        # 滤波
        filter_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="滤波", menu=filter_menu)
        filter_menu.add_command(label="均值", command=self.filter_mean)
        filter_menu.add_command(label="中值", command=self.filter_mid_value)
        filter_menu.add_command(label="方框", command=self.filter_box)
        filter_menu.add_command(label="高斯", command=self.filter_gauss)
        filter_menu.add_command(label="双边", command=self.filter_bilateral)

        # 帮助
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="帮助", menu=help_menu)
        help_menu.add_command(label="版权", command=self.help_copyright)
        help_menu.add_command(label="关于", command=self.help_about)

        # 创建一个容器,其父容器为self.root
        self.frame_scr = ttk.LabelFrame(self.root, text="Scour image:")
        # padx  pady   该容器外围需要留出的空余空间
        self.frame_scr.place(x=80, y=30, width=250, height=250)

        # 创建一个容器,其父容器为self.root
        self.frame_des = ttk.LabelFrame(self.root, text="Destination image:")
        # padx  pady   该容器外围需要留出的空余空间
        self.frame_des.place(x=370, y=30, width=250, height=250)

        # 创建两个label
        label_scr = ttk.Label(self.root, text='源图像', font=25, foreground='blue', anchor='center')
        label_scr.place(x=150, y=280, width=100, height=50)

        label_des = ttk.Label(self.root, text='目标图像', font=25, foreground='blue', anchor='center')
        label_des.place(x=450, y=280, width=100, height=50)

        self.label_scr_image = None
        self.label_des_image = None
        self.path = ''
        self.frame_scale=None
        self.root.mainloop()

    def open_file(self):
        # 打开文件对话框
        open_img_path = askopenfilename(initialdir=file_path,
                                        filetypes=[("jpg格式", "jpg"), ("png格式", "png"), ("bmp格式", "bmp")],
                                        parent=self.root,
                                        title='导入图像文件')
        if (open_img_path == ''):
            return
        else:
            if (self.label_des_image != None):
                self.label_des_image.pack_forget()  # 隐藏控件
                self.label_des_image = None
            self.path = open_img_path
            image = Image.open(self.path)
            image=Image.Image.resize(image,(250,250))
            tk_image = ImageTk.PhotoImage(image)
            if (self.label_scr_image == None):
                self.label_scr_image = tk.Label(self.frame_scr, image=tk_image)
            self.label_scr_image.configure(image=tk_image)
            self.label_scr_image.pack()  # 显示控件
            self.root.mainloop()

    def save_file(self):
        save_img_path = asksaveasfilename(initialdir=file_path,
                                     filetypes=[("jpg格式", "jpg"), ("png格式", "png"), ("bmp格式", "bmp")],
                                     parent=self.root,
                                     title='保存图像文件')
        if (save_img_path==''):
            return
        else:
            if (self.save_image is not None):
                pil_image=Image.fromarray(self.save_image)
                pil_image.save(save_img_path+'.jpg')
            else:
                tk.messagebox.showinfo(title='warning',message='还没有对图片进行处理,无法保存！')

    def recover(self):
        if (self.path == ''):
            return
        if (self.label_des_image == None):
            return
        self.label_des_image.pack_forget()
        self.label_des_image = None
        self.save_image = None

    def clear(self):
        if (self.label_scr_image != None):
            self.label_scr_image.pack_forget()  # 隐藏控件
            self.label_scr_image = None
            self.save_image=None
            self.path = ''
        if (self.label_des_image != None):
            self.label_des_image.pack_forget()  # 隐藏控件
            self.label_des_image = None
            self.save_image = None
            self.path = ''

    def exit_sys(self):
        quit_root = messagebox.askokcancel('提示', '真的要退出么!~')
        if (quit_root == True):
            self.root.destroy()
        return

    def mor_corrosion(self):
        if (self.path == ''):
            return
        if (self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)  # 读取图片
        image = cv2.resize(image, (250, 250))
        b, g, r = cv2.split(image)  # 三通道分离
        image = cv2.merge([r, g, b])  # 三通道合并
        # kernel = np.ones((5, 5), np.uint8)# 指定核大小
        # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))  # 矩形结构
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))  # 椭圆结构
        # kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 5))  # 十字形结构

        if self.frame_scale is None:
            self.frame_scale = ttk.Label(self.root)
            self.frame_scale.place(x=190, y=330)
        else:
            for tool in self.frame_scale.winfo_children():
                tool.destroy()
            self.frame_scale.destroy()
            self.frame_scale=ttk.Label(self.root)
            self.frame_scale.place(x=190,y=330)
        l = tk.Label(self.frame_scale, fg='black', width=20, text='you have not choose now')
        l.pack()

        def set_iteration(v):
            l.config(text='you have iter ' + v)
            img_erosion = cv2.erode(image, kernel, iterations=int(v))  # 腐蚀
            self.save_image=img_erosion
            image_pil_erosion = Image.fromarray(img_erosion)
            tk_image = ImageTk.PhotoImage(image_pil_erosion)
            if (self.label_des_image == None):
                self.label_des_image = tk.Label(self.frame_des, image=tk_image)
            self.label_des_image.configure(image=tk_image)
            self.label_des_image.pack()
            self.frame_des.mainloop()

        #设置滑动条
        s = tk.Scale(self.frame_scale, from_=0, to=20, orient=tk.HORIZONTAL, length=300, resolution=1, command=set_iteration)
        s.pack()
        self.root.mainloop()

    # 膨胀
    def mor_expand(self):
        if (self.path == ''):
            return
        if (self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)  # 读取图片
        image = cv2.resize(image, (250, 250))
        b, g, r = cv2.split(image)  # 三通道分离
        image = cv2.merge([r, g, b])  # 三通道合并
        # kernel = np.ones((5, 5), np.uint8)# 指定核大小
        # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))  # 矩形结构
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))  # 椭圆结构
        # kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 5))  # 十字形结构

        if self.frame_scale is None:
            self.frame_scale = ttk.Label(self.root)
            self.frame_scale.place(x=190, y=330)
        else:
            for tool in self.frame_scale.winfo_children():
                tool.destroy()
            self.frame_scale.destroy()
            self.frame_scale=ttk.Label(self.root)
            self.frame_scale.place(x=190,y=330)
        l = tk.Label(self.frame_scale, fg='black', width=20, text='you have not choose now')
        l.pack()
        def set_iteration(v):
            l.config(text='you have iter ' + v)
            img_dilation = cv2.dilate(image, kernel,iterations=int(v))  # 膨胀
            self.save_image =img_dilation
            image_pil_dilation = Image.fromarray(img_dilation)
            tk_image = ImageTk.PhotoImage(image_pil_dilation)
            if (self.label_des_image == None):
                self.label_des_image = tk.Label(self.frame_des, image=tk_image)
            self.label_des_image.configure(image=tk_image)
            self.label_des_image.pack()
            self.frame_des.mainloop()
        #设置滑动条
        s = tk.Scale(self.frame_scale, from_=0, to=20, orient=tk.HORIZONTAL, length=300, resolution=1, command=set_iteration)
        s.pack()
        self.root.mainloop()
        # 开运算

    def mor_open_operation(self):
        if (self.path == ''):
            return
        if (self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)  # 读取图片
        image = cv2.resize(image, (250, 250))
        b, g, r = cv2.split(image)  # 三通道分离
        image = cv2.merge([r, g, b])  # 三通道合并
        # kernel = np.ones((5, 5), np.uint8)# 指定核大小
        # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))  # 矩形结构
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))  # 椭圆结构
        # kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 5))  # 十字形结构

        if self.frame_scale is None:
            self.frame_scale = ttk.Label(self.root)
            self.frame_scale.place(x=190, y=330)
        else:
            for tool in self.frame_scale.winfo_children():
                tool.destroy()
            self.frame_scale.destroy()
            self.frame_scale=ttk.Label(self.root)
            self.frame_scale.place(x=190,y=330)
        l = tk.Label(self.frame_scale, fg='black', width=20, text='you have not choose now')
        l.pack()
        def set_iteration(v):
            l.config(text='you have iter ' + v)
            img_open_operation = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)  # 开运算
            self.save_image =img_open_operation
            image_pil_open = Image.fromarray(img_open_operation)
            tk_image = ImageTk.PhotoImage(image_pil_open)
            if (self.label_des_image == None):
                self.label_des_image = tk.Label(self.frame_des, image=tk_image)
            self.label_des_image.configure(image=tk_image)
            self.label_des_image.pack()
            self.frame_des.mainloop()
        #设置滑动条
        s = tk.Scale(self.frame_scale, from_=0, to=20, orient=tk.HORIZONTAL, length=300, resolution=1, command=set_iteration)
        s.pack()
        self.root.mainloop()
        # 闭运算

    def mor_close_operation(self):
        if (self.path == ''):
            return
        if (self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)  # 读取图片
        image = cv2.resize(image, (250, 250))
        b, g, r = cv2.split(image)  # 三通道分离
        image = cv2.merge([r, g, b])  # 三通道合并
        # kernel = np.ones((5, 5), np.uint8)# 指定核大小
        # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))  # 矩形结构
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))  # 椭圆结构
        # kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 5))  # 十字形结构

        if self.frame_scale is None:
            self.frame_scale = ttk.Label(self.root)
            self.frame_scale.place(x=190, y=330)
        else:
            for tool in self.frame_scale.winfo_children():
                tool.destroy()
            self.frame_scale.destroy()
            self.frame_scale=ttk.Label(self.root)
            self.frame_scale.place(x=190,y=330)
        l = tk.Label(self.frame_scale, fg='black', width=20, text='you have not choose now')
        l.pack()
        def set_iteration(v):
            l.config(text='you have iter ' + v)
            img_close_operation = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)  # 闭运算
            self.save_image =img_close_operation
            image_pil_close = Image.fromarray(img_close_operation)
            tk_image = ImageTk.PhotoImage(image_pil_close)
            if (self.label_des_image == None):
                self.label_des_image = tk.Label(self.frame_des, image=tk_image)
            self.label_des_image.configure(image=tk_image)
            self.label_des_image.pack()
            self.frame_des.mainloop()
        #设置滑动条
        s = tk.Scale(self.frame_scale, from_=0, to=20, orient=tk.HORIZONTAL, length=300, resolution=1, command=set_iteration)
        s.pack()
        self.root.mainloop()

    '''
    常见噪声有椒盐噪声和高斯噪声，椒盐噪声可以理解为斑点，随机出现在图像中的黑点或白点；
    高斯噪声可以理解为拍摄图片时由于光照等原因造成的噪声；这样解释并不准确，只要能简单分辨即可。
    '''

    # 均值滤波
    def filter_mean(self):
        if (self.path == ''):
            return
        if (self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)  # 读取图片
        image = cv2.resize(image, (250, 250))
        b, g, r = cv2.split(image)  # 三通道分离
        image = cv2.merge([r, g, b])  # 三通道合并

        def printentry():
            size=int(var.get())
            img_mean = cv2.blur(image, (size, size))  # 均值滤波
            self.save_image =img_mean
            image_pil_mean = Image.fromarray(img_mean)
            tk_image = ImageTk.PhotoImage(image_pil_mean)
            if (self.label_des_image == None):
                self.label_des_image = tk.Label(self.frame_des, image=tk_image)
            self.label_des_image.configure(image=tk_image)
            self.label_des_image.pack()
            self.frame_des.mainloop()

        if self.frame_scale is None:
            self.frame_scale = ttk.Label(self.root)
            self.frame_scale.place(x=190, y=330)
        else:
            for tool in self.frame_scale.winfo_children():
                tool.destroy()
            self.frame_scale.destroy()
            self.frame_scale=ttk.Label(self.root)
            self.frame_scale.place(x=270,y=330)

        var=tk.StringVar()
        e=tk.Entry(self.frame_scale,textvariable=var)
        e.pack()# 设置输入框对应的文本变量为var
        e.insert(0,'请输入滤波的大小')
        tk.Button(self.frame_scale, text="进行滤波",command=printentry).pack()
        self.frame_scale.mainloop()
        self.root.mainloop()

    # 方框滤波方框滤波跟均值滤波很像，当可选参数normalize为True的时候，方框滤波就是均值滤波，
    # 如3×3的核，a就等于1/9；normalize为False的时候，a=1，相当于求区域内的像素和。
    def filter_box(self):
        if (self.path == ''):
            return
        if (self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)  # 读取图片
        image = cv2.resize(image, (250, 250))
        b, g, r = cv2.split(image)  # 三通道分离
        image = cv2.merge([r, g, b])  # 三通道合并

        if self.frame_scale is None:
            self.frame_scale = ttk.Label(self.root)
            self.frame_scale.place(x=190, y=330)
        else:
            for tool in self.frame_scale.winfo_children():
                tool.destroy()
            self.frame_scale.destroy()
            self.frame_scale=ttk.Label(self.root)
            self.frame_scale.place(x=270,y=330)

        def printentry():
            size=int(var.get())
            norm=var.get()
            if norm=="是":
                img_box = cv2.boxFilter(image, -1, (size, size), normalize=False)  # 方框滤波
                self.save_image =img_box
                image_pil_box = Image.fromarray(img_box)
                tk_image = ImageTk.PhotoImage(image_pil_box)
                if (self.label_des_image == None):
                    self.label_des_image = tk.Label(self.frame_des, image=tk_image)
                self.label_des_image.configure(image=tk_image)
                self.label_des_image.pack()
                self.frame_des.mainloop()
            else:
                img_box = cv2.boxFilter(image, -1, (size, size), normalize=True)  # 方框滤波
                self.save_image = img_box
                image_pil_box = Image.fromarray(img_box)
                tk_image = ImageTk.PhotoImage(image_pil_box)
                if (self.label_des_image == None):
                    self.label_des_image = tk.Label(self.frame_des, image=tk_image)
                self.label_des_image.configure(image=tk_image)
                self.label_des_image.pack()
                self.frame_des.mainloop()

        var=tk.StringVar()
        var1=tk.StringVar()
        e=tk.Entry(self.frame_scale,textvariable=var) # 设置输入框对应的文本变量为var
        e.pack()
        e.insert(0,'请输入滤波的大小')
        d=tk.Entry(self.frame_scale, textvariable=var1)
        d.pack()
        d.insert(0,'请输入是或否norm')
        tk.Button(self.frame_scale, text="进行滤波",command=printentry).pack()
        self.frame_scale.mainloop()
        self.root.mainloop()

    # 高斯滤波与两种滤波方式，卷积核内的每个值都一样，相当于图像区域中每个像素的权重也就一样。
    # 高斯滤波的卷积核权重并不相同，中间像素点权重最高，越远离中心的像素权重越小。
    # 高斯滤波相比均值滤波效率要慢，但可以有效消除高斯噪声，能保留更多的图像细节，所以经常被称为最有用的滤波器。
    def filter_gauss(self):
        if (self.path == ''):
            return
        if (self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)  # 读取图片
        image = cv2.resize(image, (250, 250))
        b, g, r = cv2.split(image)  # 三通道分离
        image = cv2.merge([r, g, b])  # 三通道合并

        if self.frame_scale is None:
            self.frame_scale = ttk.Label(self.root)
            self.frame_scale.place(x=190, y=330)
        else:
            for tool in self.frame_scale.winfo_children():
                tool.destroy()
            self.frame_scale.destroy()
            self.frame_scale=ttk.Label(self.root)
            self.frame_scale.place(x=270,y=330)
        def printentry():
            size=int(var.get())
            o=int(var.get())
            img_gauss = cv2.GaussianBlur(image, (size,size), o)  # 方框滤波
            self.save_image = img_gauss
            image_pil_gauss = Image.fromarray(img_gauss)
            tk_image = ImageTk.PhotoImage(image_pil_gauss)
            if (self.label_des_image == None):
                self.label_des_image = tk.Label(self.frame_des, image=tk_image)
            self.label_des_image.configure(image=tk_image)
            self.label_des_image.pack()
            self.frame_des.mainloop()

        var=tk.StringVar()
        var1=tk.StringVar()
        e=tk.Entry(self.frame_scale,textvariable=var) # 设置输入框对应的文本变量为var
        e.pack()
        e.insert(0,'请输入滤波的大小')
        d=tk.Entry(self.frame_scale, textvariable=var1)
        d.pack()
        d.insert(0,'请输入sigma的值')
        tk.Button(self.frame_scale, text="进行滤波",command=printentry).pack()
        self.frame_scale.mainloop()
        self.root.mainloop()

    # 中值滤波，中值又叫中位数，是所有值排序后取中间的值。
    # 中值滤波就是用区域内的中值来代替本像素值，所以那种孤立的斑点，
    # 如0或255很容易消除掉，适用于去除椒盐噪声和斑点噪声。中值是一种非线性操作，效率相比前面几种线性滤波要慢。
    # 斑点噪声图，用中值滤波显然更好：
    def filter_mid_value(self):
        if (self.path == ''):
            return
        if (self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)  # 读取图片
        image = cv2.resize(image, (250, 250))
        b, g, r = cv2.split(image)  # 三通道分离
        image = cv2.merge([r, g, b])  # 三通道合并

        if self.frame_scale is None:
            self.frame_scale = ttk.Label(self.root)
            self.frame_scale.place(x=190, y=330)
        else:
            for tool in self.frame_scale.winfo_children():
                tool.destroy()
            self.frame_scale.destroy()
            self.frame_scale=ttk.Label(self.root)
            self.frame_scale.place(x=270,y=330)

        def printentry():
            size=int(var.get())
            img_mid_value = cv2.medianBlur(image, size)  # 中值滤波
            self.save_image = img_mid_value
            image_pil_mid_value = Image.fromarray(img_mid_value)
            tk_image = ImageTk.PhotoImage(image_pil_mid_value)
            if (self.label_des_image == None):
                self.label_des_image = tk.Label(self.frame_des, image=tk_image)
            self.label_des_image.configure(image=tk_image)
            self.label_des_image.pack()
            self.frame_des.mainloop()
        var=tk.StringVar()
        e=tk.Entry(self.frame_scale,textvariable=var)
        e.pack()# 设置输入框对应的文本变量为var
        e.insert(0,'请输入均值的大小')
        tk.Button(self.frame_scale, text="进行滤波",command=printentry).pack()
        self.frame_scale.mainloop()
        self.root.mainloop()

    # 双边滤波，模糊操作基本都会损失掉图像细节信息，尤其前面介绍的线性滤波器，图像的边缘信息很难保留下来。
    # 然而，边缘edge信息是图像中很重要的一个特征，所以这才有了双边滤波。
    def filter_bilateral(self):
        if (self.path == ''):
            return
        if (self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)  # 读取图片
        image = cv2.resize(image, (250, 250))
        b, g, r = cv2.split(image)  # 三通道分离
        image = cv2.merge([r, g, b])  # 三通道合并

        if self.frame_scale is None:
            self.frame_scale = ttk.Label(self.root)
            self.frame_scale.place(x=190, y=330)
        else:
            for tool in self.frame_scale.winfo_children():
                tool.destroy()
            self.frame_scale.destroy()
            self.frame_scale=ttk.Label(self.root)
            self.frame_scale.place(x=270,y=330)

        def printentry():
            size=int(var.get())
            sigmaColor=int(var1.get())
            sigmaSpace=int(var2.get())
            img_bilateral = cv2.bilateralFilter(image, size, sigmaColor, sigmaSpace)  # 双边滤波
            self.save_image = img_bilateral
            image_pil_bilateral = Image.fromarray(img_bilateral)
            tk_image = ImageTk.PhotoImage(image_pil_bilateral)
            if (self.label_des_image == None):
                self.label_des_image = tk.Label(self.frame_des, image=tk_image)
            self.label_des_image.configure(image=tk_image)
            self.label_des_image.pack()
            self.frame_des.mainloop()
        var=tk.StringVar()
        var1=tk.StringVar()
        var2 = tk.StringVar()
        e=tk.Entry(self.frame_scale,textvariable=var) # 设置输入框对应的文本变量为var
        e.pack()
        e.insert(0,'请输入直径的大小')
        d=tk.Entry(self.frame_scale, textvariable=var1)
        d.pack()
        d.insert(0,'请输入sigmaColor的值')
        k=tk.Entry(self.frame_scale, textvariable=var2)
        k.pack()
        k.insert(0,'请输入sigmaSpace的值')
        tk.Button(self.frame_scale, text="进行滤波",command=printentry).pack()
        self.frame_scale.mainloop()
        self.root.mainloop()

    # 图像金字塔操作的将是图像的像素问题（图像变清晰了还是模糊了）
    # 图像金字塔主要有两类：高斯金字塔和拉普拉斯金字塔。
    def scale_pyrup(self):
        if (self.path == ''):
            return
        if (self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)  # 读取图片
        image = cv2.resize(image, (250, 250))
        b, g, r = cv2.split(image)  # 三通道分离
        image = cv2.merge([r, g, b])  # 三通道合并
        if self.frame_scale is None:
            pass
        else:
            for tool in self.frame_scale.winfo_children():
                tool.destroy()
            self.frame_scale.destroy()
        img_pyrup = cv2.pyrUp(image)  # 高斯金字塔
        self.save_image=img_pyrup
        image_pil_pyrup = Image.fromarray(img_pyrup)
        tk_image = ImageTk.PhotoImage(image_pil_pyrup)
        if (self.label_des_image == None):
            self.label_des_image = tk.Label(self.frame_des, image=tk_image)
        self.label_des_image.configure(image=tk_image)
        self.label_des_image.pack()
        self.root.mainloop()

    def scale_pyrdown(self):
        if (self.path == ''):
            return
        if (self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)  # 读取图片
        image = cv2.resize(image, (250, 250))
        b, g, r = cv2.split(image)  # 三通道分离
        image = cv2.merge([r, g, b])  # 三通道合并
        if self.frame_scale is None:
            pass
        else:
            for tool in self.frame_scale.winfo_children():
                tool.destroy()
            self.frame_scale.destroy()
        img_pyrdown = cv2.pyrDown(image)  # 高斯金字塔
        self.save_image = img_pyrdown
        image_pil_pyrdown = Image.fromarray(img_pyrdown)
        tk_image = ImageTk.PhotoImage(image_pil_pyrdown)
        if (self.label_des_image == None):
            self.label_des_image = tk.Label(self.frame_des, image=tk_image)
        self.label_des_image.configure(image=tk_image)
        # self.label_des_image.place(relx=0,rely=0)# 放置组件的不同方式
        self.label_des_image.pack()
        self.root.mainloop()

    def scale_zoom_in(self):
        if (self.path == ''):
            return
        if (self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)  # 读取图片
        image = cv2.resize(image, (250, 250))
        b, g, r = cv2.split(image)  # 三通道分离
        image = cv2.merge([r, g, b])  # 三通道合并
        def printentry():
            size=int(var.get())
            img_zoom_in = cv2.resize(image, (size,size))  # 放大
            self.save_image = img_zoom_in
            image_pil_zoom_in = Image.fromarray(img_zoom_in)
            tk_image = ImageTk.PhotoImage(image_pil_zoom_in)
            if (self.label_des_image == None):
                self.label_des_image = tk.Label(self.frame_des, image=tk_image)
            self.label_des_image.configure(image=tk_image)
            self.label_des_image.place(x=0, y=0)  # 放置组件的不同方式与金字塔放大相比对齐方式不同显示不同
            # self.label_des_image.pack()
            self.frame_des.mainloop()

        if self.frame_scale is None:
            self.frame_scale = ttk.Label(self.root)
            self.frame_scale.place(x=270, y=330)
        else:
            for tool in self.frame_scale.winfo_children():
                tool.destroy()
            self.frame_scale.destroy()
            self.frame_scale=ttk.Label(self.root)
            self.frame_scale.place(x=270,y=330)

        var=tk.StringVar()
        e=tk.Entry(self.frame_scale,textvariable=var)
        e.pack()# 设置输入框对应的文本变量为var
        e.insert(0,'请输入想放大的大小,原大小250')
        tk.Button(self.frame_scale, text="进行放大",command=printentry).pack()
        self.frame_scale.mainloop()
        self.root.mainloop()

    def scale_zoom_out(self):
        if (self.path == ''):
            return
        if (self.label_scr_image == None):
            return
        image = cv2.imdecode(np.fromfile(self.path, dtype=np.uint8), 1)  # 读取图片
        image = cv2.resize(image, (250, 250))
        b, g, r = cv2.split(image)  # 三通道分离
        image = cv2.merge([r, g, b])  # 三通道合并
        def printentry():
            size=int(var.get())
            img_zoom_in = cv2.resize(image, (size,size))  # 放大
            self.save_image = img_zoom_in
            image_pil_zoom_in = Image.fromarray(img_zoom_in)
            tk_image = ImageTk.PhotoImage(image_pil_zoom_in)
            if (self.label_des_image == None):
                self.label_des_image = tk.Label(self.frame_des, image=tk_image)
            self.label_des_image.configure(image=tk_image)
            self.label_des_image.place(x=0, y=0)  # 放置组件的不同方式与金字塔放大相比对齐方式不同显示不同
            # self.label_des_image.pack()
            self.frame_des.mainloop()

        if self.frame_scale is None:
            self.frame_scale = ttk.Label(self.root)
            self.frame_scale.place(x=270, y=330)
        else:
            for tool in self.frame_scale.winfo_children():
                tool.destroy()
            self.frame_scale.destroy()
            self.frame_scale=ttk.Label(self.root)
            self.frame_scale.place(x=270,y=330)

        var=tk.StringVar()
        e=tk.Entry(self.frame_scale,textvariable=var)
        e.pack()# 设置输入框对应的文本变量为var
        e.insert(0,'请输入想缩小的大小,原大小250')
        tk.Button(self.frame_scale, text="进行缩小",command=printentry).pack()
        self.frame_scale.mainloop()
        self.root.mainloop()

    def help_copyright(self):
        tk.messagebox.showinfo(title='版权', message='图像处理大作业~')

    def help_about(self):
        tk.messagebox.showinfo(title='关于', message='图像处理系统！~')


if __name__ == '__main__':
    Image_sys()