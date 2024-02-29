import math
import sympy as sp
def calculation2(Uin,Uo,Prated,fsw):
    P_margin = 0.2#功率裕度百分比（百分比）
    VCin_rip_per = 0.01 #输入侧电容电压纹波要求（百分比）
    VCout_rip_per = 0.01 #输出侧电容电压纹波要求（百分比）
    IL_rip_per = 0.1 #电感电流的纹波峰峰值应小于输入电流的要求
    if Uin > Uo:
        M = "buck" #工作在buck工作模态
        ##Step1 - 电路关键参数确定
        #计算开关占空比
        D = Uo / Uin #占空比 -->关键参数
        #计算输入及输出侧直流电流
        Idcin = Prated / Uin #输入直流电流 -->关键参数
        Idcout = Prated / Uo #输出直流电流 -->关键参数
        R = Uo / Idcout; #输出电阻
        ##Step2 - 计算buck模式的电感
        #L和电感电流峰值谷值
        #计算Buck变换器的电感L
        Pmax = Prated * (1 + P_margin) #最大功率
        ILmax = Pmax / Uo  #最大平均电感电流
        IL = Prated / Uo #平均电感电流
        deltaILmax = IL * IL_rip_per #最大电感电流纹波
        Lmin = (Uin) / (4 * fsw * deltaILmax) #电感最小值
        L1 = Lmin #设计所需电感值可改范围Lmin ~150 % Lmin
        #计算电感电流峰值谷值
        deltaIL = (D * (1 - D) * Uin) / (fsw * L1) # 电感电流纹波值
        IL_peak = ILmax + deltaIL / 2 #电感电流最大值
        IL_valley = IL - deltaIL / 2 #电感电流谷值
        #Step3 - 输入电容设计
        #输入电容关键参数
        Cin1_min = (Idcin * (1 - D)) / (Uin * VCin_rip_per * fsw) #输入电容满足电压纹波的最小容值
        VCin = Uin + Uin * VCin_rip_per#输入电容电压应力
        ICin_rms = math.sqrt((Idcin ** 2 * (1 - D)) + (((IL_valley - Idcin) ** 2 + (IL_valley - Idcin) * (IL_peak - Idcin) + (IL_peak - Idcin) **2) / 3) * D)#输入电容电流有效值

        Cin1_margin = 2 #输出直流侧电容设计裕量倍数，单位：无，范围：1.2~3
        Cin1_ESR = 6e-3 #输入输出直流侧电容ESR，单位：Ω，范围：20 % ~500 %
        QCin1 = 800 #输入输出直流电容品质因数，单位：无，范围：50 % ~200 %
        Cin1_single = 1e-6 #输入直流侧单个电容容值，单位：F，范围：47 % ~470 %

        Cin1_num = math.ceil(Cin1_min * Cin1_margin / Cin1_single) #输入直流侧电容个数 -->输出
        Cin1 = Cin1_num * Cin1_single #输入直流侧电容容值 -->输出
        #Step4 - 输出电容设计
        #输出电容关键参数
        Cout1_min = deltaILmax / (8 * fsw * Uo * VCout_rip_per)#输出电容满足电压纹波的最小容值 % 输出电容满足电压纹波的最小容值
        VCout = Uo * (1 + VCout_rip_per)#输出电容电压应力
        ICout_rms = math.sqrt(1 / 3) * (deltaIL / 2)#输出电容电流有效值

        Cout1_margin = 2#输出直流侧电容设计裕量倍数，单位：无，范围：1.2~3
        Cout1_ESR = 6e-3#输入输出直流侧总电容ESR，单位：Ω，范围：20 % ~500 %
        QCout1 = 800#输入输出直流电容总品质因数，单位：无，范围：50 % ~200 %
        Cout1_single = 1e-6#输入直流侧单个电容容值，单位：F，范围：47 % ~470 %

        Cout1_num = math.ceil(Cout1_min * Cout1_margin / Cout1_single)#输出直流侧电容个数
        Cout1 = Cout1_num * Cout1_single#输出直流侧电容容值
        C1=Cout1
        C2=Cin1
        L=L1
        fcc = fsw / 10
        wcc = 2 * math.pi * fcc
        gama = 68
        s = wcc * 1j

        # Define the transfer function Gid
        Gid=(Uin*(Cout1*s+1/R))/(L1*Cout1*s**2+L1*s/R+1);

        # Define the PI controller parameters
        kpi, kii = sp.symbols('kpi kii')
        abs_Gi_PI = sp.sqrt((kpi * wcc) ** 2 + kii ** 2) / wcc
        ang_Gi_PI = sp.atan(kpi * wcc / kii) - math.pi / 2

        abs_Gid = sp.Abs(Gid)
        ang_Gid = sp.arg(Gid)

        # Set up the equations
        equ_i = [abs_Gi_PI * abs_Gid - 1, ang_Gi_PI + ang_Gid - (-(180 - gama) / (180 / math.pi))]

        # Solve the equations
        PI_i = sp.solve(equ_i, (kpi, kii), dict=True)

        # Extract the solutions
        kpi = format(-float(PI_i[0][kpi]), '.4g')
        kii = format(-float(PI_i[0][kii]), '.4g')
    else:
        M = "boost" ##工作在boost工作模态
        ##Step1 - 电路关键参数确定
        #计算开关占空比
        D = 1 - Uin / Uo #占空比 -->关键参数
        #计算输入及输出侧直流电流
        Idcin = Prated / Uin#输入直流电流 -->关键参数
        Idcout = Prated / Uo#输出直流电流 -->关键参数
        R = Uo / Idcout#输出电阻
        ##Step2 - 计算buck模式的电感L和电感电流峰值谷值
        #计算Buck变换器的电感L
        Pmax = Prated * (1 + P_margin)#最大功率
        ILmax = Pmax / Uin#最大平均电感电流
        IL = Prated / Uin#平均电感电流
        deltaILmax = IL * IL_rip_per#最大电感电流纹波
        Lmin = (Uin) / (fsw * deltaILmax)#电感最小值
        L1 = Lmin#设计所需电感值可改范围Lmin~150 % Lmin
        #计算电感电流峰值谷值
        deltaIL = (Uin * D) / (fsw * L1)#电感电流纹波值
        IL_peak = ILmax + deltaIL / 2#电感电流最大值
        IL_valley = IL - deltaIL / 2#电感电流谷值
        ##Step3 - 输入电容设计
        #输入电容关键参数
        Cin1_min = deltaILmax / (8 * fsw * Uin * VCin_rip_per)#输入电容满足电压纹波的最小容值
        VCin = Uin + Uin * VCin_rip_per#输入电容电压应力
        ICin_rms = math.sqrt(1 / 3) * (deltaIL / 2)#输入电容电流有效值

        Cin1_margin = 2#输出直流侧电容设计裕量倍数，单位：无，范围：1.2~3
        Cin1_ESR = 6e-3#输入输出直流侧电容ESR，单位：Ω，范围：20 % ~500 %
        QCin1 = 800#输入输出直流电容品质因数，单位：无，范围：50 % ~200 %
        Cin1_single = 1e-6#输入直流侧单个电容容值，单位：F，范围：47 % ~470 %

        Cin1_num = math.ceil(Cin1_min * Cin1_margin / Cin1_single)##输入直流侧电容个数 -->输出
        Cin1 = Cin1_num * Cin1_single#输入直流侧电容容值 -->输出
        ##Step4 - 输出电容设计
        #输出电容关键参数
        Cout1_min = (Idcout * D) / (fsw * Uo * VCout_rip_per)#输出电容满足电压纹波的最小容值
        VCout = Uo * (1 + VCout_rip_per)#输出电容电压应力
        ICout_rms = math.sqrt((Idcout **2 * D) + (((IL_valley - Idcout) ** 2 + (IL_valley - Idcout) * (IL_peak - Idcout) + (IL_peak - Idcout) ** 2) / 3) * (1 - D))#输出电容电流有效值
        Cout1_margin = 2#输出直流侧电容设计裕量倍数，单位：无，范围：1.2~3
        Cout1_ESR = 6e-3#输入输出直流侧总电容ESR，单位：Ω，范围：20 % ~500 %
        QCout1 = 800#输入输出直流电容总品质因数，单位：无，范围：50 % ~200 %
        Cout1_single = 1e-6#输入直流侧单个电容容值，单位：F，范围：47 % ~470 %

        Cout1_num = math.ceil(Cout1_min * Cout1_margin / Cout1_single)#输出直流侧电容个数
        Cout1 = Cout1_num * Cout1_single#输出直流侧电容容值
        C1=Cin1
        C2=Cout1
        L=L1
        fcc = fsw / 20
        wcc = 2 * math.pi * fcc
        gama = 68
        s = wcc * 1j

        # Define the transfer function Gid
        Gid=(Uin*Cout1*s+2*Uin/R)/(L1*Cout1*s**2+L1*s/R+(1-D)**2)

        # Define the PI controller parameters
        kpi, kii = sp.symbols('kpi kii')
        abs_Gi_PI = sp.sqrt((kpi * wcc) ** 2 + kii ** 2) / wcc
        ang_Gi_PI = sp.atan(kpi * wcc / kii) - math.pi / 2

        abs_Gid = sp.Abs(Gid)
        ang_Gid = sp.arg(Gid)

        # Set up the equations
        equ_i = [abs_Gi_PI * abs_Gid - 1, ang_Gi_PI + ang_Gid - (-(180 - gama) / (180 / math.pi))]

        # Solve the equations
        PI_i = sp.solve(equ_i, (kpi, kii), dict=True)

        # Extract the solutions
        kpi = format(-float(PI_i[0][kpi]), '.4g')
        kii = format(-float(PI_i[0][kii]), '.4g')
    L_str = format(L, ".3e")
    C1_str = format(C1, ".3e")
    C2_str = format(C2, ".3e")

    return M,L_str,C1_str,C2_str,kpi,kii
M,L_str,C1_str,C2_str,kpi,kii=calculation2(900,600,100e3,50e3)
print(M,L_str,C1_str,C2_str,kpi,kii)