from sympy import symbols, diff, sympify, simplify, pi, E, exp, sin, cos, tan, log
import pandas as pd
import numpy as np
from tabulate import tabulate
import re  # 正则表达式
import wcwidth
from tkinter import *
from tkinter import filedialog
import threading


class Data:
    def __init__(self):
        self.input_data = pd.DataFrame()  # 初始化一个空数据框,储存输入结果
        self.input_pre_T = pd.DataFrame()  # 初始化一个空数据框,储存预处理结果
        self.input_pre = pd.DataFrame()  # 初始化一个空数据框,储存预处理结果
        self.analysis_data = pd.DataFrame()  # 初始化一个空数据框,储存分析要分析的数据,默认为原始数据

        self.x_size = 0  # 分量个数
        self.xi_size = 0  # 单个分量数据个数

        self.i = 1  # 计数器

    #  导入数据
    def data_import(self):

        print("注意！导入数据后会删除之前的数据")

        # 实例化
        root = Tk()
        root.geometry("500x500")
        root.withdraw()
        # 获取文件夹路径
        f_path = filedialog.askopenfilename()
        if f_path == "":
            print("未选择文件,请重新选择")
            root.destroy()
            return 0
        root.destroy()

        #  初始化数据
        self.input_data = pd.DataFrame()
        self.input_pre_T = pd.DataFrame()
        self.input_pre = pd.DataFrame()
        self.analysis_data = pd.DataFrame()

        #  读取数据
        self.input_data = pd.read_excel(f_path)

        self.x_size = self.input_data.shape[1]  # 分量个数
        self.xi_size = self.input_data.shape[0]  # 单个分量数据个数

        self.input_pre_T = pd.DataFrame(columns=range(self.xi_size), index=['x1'])  # 初始化数据框,储存预处理结果

        self.analysis_data = self.input_data  # 初始化一个空数据框,储存分析要分析的数据,默认为原始数据

    #  输入数列关系
    def seq_relation(self):
        seq_values = []  # 初始化一个空列表来存储数列值
        n = 0  # 初始化一个计数器
        pi = np.pi
        E = np.e

        #  创建空列表
        for i in range(self.x_size):
            locals()['x' + str(i + 1)] = []

        # 将数据框的值赋给x1,x2,...,xNx
        for i in range(self.x_size):
            for j in range(self.xi_size):
                locals()['x' + str(i + 1)].append(self.input_data.iloc[j, i])

        seq = input("请输入数列（例如：'x1[i]+x1[i+1]'或'x1+x2'）：")  # 接收用户输入的数列字符串

        # 如果有输入x1，x2等变量，且后面没有跟着[i]，将其替换为x1[i]，x2[i]等
        for i in range(self.x_size):
            if not re.search('x' + str(i + 1) + '\\[i]', seq):
                seq = seq.replace('x' + str(i + 1), 'x' + str(i + 1) + '[i]')

        #  将数列字符串转换为表达式
        for i in range(self.xi_size):
            try:
                seq_exp = eval(seq)
                seq_values.append(seq_exp)
                n += 1
            except:
                break

        #  如果数列值不够，用None补齐
        if n != self.xi_size:
            while n != self.xi_size:
                seq_values.append('None')
                n += 1

        #  将数列值赋给x1,x2,...,xNx
        self.input_pre_T.loc['x' + str(self.i)] = seq_values
        self.i += 1
        self.input_pre = self.input_pre_T.T  # 转置

    #  选择要分析的数据
    def det(self, i):
        if i == 1:
            self.analysis_data = self.input_data
        else:
            self.analysis_data = self.input_pre

        self.analysis_data = self.analysis_data.astype(float)

    #  打印数据
    def print_ori_data(self):
        print('原始数据为：')
        print(tabulate(self.input_data, headers='keys', tablefmt='grid'))
        print('预处理数据为：')
        print(tabulate(self.input_pre, headers='keys', tablefmt='grid'))

    def print_analysis_data(self):
        print('分析数据为：')
        print(tabulate(self.analysis_data, headers='keys', tablefmt='grid'))

    #  保存预处理数据
    def save_pre_data(self):
        filename = input("请输入保存文件名(不需要后缀)(如果留空，默认文件名为'预处理数据'，直接按回车就行)：")
        if filename == "":
            filename = '预处理数据.xlsx'
        else:
            filename += '.xlsx'
        # 实例化
        root = Tk()
        root.geometry("500x500")
        root.withdraw()
        # 获取文件夹路径
        f_path = filedialog.askdirectory()
        if f_path == "":
            print("未选择文件")
            root.destroy()
            return 0
        root.destroy()
        self.input_pre.to_excel(f_path + '/' + filename)
        print('文件的保存路径为：' + f_path + '/' + filename)


