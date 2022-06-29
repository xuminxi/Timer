import math
import time
import tkinter as tk


class Timer(object):
    def __init__(self):
        # 设置窗体
        self.window = tk.Tk()
        self.set_window()

        # 设置画布
        self.canvas = tk.Canvas(self.window, width=360, height=360)
        self.canvas.pack()

        # 设置按钮
        self.set_button()
        self.start_flag = False

        # 设置时钟
        self.set_clock()

        #初始化
        self.dif = 0

        # 设置数字秒表
        self.time_string = tk.StringVar()
        tk.Label(self.window, textvariable=self.time_string, font=("Times New Roman", 20), fg='red').place(x=130, y=210)

        # 初始化为0
        self.time_string.set('00:00:00')
        self.canvas.create_line(180, 160, 180, 54, fill="#000000", width=3)
        self.start_time = 0
        self.timer = None
        self.p1, self.p2 = [], []

        # 初始化指针角度
        self.theta0, self.theta1 = -math.pi / 2, -math.pi / 2

    def set_window(self):
        self.window.title('tk')
        self.window.geometry('360x360')
        self.window.resizable(False, False)

    def set_button(self):
        tk.Button(self.window, text="复位", command=self.reset).place(x=95, y=320)
        tk.Button(self.window, text="启动", command=self.start).place(x=230, y=320)
        tk.Button(self.window, text="暂停", command=self.stop).place(x=165, y=320)

    def set_clock(self):
        # 绘制中心的小圆
        self.canvas.create_oval(175, 160, 185, 170, width=2)

        # 绘制12条较长的线
        length = 16
        theta = 0
        r, cx, cy = 130, 180, 165
        start_x, start_y = r + cx, cy
        for i in range(12):
            end_x, end_y = start_x + length * math.cos(theta), start_y + length * math.sin(theta)
            self.canvas.create_line(start_x, start_y, end_x, end_y, fill="#000000", width=3)
            theta += math.pi / 6
            start_x = cx + r * math.cos(theta)
            start_y = cy + r * math.sin(theta)

        # 绘制48条较短的线
        length = 8
        theta = 0
        r, cx, cy = 138, 180, 165
        start_x, start_y = r + cx, cy
        for i in range(60):
            end_x, end_y = start_x + length * math.cos(theta), start_y + length * math.sin(theta)
            self.canvas.create_line(start_x, start_y, end_x, end_y, fill="#000000", width=3)
            theta += math.pi / 30
            start_x = cx + r * math.cos(theta)
            start_y = cy + r * math.sin(theta)

        # 绘制文字
        theta = -math.pi / 3
        r, cx, cy = 120, 180, 165
        start_x = cx + r * math.cos(theta)
        start_y = cy + r * math.sin(theta)
        for i in range(5, 65, 5):
            self.canvas.create_text(start_x, start_y, text=str(i), font=("Times New Roman", 11))
            theta += math.pi / 6
            start_x = cx + r * math.cos(theta)
            start_y = cy + r * math.sin(theta)

    def reset(self):
        self.start_flag = False
        self.window.after_cancel(self.timer)
        self.time_string.set('00:00:00')
        self.dif = 0
        self.start_time = 0
        self.theta0, self.theta1 = -math.pi / 2, -math.pi / 2

        self.canvas.create_line(self.p1[0], self.p1[1], self.p2[0], self.p2[1], fill="#F0F0F0", width=3)
        self.canvas.create_line(180, 160, 180, 54, fill="#000000", width=3)

    def start(self):
        if not self.start_flag:
            self.start_flag = True
            self.start_time = time.time()
            self.origin_time = time.time()
            self.update()

    def stop(self):
        if self.dif :
            #confirm if it is runing,if running, stop timer
            if self.start_flag == True:
                self.start_flag = False
                self.stop_time = time.time()
            #otherwise, start timer
            else:
                self.start_flag = True
                self.update()
        else:
            pass

    def update(self):
        #confirm if it is required to be runnning,
        if self.start_flag ==True:
            self.dif = self.origin_time - self.start_time

            # 计算数字时间字符串以及指针转动角度
            if self.dif  < 1:
                self.dif  = int(self.dif  * 100)
                self.theta0 = self.theta1
                self.theta1 = -math.pi / 2 + self.dif  / 50 * math.pi
                if self.dif  < 10:
                    self.dif = "0" + str(self.dif )
                time_str = '00:00:{}'.format(self.dif)

            elif 1 <= self.dif  < 60:
                second = int(self.dif )
                ten_mil = int((self.dif  - second) * 1000 // 10)
                self.theta0 = self.theta1
                self.theta1 = -math.pi / 2 + ten_mil / 50 * math.pi
                if second < 10:
                    second = "0" + str(second)
                if ten_mil < 10:
                    ten_mil = "0" + str(ten_mil)
                time_str = '00:{}:{}'.format(second, ten_mil)

            elif 60 <= self.dif  < 3600:
                minute = int(self.dif  // 60)
                second = int(self.dif  - minute * 60)
                ten_mil = int((self.dif  - minute * 60 - second) * 1000 // 10)
                self.theta0 = self.theta1
                self.theta1 = -math.pi / 2 + ten_mil / 50 * math.pi

                if minute < 10:
                    minute = "0" + str(minute)
                if second < 10:
                    second = "0" + str(second)
                if ten_mil < 10:
                    ten_mil = "0" + str(ten_mil)
                time_str = '{}:{}:{}'.format(minute, second, ten_mil)

            else:
                time_str = '99:99:99'
                self.theta0 = self.theta1
                self.theta1 = -math.pi / 2
            self.time_string.set(time_str)

            # 绘制指针
            length = 105
            r, cx, cy = 6, 180, 165
            start_x = [cx + r * math.cos(self.theta0), cx + r * math.cos(self.theta1)]
            start_y = [cy + r * math.sin(self.theta0), cy + r * math.sin(self.theta1)]
            end_x = [start_x[0] + length * math.cos(self.theta0), start_x[1] + length * math.cos(self.theta1)]
            end_y = [start_y[0] + length * math.sin(self.theta0), start_y[1] + length * math.sin(self.theta1)]

            self.p1, self.p2 = [start_x[1], start_y[1]], [end_x[1], end_y[1]]

            # 先用白线把上一条线盖住
            self.canvas.create_line(start_x[0], start_y[0], end_x[0], end_y[0], fill="#F0F0F0", width=3)
            # 绘制新的指针
            self.canvas.create_line(start_x[1], start_y[1], end_x[1], end_y[1], fill="#000000", width=3)

            #since we update the str every 0.02s, we need to accumulate 0.02s everytime, meanwhile , it will be record when it is running
            self.origin_time+=0.02
            self.timer = self.window.after(20, self.update)


    def run(self):
        self.window.mainloop()


if __name__ == '__main__':
    timer = Timer()
    timer.run()
