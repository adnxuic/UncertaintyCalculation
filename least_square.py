from tkinter import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib import rcParams
import matplotlib
from scipy.interpolate import splrep, splev
from tkinter import filedialog
from tabulate import tabulate
import wcwidth

matplotlib.use('TKAgg')  # 设置后端为TkAgg


#  图像类
class Picture:
    def __init__(self, input_data=pd.DataFrame()):
        self.x_name = ''  # x轴名称
        self.y_name = ''  # y轴名称
        self.title_name = ''  # 图片标题
        self.scatter_name = ''  # 散点图例名字
        self.formulate = ''  # 公式表达式
        self.titlelocx = 0.5  # 标题x坐标
        self.titlelocy = 0.05  # 标题y坐标
        self.formulalocx = 0.6  # 公式x坐标
        self.formulalocy = 0.9  # 公式y坐标
        self.legendloc = 'upper left'  # 图例位置
        self.fontsize = 5  # 字体大小
        self.background = 'none'  # 是否透明背景

        self.input_data = input_data  # 初始化一个空数据框,储存输入结果
        self.x = np.array([])  # x轴数据
        self.y = np.array([])  # y轴数据

    def picture_init(self):
        self.x_name = input("请输入x轴名称：")
        self.y_name = input("请输入y轴名称：")
        self.title_name = input("请输入图片标题：")
        self.scatter_name = input("请输入散点图例名字：")
        self.formulate = input("请输入公式表达式：")

    def picture_show(self, save=False, save_path=''):
        pass

    def title_setting(self):
        input_x = input("请输入标题x坐标（0-1）：")
        input_y = input("请输入标题y坐标（0-1）：")
        self.titlelocx = float(input_x)
        self.titlelocy = float(input_y)
        self.picture_show()

    def func_location(self):
        input_x = input("请输入公式x坐标（0-1）：")
        input_y = input("请输入公式y坐标（0-1）：")
        self.formulalocx = float(input_x)
        self.formulalocy = float(input_y)
        self.picture_show()

    def legend_setting(self):
        legend_loc_dict_show = {
            '1': 'best(自动选择最佳位置)',  # 自动选择最佳位置
            '2': 'upper right(右上角)',  # 右上角
            '3': 'upper left(左上角)',  # 左上角
            '4': 'lower left(左下角)',  # 左下角
            '5': 'lower right(右下角)',  # 右下角
            '6': 'right(右侧)',  # 右侧
            '7': 'center left(左侧)',  # 左侧
            '8': 'center right(右侧)',  # 右侧
            '9': 'lower center(下方)',  # 下方
            '10': 'upper center(上方)',  # 上方
            '11': 'center(中间)'  # 中间
        }

        legend_loc_dict = {
            '1': 'best',  # 自动选择最佳位置
            '2': 'upper right',  # 右上角
            '3': 'upper left',  # 左上角
            '4': 'lower left',  # 左下角
            '5': 'lower right',  # 右下角
            '6': 'right',  # 右侧
            '7': 'center left',  # 左侧
            '8': 'center right',  # 右侧
            '9': 'lower center',  # 下方
            '10': 'upper center',  # 上方
            '11': 'center'  # 中间
        }

        # 打印出所有的图例位置选项
        for key, value in legend_loc_dict_show.items():
            print(f"{key}: {value}")

        # 让用户输入一个数字来选择图例的位置
        legend_loc_num = input("请输入图例位置的数字：")
        self.legendloc = legend_loc_dict[legend_loc_num]
        self.picture_show()

    # 字体大小设置
    def font_size(self):
        input_x = input("请输入字体大小：")
        self.fontsize = int(input_x)
        self.picture_show()

    # 透明背景设置
    def background_setting(self):
        self.background = 'yes'
        print("透明背景设置成功")

    # 保存图片
    def save_picture(self, root, picture_name=''):
        root.destroy()

        # 选择保存名
        filename = input("请输入保存文件名(不需要后缀)(如果留空，默认文件名为：" + picture_name + "，直接按回车就行)：")
        if filename == "":
            filename = picture_name + '.png'
        else:
            filename += '.xlsx'
        # 实例化
        root2 = Tk()
        root2.geometry("500x500")
        root2.withdraw()
        # 获取文件夹路径
        f_path = filedialog.askdirectory()
        if f_path == "":
            print("未选择文件")
            root2.destroy()
            return self.picture_setting()
        root2.destroy()

        self.picture_show(save=True, save_path=f_path + '/' + filename)
        print('文件的保存路径为：' + f_path + '/' + filename)

        self.picture_setting()

    def picture_setting(self):
        def goto(num):
            root.destroy()
            if num == 1:
                self.title_setting()
                return self.picture_setting()
            elif num == 2:
                self.func_location()
                return self.picture_setting()
            elif num == 3:
                self.legend_setting()
                return self.picture_setting()
            elif num == 4:
                self.font_size()
                return self.picture_setting()
            elif num == 5:
                self.background_setting()
                return self.picture_setting()

        root = Tk()
        root.title('图片调整')
        root.geometry('300x300+888+444')
        butmain1 = Button(root, text="标题位置调整", command=lambda: goto(1))
        butmain1.pack(pady=5)
        butmain2 = Button(root, text="公式位置调整", command=lambda: goto(2))
        butmain2.pack(pady=5)
        butmain3 = Button(root, text="图例位置调整", command=lambda: goto(3))
        butmain3.pack(pady=5)
        butmain4 = Button(root, text="字体大小", command=lambda: goto(4))
        butmain4.pack(pady=5)
        butmain5 = Button(root, text="透明背景设置", command=lambda: goto(5))
        butmain5.pack(pady=5)
        butmain6 = Button(root, text="保存图片", command=lambda: self.save_picture(root))
        butmain6.pack(pady=5)

        root.mainloop()