def main():
    from least_square import LeastSquarePicture, BSplinePicture
    from UCclass import UncertaintyCalculate

    def data_processing(num, root):
        root.destroy()  # destroy main win
        if num == 0:
            data.data_import()
        elif num == 1:
            data.seq_relation()  # enter win 1
        elif num == 2:
            data.print_ori_data()  # enter win 2
        elif num == 3:
            def detvalue(i):
                if i == 1:
                    data.det(1)
                    root2.destroy()
                    return 0
                else:
                    data.det(2)
                    root2.destroy()
                    return 0

            root2 = Tk()
            root2.title('不确定度分析')
            root2.geometry('300x300+888+444')

            button2_1 = Button(root2, text="原始数据", command=lambda: detvalue(1))
            button2_1.pack(pady=5)
            button2_2 = Button(root2, text="预处理数据", command=lambda: detvalue(2))
            button2_2.pack(pady=5)

            root2.mainloop()
        elif num == 4:
            data.print_analysis_data()
        elif num == 5:
            data.save_pre_data()
        window()

    def uncertainty_calculation(root):
        root.destroy()

        uc = UncertaintyCalculate(data.analysis_data)
        uc.initialization()
        uc.data_process()
        uc.print_default()
        uc.windows()

        window()

    def least_square_method(root):
        root.destroy()

        lsp = LeastSquarePicture(data.analysis_data)
        lsp.least_square()
        lsp.picture_init()
        lsp.picture_show()
        lsp.picture_setting()

        window()

    # 三阶B样条曲线拟合
    def b_spline_method(root):
        root.destroy()

        bsp = BSplinePicture(data.analysis_data)
        bsp.b_spline()
        bsp.picture_init()
        bsp.picture_show()
        bsp.picture_setting()

        window()

    # 主窗口
    def window():
        root = Tk()
        root.title('不确定度分析')
        root.geometry('400x400+888+300')
        button1 = Button(root, text="导入数据", command=lambda: data_processing(0, root))
        button1.pack(pady=5)
        button2 = Button(root, text="预处理", command=lambda: data_processing(1, root))
        button2.pack(pady=5)
        button3 = Button(root, text="打印原始和预处理数据", command=lambda: data_processing(2, root))
        button3.pack(pady=5)
        button4 = Button(root, text="选择要分析的数据", command=lambda: data_processing(3, root))
        button4.pack(pady=5)
        button5 = Button(root, text="打印要分析的数据", command=lambda: data_processing(4, root))
        button5.pack(pady=5)
        button9 = Button(root, text="保存预处理数据", command=lambda: data_processing(5, root))
        button9.pack(pady=5)

        #  文字说明
        label = Label(root, text="数据分析：")
        label.pack(pady=5)

        button6 = Button(root, text="不确定度计算", command=lambda: uncertainty_calculation(root))
        button6.pack(pady=5)

        button7 = Button(root, text="最小二乘法线性拟合", command=lambda: least_square_method(root))
        button7.pack(pady=5)

        button8 = Button(root, text="三阶B样条曲线拟合", command=lambda: b_spline_method(root))
        button8.pack(pady=5)

        root.mainloop()

    # 实例化
    data = Data()
    window()


if __name__ == '__main__':
    main()
