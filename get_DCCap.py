def Caploss(D, fs, IL, Idc, V_rip):
    Ths=1/fs/2
    ILac = [il - Idc for il in IL]
    if (ILac[0]*ILac[1]<=0) and (ILac[1]*ILac[2]>=0):
        ILac = [abs(il) for il in ILac]
        Dz=D*ILac[0]/(ILac[0]+ILac[1])      #电流交流分量过零点处的坐标
        Cap=ILac[0]*Dz*Ths/2/V_rip
    elif (ILac[0]*ILac[1]>=0) and (ILac[1]*ILac[2]<=0):
        ILac = [abs(il) for il in ILac]
        Dz=(1-D)*ILac[2]/(ILac[1]+ILac[2])
        Cap=ILac[2]*Dz*Ths/2/V_rip
    elif (ILac[0]*ILac[1]<=0) and (ILac[1]*ILac[2]<=0):
        ILac = [abs(il) for il in ILac]
        Dz=D*ILac[1]/(ILac[0]+ILac[1])+(1-D)*ILac[1]/(ILac[1]+ILac[2])
        Cap=ILac[1]*Dz*Ths/2/V_rip
    else:
        Cap=-1;     # 输入参数有误
    return Cap