#  最小二乘法图像拟合类
class LeastSquarePicture(Picture):
    def __init__(self, input_data=pd.DataFrame()):
        super().__init__(input_data)
        self.k = 0
        self.b = 0
        self.r = 0

        self.data_values = self.input_data.values  # 将数据框转换为数组

    def least_square(self):
        # 1.2数据处理
        self.x = self.data_values[:, 0]
        self.y = self.data_values[:, 1]

        # 2.1计算均值
        x_mean = np.mean(self.x)
        y_mean = np.mean(self.y)

        # 2.2计算拟合直线的斜率
        num = 0
        den_x = 0
        den_y = 0
        sse = 0

        for i in range(self.data_values.shape[0]):
            num += (self.x[i] - x_mean) * (self.y[i] - y_mean)
            den_x += (self.x[i] - x_mean) ** 2
            den_y += (self.y[i] - y_mean) ** 2

        self.k = num / den_x

        # 2.3计算拟合直线的截距
        self.b = y_mean - self.k * x_mean

        #  see是残差平方和
        for i in range(self.data_values.shape[0]):
            sse += (self.y[i] - self.k * self.x[i] - self.b) ** 2

        # 3.1计算拟合直线的决定系数R方
        self.r = 1 - sse / den_y

        # 3.2将k，b，R方的值存入df并输出
        df = pd.DataFrame(columns=['k', 'b', 'R^2'])
        df.loc['拟合结果'] = [self.k, self.b, self.r]
        print(tabulate(df, headers='keys', tablefmt='grid'))

    def picture_show(self, save=False, save_path=''):
        # 字体加载
        font_path = "times+simsun.ttf"
        font_manager.fontManager.addfont(font_path)
        prop = font_manager.FontProperties(fname=font_path)

        # 字体设置
        rcParams['font.family'] = 'sans-serif'  # 使用字体中的无衬线体异常
        rcParams['font.sans-serif'] = prop.get_name()  # 根据名称设置字体
        plt.rcParams['mathtext.fontset'] = 'stix'  # 设置数学公式字体为stix
        rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        rcParams['font.size'] = self.fontsize  # 设置字体大小

        # 是否透明背景设置
        if self.background == 'none':
            plt.figure(figsize=(4, 3), dpi=600)
        elif self.background == 'yes':
            plt.figure(figsize=(4, 3), dpi=600, facecolor='none')

        plt.tick_params(direction='in')  # 设置刻度线向图内
        plt.scatter(self.x, self.y, color='blue', marker='o', label=self.scatter_name, s=7)  # 绘制散点图
        plt.plot(self.x, self.k * self.x + self.b, color='red', label='线性拟合', linewidth=1.5,
                 linestyle=':')  # 绘制拟合直线

        # 设置xy轴标签
        plt.xlabel(self.x_name, ha='center')
        plt.ylabel(self.y_name, ha='center')
        plt.figtext(self.titlelocx, self.titlelocy, self.title_name, ha='center', va='bottom')  # 在图像底部设置标题

        # plt.xlim([0, 120])  # 设置x轴范围
        # plt.ylim([0, 1200])  # 设置y轴范围

        plt.figtext(self.formulalocx, self.formulalocy, self.formulate, ha='center', va='top')  # 在图像顶部设置公式
        plt.figtext(self.formulalocx, self.formulalocy - 0.1, "R$^2$={:.5f}".format(self.r), ha='center',
                    va='top')  # 在图像顶部设置相关系数
        plt.legend(frameon=False, loc=self.legendloc)  # 去掉图例边框
        plt.subplots_adjust(left=0.15, bottom=0.3, right=0.96, top=0.96, wspace=0, hspace=0)  # 调整图像边距

        if save:
            plt.savefig(save_path, dpi=600, bbox_inches='tight')
            plt.close()  # 关闭图像,窗口能重新打开
            print('保存成功！')
        else:
            plt.show()

    def save_picture(self, root, picture_name='拟合图像'):
        super().save_picture(root, picture_name)


