import math
import sympy as sp
def calculation3(Uin,Uo,Prated,fsw):
    P_margin = 0.2#功率裕度百分比（百分比）
    VCin_rip_per = 0.01 #输入侧电容电压纹波要求（百分比）
    VCout_rip_per = 0.01 #输出侧电容电压纹波要求（百分比）
    IL_rip_per = 0.1 #电感电流的纹波峰峰值应小于输入电流的要求
    if Uin>Uo:
        M="buck"              #电路工作在buck模式
        D=Uo/Uin                    # 占空比     -->关键参数
        Idcin=Prated/Uin           # 输入直流电流        -->关键参数
        Idcout=Prated/Uo         # 输出直流电流        -->关键参数
        R=Uo/Idcout             #输出电阻
        # Step6 - buck模式电感设计
        Pmax=Prated*(1+P_margin)    #最大功率
        ILmax=Pmax/Uo         #最大平均电感电流
        IL=Prated/Uo                #平均电感电流
        deltaILmax=IL*IL_rip_per          #最大电感电流纹波
        Lmin=Uin/(16*fsw*deltaILmax)        #电感最小值
        L1=1.2*Lmin                 #设计所需电感值
        #Step4 - 输入电容设计
        if D<0.5:
            Cin1_min=(2*Prated*D)/(fsw*Uin*(Uin/2)*VCin_rip_per)        #输入电容1满足电压纹波的最小容值
            Cin2_min=Cin1_min                                        #输入电容2满足电压纹波的最小容值
            VCin=Uin/2+(Uin/2)*VCin_rip_per #输入电容电压应力
        else:
            Cin1_min=(2*Prated*(1-D))/(fsw*Uin*(Uin/2)*VCin_rip_per)        #输入电容1满足电压纹波的最小容值
            Cin2_min=Cin1_min                                        #输入电容2满足电压纹波的最小容值
            VCin=Uin/2+(Uin/2)*VCin_rip_per #输入电容电压应力
        Cin1_margin=2
        Cin1_ESR=6e-3
        QCin1=800                  # 输入输出直流电容总品质因数，单位：无
        Cin1_single=1e-6         # 输入直流侧单个电容容值，单位：F
        Cin2_margin=2
        Cin2_ESR=6e-3
        QCin2=800                  # 输入输出直流电容总品质因数，单位：无
        Cin2_single=1e-6         # 输入直流侧单个电容容值，单位：F
        Cin1_num=math.ceil(Cin1_min*Cin1_margin/Cin1_single)    # 输入直流侧电容1个数     -->输出
        Cin2_num=Cin1_num                                  # 输入直流侧电容2个数     -->输出
        Cin1=Cin1_num*Cin1_single                          # 输入直流侧电容1容值     -->输出
        Cin2=Cin1                                          # 输入直流侧电容2容值     -->输出
        # Step5 - 输出电容设计
        #输出电容的关键参数
        Cout1_min=deltaILmax/(16*fsw*Uo*VCout_rip_per)         #输出电容满足电压纹波的最小容值
        VCout=Uo+Uo*VCout_rip_per                             #输出电容电压应力
        Cout1_margin=2
        Cout1_ESR=6e-3
        QCout1=800                 # 输入输出直流电容总品质因数，单位：无
        Cout1_single=1e-6         # 输入直流侧单个电容容值，单位：F
        #输出电容设计结果
        Cout1_num=math.ceil(Cout1_min*Cout1_margin/Cout1_single) #输出直流侧电容个数
        Cout1=Cout1_num*Cout1_single                        # 输出直流侧电容容值
        L=L1
        C1=Cin1
        C2=Cin2
        C3=Cout1
        fcc = fsw / 20
        wcc = 2 * math.pi * fcc
        gama = 68
        s = wcc * 1j

        # Define the transfer function Gid
        Gid = (Uin * (Cout1 * s + 1 / R)) / (L1 * Cout1 * s ** 2 + L1 * s / R + 1)

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
        kpi = format(-float(PI_i[0][kpi]), '.3g')
        kii = format(-float(PI_i[0][kii]), '.3g')
    else:
        M="boost"
        D=1-Uin/Uo                    # 占空比     -->关键参数
        # 计算输入及输出侧直流电流
        Idcin=Prated/Uin           # 输入直流电流        -->关键参数
        Idcout=Prated/Uo         # 输出直流电流        -->关键参数
        R=Uo/Idcout             #输出电阻
        # Step6 - boost模式电感设计
        Pmax=Prated*(1+P_margin)    #最大功率
        ILmax=Pmax/Uin          #最大平均电感电流
        IL=Prated/Uin               #平均电感电流
        deltaILmax=IL*IL_rip_per          #最大电感电流纹波
        Lmin=Uo/(16*fsw*deltaILmax)        #电感最小值
        L1=1.2*Lmin                  #设计所需电感值
        # Step4 - 输入电容设计
        #输入电容关键参数
        Cin1_min=deltaILmax/(16*fsw*Uin*VCin_rip_per)         #输入电容满足电压纹波的最小容值
        VCin=Uo+Uo*VCin_rip_per                             #输入电容电压应力
        Cin1_margin=2
        Cin1_ESR=6e-3
        QCin1=800                 # 输入输出直流电容总品质因数，单位：无
        Cin1_single=1e-6         # 输入直流侧单个电容容值，单位：F
        Cin1_num=math.ceil(Cin1_min*Cin1_margin/Cin1_single)   # 输入直流侧电容个数     -->输出
        Cin1=Cin1_num*Cin1_single                          # 输入直流侧电容容值     -->输出
        if D<0.5:
        #输出电容关键参数
            Cout1_min=(Idcout*D)/(fsw*(Uo/2)*VCout_rip_per)     #输出电容满足电压纹波的最小容值
            Cout2_min=Cout1_min                                  #输出电容满足电压纹波的最小容值
            VCout=Uo/2+(Uo/2)*VCout_rip_per                     #输出电容电压应力
        else:
        #输出电容关键参数
            Cout1_min=(Idcout*(1-D))/(fsw*(Uo/2)*VCout_rip_per)      #输出电容满足电压纹波的最小容值
            Cout2_min=Cout1_min                                  #输出电容满足电压纹波的最小容值
            VCout=Uo/2+(Uo/2)*VCout_rip_per                    #输出电容电压应力
        Cout1_margin=2
        Cout1_ESR=6e-3
        QCout1=800                  # 输入输出直流电容总品质因数，单位：无
        Cout1_single=1e-6         # 输入直流侧单个电容容值，单位：F
        Cout2_margin=2
        Cout2_ESR=6e-3
        QCout2=800                  # 输入输出直流电容总品质因数，单位：无
        Cout2_single=1e-6         # 输入直流侧单个电容容值，单位：F
        Cout1_num=math.ceil(Cout1_min*Cout1_margin/Cout1_single) # 输出直流侧电容1个数
        Cout2_num=Cout1_num                                 # 输出直流侧电容2个数
        Cout1=Cout1_num*Cout1_single                        # 输出直流侧电容1容值
        Cout2=Cout1                                        # 输出直流侧电容2容值
        L=L1
        C1=Cout1
        C2=Cout2
        C3=Cin1
        fcc = fsw / 20
        wcc = 2 * math.pi * fcc
        gama = 68
        s = wcc * 1j

        # Define the transfer function Gid
        Gid=(Uo*(Cout1*s+4/R))/(L1*Cout1*s**2+2*L1*s/R+2*(1-D)**2)

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
        kpi = format(-float(PI_i[0][kpi]), '.3g')
        kii = format(-float(PI_i[0][kii]), '.3g')
    L_str = format(L1, ".3e")
    C1_str = format(C1, ".3e")
    C2_str = format(C2, ".3e")
    C3_str = format(C3,".3e")
    return M,L_str,C1_str,C2_str,C3_str,kpi,kii