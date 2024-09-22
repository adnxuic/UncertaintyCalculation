<center>UncertaintyCalculation使用手册（1.4.0）</center>



[TOC]

<div style="page-break-after: always;"></div>

## 数据处理流程

~~~ mermaid
graph TD
A(导入数据)==>B(数据预处理)
B==>C(数据处理)
C-->D[不确定度计算]
C-->E[数据可视化]
~~~

<div style="page-break-after: always;"></div>

## 1.导入数据

![主窗口](/picture/main_window.png)

### 1.1 导入数据



* 打开后会弹出窗口,直接选择文件就行。

  1. 导入的文件为==Excel==

  2. Excel的==格式要求==为：

     ![excel格式](/picture/excel.png)

     可以有再多列的数据x3,x4等等

  3. 对于不确定度计算，一列为一个分量

  4. 对于数据可视化，第一列为x轴，第二列为y轴（不管后面有几列都取前两行）

* 注意！每次导入数据都会清空之前的所有数据，方便重复计算！



### 1.2 预处理数据



* 对一些数据先处理，方便后面的数据处理，如：
  * 取平均值消除偏心差
  * 取对数处理，方便线性拟合
* 可用数列的表示形式，如：
  * x1[i]+i
  * x1[i]+x2[i+1]
* 可用函数形式：
  * x1+x2
  * log(x1)[数学附录](#数学附录)



### 1.3 打印、选择与保存



1. 打印：打印为在控制台上显示数据
2. 选择：选择数据为选择你要进行分析的数据（如果没选择，那么默认为导入的原始数据）
3. 保存：保存为Excel格式，在控制台输入文档的名称（不是文件的保存路径且不需要后缀）



## 2.数据分析

### 2.1 不确定度计算

* 简单的不确定度评定：
  1. 默认为自由度为无限大
  2. B类不确定度的仪器示值误差按均匀分布计算
* 公式输入:
  1. 各分量名称为x1,x2······xn(请记住各分量的意义)
  2. 符号要求见附录

![不确定度图](/picture/uc.png)

* 打印与保存同上

  

### 2.2 线性拟合

* 注意！ x轴的值（对应x1）要从小到大排列

* 各名称输入支持Latex格式

  ![拟合终端](/picture/fit1.png)

  ![拟合](/picture/fit2.png)

  *  如果出现糊在一起的情况，就手动调整
  *  图片中文为宋体，英文为Times New Roman

* 关闭图片后

  ​	![拟合选项窗口](/picture/fitwindow.png)

  * 建议调整字体（默认为5）和标题位置（调整选项中0-1为相对位置）

![拟合图](/picture/fit_picture.png)

* 保存：

  1. 放大窗口后下面有保存图标：

     ![图片保存](/picture/save.png)

     2.选项卡的保存选项

### 2.3 B样条曲线拟合

* 注意！ x轴的值（对应x1）要从小到大排列

* 公式等可以滞空（直接回车）

![B样条终端](/picture/B1.png)

![B样条图](/picture/B2.png)

* 图片设置保存如上



<div style="page-break-after: always;"></div>

## A.数学附录

| 输入表达式 |   数学表达式    |
| :--------: | :-------------: |
|   x1/x2    | $\frac{x1}{x2}$ |
|   x1*x2    |  $x1 \cdot x2$  |
|  exp(x1)   |    $e^{x1}$     |
|  log(x1)   |    $ln(x1)$     |
| log(x1,a)  |  $\log_a(x1)$   |
|     pi     |      $\pi$      |
|     E      |  $e$(自然常数)  |



##  B.问题反馈

邮箱：uncercalculate@163.com

Github: [adnxuic/UcertaintyCalculation (github.com)](https://github.com/adnxuic/UcertaintyCalculation)
