# DriverlessCar

本项目是基于Raspberry Pi 3B+嵌入式系统的无人驾驶小车设计

## 1 预处理 

包含调用OpenCV的过滤、色彩空间转换等预处理方法

## 2 特征点检测和匹配

包含调用OpenCV的SIFT、SURF、ORB算法及其比较

## 3 CNN模型

包含一个卷积神经网络模型，包括两个Convolution + Pooling layer、全连接层、Dropout、全连接层、Softmax输出层

| 类型 | Kernel尺寸/步长（或注释） | 输入尺寸 |
|  ----  |  ----  |  ----  |
| 卷积 | 3*3*16/1 | 128*128*1 |
| 池化 | 2*2/2 | 128*128*16 |
| 卷积 | 3*3*32/1 | 64*64*16 |
| 池化 | 2*2/2 | 64*64*32 |
| 全连接 | (32*32*32)*256 | 1*(32*32*32) |
| Dropout | 随机失活 | 1*256 |
| 全连接 | 256*(classnumber) |1*256 |
| Softmax | probabilities | (classnumber) |