#  B样条插值图像拟合类
class BSplinePicture(Picture):
    def __init__(self, input_data=pd.DataFrame()):
        super().__init__(input_data)
        self.tck = None
        self.x_new = np.array([])
        self.y_new = np.array([])

        self.data_values = self.input_data.values

    def b_spline(self):
        #  1.1数据处理
        self.x = self.data_values[:, 0]
        self.y = self.data_values[:, 1]

        # 2.1进行 B 样条插值
        self.tck = splrep(self.x, self.y, k=3)  # k=2 表示二次 B 样条插值

        # 2.2在更密集的点上进行插值，以获得更平滑的曲线
        self.x_new = np.linspace(self.x.min(), self.x.max(), 1000)
        self.y_new = splev(self.x_new, self.tck)

    def picture_show(self, save=False, save_path=''):
        # 字体加载
        font_path = "times+simsun.ttf"
        font_manager.fontManager.addfont(font_path)
        prop = font_manager.FontProperties(fname=font_path)

        # 字体设置
        rcParams['font.family'] = 'sans-serif'  # 使用字体中的无衬线体异常
        rcParams['font.sans-serif'] = prop.get_name()  # 根据名称设置字体
        plt.rcParams['mathtext.fontset'] = 'stix'  # 设置数学公式字体为stix
        rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        rcParams['font.size'] = self.fontsize  # 设置字体大小

        # 是否透明背景设置
        if self.background == 'none':
            plt.figure(figsize=(4, 3), dpi=600)
        elif self.background == 'yes':
            plt.figure(figsize=(4, 3), dpi=600, facecolor='none')

        plt.tick_params(direction='in')  # 设置刻度线向图内

        plt.scatter(self.x, self.y, color='blue', marker='o', label=self.scatter_name, s=7)  # 绘制散点图
        plt.plot(self.x_new, self.y_new, '-', label='B 样条插值', color='red', linewidth=0.5)  # 绘制插值曲线

        # 设置xy轴标签
        plt.xlabel(self.x_name, ha='center')
        plt.ylabel(self.y_name, ha='center')
        plt.figtext(self.titlelocx, self.titlelocy, self.title_name, ha='center', va='bottom')
        plt.figtext(self.formulalocx, self.formulalocy, self.formulate, ha='center', va='top')
        plt.legend(frameon=False, loc=self.legendloc)
        plt.subplots_adjust(left=0.15, bottom=0.3, right=0.96, top=0.96, wspace=0, hspace=0)

        if save:
            plt.savefig(save_path, dpi=600, bbox_inches='tight')
            plt.close()
            print('保存成功！')
        else:
            plt.show()

    def save_picture(self, root, picture_name='插值图像'):
        super().save_picture(root, picture_name)
