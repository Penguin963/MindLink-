#导入相关库
import serial

import matplotlib.pyplot as plt

#链接蓝牙接口com4，将波特率和接收数据比特数按照产品说明书设置好
ser = serial.Serial(port="com4", baudrate=57600, timeout=1, bytesize=8, parity=serial.PARITY_NONE)

# 设置图像大小
plt.figure(figsize=(10, 10), dpi=70)

#设置变量存储x轴
X = []

#Y1和Y2分别存储attention专注度和meditation冥想值数据
Y1 = []
Y2 = []

#设置相关变量存储脑电相关数据
#以下变量分别为delta、theta、low alpha、high alpha、low beta、high beta、low gamma和 mid gamma的数据
nd = []
nt = []
nla = []
nha = []
nlb = []
nhb = []
nlg = []
nhg = []

#以下变量分别为delta、theta、low alpha、high alpha、low beta、high beta、low gamma和 mid gamma的占比
pd = []
pt = []
pla = []
pha = []
plb = []
phb = []
plg = []
phg = []

#num为接收脑电波数据的次数（大约一秒钟接受一次目标数据包）
num = 0

#判断接口是否链接成功
if ser.isOpen():
    #开始循环
    while num <= 50:
        #data存储获取的字节流数据
        data = ser.read(288)
        #按照数据包说明解析出各脑电波的数据并转换为十进制数
        for i in range(1, len(data) - 32):
            if data[i] == int('AA', 16):
                if data[i+1] == int('AA', 16):
                    if data[i+2] == int('20', 16):
                        if data[i+3] == int('02', 16):
                            if data[i+5] == int('83', 16):
                                if data[i+6] == int('18', 16):
                                    h_ = data[i+7]
                                    m_ = data[i+8]
                                    l_ = data[i+9]
                                    delta = h_ * 65536 + m_ * 256 + l_
                                    nd.append(delta)
                                    print("delta: ", delta)
                                    h_ = data[i+10]
                                    m_ = data[i+11]
                                    l_ = data[i+12]
                                    theta = h_ * 65536 + m_ * 256 + l_
                                    nt.append(theta)
                                    print("theta: ", theta)
                                    h_ = data[i+13]
                                    m_ = data[i+14]
                                    l_ = data[i+15]
                                    lowAlpha = h_ * 65536 + m_ * 256 + l_
                                    nla.append(lowAlpha)
                                    print("lowAlpha: ", lowAlpha)
                                    h_ = data[i+16]
                                    m_ = data[i+17]
                                    l_ = data[i+18]
                                    highAlpha = h_ * 65536 + m_ * 256 + l_
                                    nha.append(highAlpha)
                                    print("highAlpha: ", highAlpha)
                                    h_ = data[i+19]
                                    m_ = data[i+20]
                                    l_ = data[i+21]
                                    lowBeta = h_ * 65536 + m_ * 256 + l_
                                    nlb.append(lowBeta)
                                    print("lowBeta: ", lowBeta)
                                    h_ = data[i+22]
                                    m_ = data[i+23]
                                    l_ = data[i+24]
                                    highBeta = h_ * 65536 + m_ * 256 + l_
                                    nhb.append(highBeta)
                                    print("highBeta: ", highBeta)
                                    h_ = data[i+25]
                                    m_ = data[i+26]
                                    l_ = data[i+27]
                                    lowGamma = h_ * 65536 + m_ * 256 + l_
                                    nlg.append(lowGamma)
                                    print("lowGamma: ", lowGamma)
                                    h_ = data[i+28]
                                    m_ = data[i+29]
                                    l_ = data[i+30]
                                    midGamma = h_ * 65536 + m_ * 256 + l_
                                    print("midGamma", midGamma)
                                    nhg.append(midGamma)
                                    #计算脑电波的占比
                                    all = delta + theta + lowAlpha + highAlpha + lowBeta + highBeta + lowGamma + midGamma
                                    pd.append(delta / all)
                                    pt.append(theta / all)
                                    pla.append(lowAlpha / all)
                                    pha.append(highAlpha / all)
                                    plb.append(lowBeta / all)
                                    phb.append(highBeta / all)
                                    plg.append(lowGamma / all)
                                    phg.append(midGamma / all)
                                    if data[i+31] == int('04', 16):
                                        attention_data = data[i+32]
                                        if data[i+33] == int('05', 16):
                                            meditation_data = data[i+34]
                                            print(attention_data)
                                            print(meditation_data)
                                            num = num + 1
                                            X.append(num)
                                            Y1.append(attention_data)
                                            Y2.append(meditation_data)
                                            print("end")
    #绘制attention专注度和meditation冥想值数据折线图
    plt.subplot(3,1,1)
    plt.plot(X, Y1, color="lightcoral", linewidth=3.0, linestyle="-", label="attention_data")
    plt.plot(X, Y2, color="burlywood", linewidth=3.0, linestyle="--", label="meditation_data")
    plt.legend(loc="upper left")  # 把标签加载到图中哪个位置
    plt.title("attention & meditation")

    #绘制8种脑电信号的折线图
    plt.subplot(3,1,2)
    plt.plot(X, nd, color="lightcoral", linewidth=3.0, linestyle="-", label="delta_data")
    plt.plot(X, nt, color="brown", linewidth=3.0, linestyle="--", label="theta_data")
    plt.plot(X, nla, color="darkgoldenrod", linewidth=3.0, linestyle="-", label="lowAlpha_data")
    plt.plot(X, nha, color="goldenrod", linewidth=3.0, linestyle="--", label="highAlpha_data")
    plt.plot(X, nlb, color="darkgreen", linewidth=3.0, linestyle="-", label="lowBeta_data")
    plt.plot(X, nhb, color="limegreen", linewidth=3.0, linestyle="--", label="highBeta_data")
    plt.plot(X, nlg, color="darkblue", linewidth=3.0, linestyle="-", label="lowGamma_data")
    plt.plot(X, nhg, color="blue", linewidth=3.0, linestyle="--", label="midGamma_data")
    plt.legend(loc="upper left")  # 把标签加载到图中哪个位置
    plt.title("8 EGG Power")

    #绘制8种脑电信号的堆积图
    plt.subplot(3, 1, 3)
    labels = ['delta', 'theta', 'lowAlpha', 'highAlpha', 'lowBeta', 'highBeta', 'lowGamma', 'midGamma']
    colors = ["lightcoral", "brown", "darkgoldenrod", "goldenrod", "darkgreen", "limegreen", "darkblue", "blue"]
    plt.stackplot(X, pd, pt, pla, pha, plb, phb, plg, phg, labels=labels, colors=colors)
    plt.legend(loc="upper left")
    plt.title("propotion of 8 EGG")
    plt.show()
else:
    ser.open()
