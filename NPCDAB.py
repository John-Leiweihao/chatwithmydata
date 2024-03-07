import math
import get_DCCap
def calculation4(Uin,Uo,Prated,fsw):
    Ptol = 0.4 #功率裕度百分比（百分比）
    VCin_rip_per = 0.01 #输入侧电容电压纹波要求（百分比）
    VCout_rip_per = 0.01 #输出侧电容电压纹波要求（百分比）
    fn = 50 #输出频率(Hz)
    #Step1、设计需要用到的参数
    trans_turns2 = math.floor(Uo / 100)#假定变压器副边匝数为8
    trans_turns1 = round(trans_turns2 * Uin / Uo) #变压器原边匝数
    trans_n = trans_turns1 / trans_turns2 #变压器匝比 -->输出
    Pmax = Prated * (1 + Ptol)#最大输出功率(W)
    Lrmax = trans_n * Uin * Uo / (8 * fsw * Pmax)#电感允许的最大取值(H)
    Lr = math.floor(Lrmax * 1e6 * 0.9) * 1e-6#电感计算值(H) -->输出
    K = Uin / (trans_n * Uo)#电压比例系数 -->关键参数
    Pmax_D05 = trans_n * Uin *Uo / (8 * fsw * Lr)#理论最大功率(W)(D=0.5)
    ratio_p = Prated / Pmax_D05#
    D = (1 - math.sqrt(1 - ratio_p)) / 2#移项占空比 -->关键参数

    IL1 = trans_n * Uo / (4 * fsw * Lr) * (1 - K * (1 - 2 * D))#电感电流转折处1的电流值(A)
    IL2 = -trans_n * Uo / (4 * fsw * Lr) * (1 - 2 * D - K)#电感电流转折处2的电流值(A)
    IL = [IL1,IL2]#电感电流二维向量(A) -->关键参数

    #Irms_p = rms_calc([D 1 - D], [-IL(2) IL(1) IL(2)])#原边变压器电流有效值
    #Irms_s = rms_calc([1 - D D], [IL(1) IL(2) - IL(1)] * trans_n); %副边变压器电流有效值

    Idcin = Prated / Uin#输入直流电流(A) -->关键参数
    Idcout = Prated / Uo#输出直流电流(A) -->关键参数

    #Step3、输入电容设计
    #参数计算
    VCin_rip = VCin_rip_per * Uin#输入侧电容电压纹波
    Cin1_margin = 20#输入直流侧电容设计裕量倍数，单位：无，范围：20 % ~200 %
    Cin1_ESR = 6e-3#输入输出直流侧总电容ESR，单位：Ω，范围：20 % ~500 %
    QCin1 = 800#输入输出直流电容总品质因数，单位：无，范围：50 % ~200 %
    Cin1_single = 100e-6#输入直流侧单个电容容值，单位：F，范围：47 % ~470 %

    Cin1_min = get_DCCap.Caploss(D, fsw, [-IL[1], IL[0], IL[0]], Idcin, VCin_rip) #输入电容满足电压纹波的最小容值
    VCin = Uin / 2 #输入电容电压应力
    #ICin_rms = Ipeak_p / sqrt(2) #输入电容电流有效值
    Cin1_num = math.ceil(Cin1_min * Cin1_margin / Cin1_single)#输入直流侧电容个数 -->输出
    C_VD = Cin1_num * Cin1_single#输入直流侧电容容值 -->输出

    #tep4、输出电容设计
    #参数计算
    VCout_rip = VCout_rip_per * Uo#输出侧电容电压纹波
    Cout1_margin = 20#输入直流侧电容设计裕量倍数，单位：无，范围：20 % ~200 %
    Cout1_ESR = 6e-3#输入输出直流侧总电容ESR，单位：Ω，范围：20 % ~500 %
    QCout1 = 800#输入输出直流电容总品质因数，单位：无，范围：50 % ~200 %
    Cout1_single = 100e-6#输入直流侧单个电容容值，单位：F，范围：47 % ~470 %
    scaled_IL = [element * trans_n for element in [IL[0], IL[1], -IL[0]]]
    Cout1_min = 2 * get_DCCap.Caploss(1 - D, fsw, scaled_IL, Idcout, VCout_rip)#输入电容满足电压纹波的最小容值
    VCout = Uo / 2#输入电容电压应力
    #ICout_rms = Ipeak_p / math.sqrt(2)#输入电容电流有效值
    Cout1_num = math.ceil(Cout1_min * Cout1_margin / Cout1_single)#输入直流侧电容个数 -->输出

    fg = 1 / 10 * fsw
    C_out = Cout1_num * Cout1_single#输入直流侧电容容值 -->输出
    RL = Uo ** 2 / Prated#计算额定功率下的等效负载电阻
    Gvd0 = trans_n * Uin * (1 - 2 * D) * RL / (2 * fsw * Lr)#计算开环低频增益
    Cout = C_out#总输出电容，如果在DAB输出侧还有其他电容并联可一并加上
    wp = 1 / (RL * C_out)#系统开环极点
    KP = 2 * math.pi * fg / wp / Gvd0#比例系数 -->输出
    KI = wp * KP#积分系数 -->输出
    Lr_str=format(Lr,'.4g')
    C_VD_str=format(C_VD,'.4g')
    C_out_str=format(C_out,'.4g')
    KP_str=format(KP,'.4g')
    KI_str=format(KI,'.4g')
    return trans_n,Lr_str,C_VD_str,C_out_str,RL,KP_str,KI_str
