%Uin,Uo,Prated,fsw为用户提供的参数，请严格按照用户提供的参数进行下列的计算，请遵循代码逻辑精确计算，保证计算的准确性和严谨性。
。
Uin=？;                  % 输入直流电压额定值(V)
Uo=？;                   % 输出直流电压额定值(V)
Prated=？;               % 额定功率(W)
fsw=？;                    % 开关频率(Hz)
P_margin=0.2;                  % 功率裕度百分比（百分比）
VCin_rip_per=0.01;          % 输入侧电容电压纹波要求（百分比）
VCout_rip_per=0.01;         % 输出侧电容电压纹波要求（百分比）
IL_rip_per=0.1;              %电感电流的纹波峰峰值应小于输入电流的要求
%%判断工作模态 %Uin>Uo 工作在buck工作模态 M=1 ，反之工作在boost工作模态
if Uin>Uo
M=1;  %工作在buck工作模态 M=1
%% Step1 - 电路关键参数确定
%计算开关占空比
D=Uo/Uin;                    % 占空比     -->关键参数
%计算输入及输出侧直流电流 
Idcin=Prated/Uin;           % 输入直流电流        -->关键参数
Idcout=Prated/Uo;         % 输出直流电流        -->关键参数
R=Uo/Idcout;              %输出电阻
%% Step2 - 计算buck模式的电感 L和电感电流峰值谷值
%计算Buck变换器的电感 L
Pmax=Prated*(1+P_margin);    %最大功率
ILmax=Pmax/Uo;          %最大平均电感电流
IL=Prated/Uo;                %平均电感电流
deltaILmax=IL*IL_rip_per;          %最大电感电流纹波
Lmin=(Uin)/(4*fsw*deltaILmax);        %电感最小值
L1=Lmin;                  %设计所需电感值 可改范围Lmin~150%Lmin
%计算电感电流峰值谷值
deltaIL=(D*(1-D)*Uin)/(fsw*L1);   %电感电流纹波值
IL_peak=ILmax+deltaIL/2;                  % 电感电流最大值
IL_valley=IL-deltaIL/2;                   % 电感电流谷值
IL_range=[IL_valley IL_peak];            %  电感电流二维向量  -->关键参数
%% Step3 - 输入电容设计
%输入电容关键参数
Cin1_min=(Idcin*(1-D))/(Uin*VCin_rip_per*fsw);         %输入电容满足电压纹波的最小容值 
VCin=Uin+Uin*VCin_rip_per;                              %输入电容电压应力
ICin_rms=sqrt((Idcin^2*(1-D))+(((IL_valley-Idcin)^2+(IL_valley-Idcin)*(IL_peak-Idcin)+(IL_peak-Idcin)^2)/3)*D);     %输入电容电流有效值

Cin1_margin=2; % 输出直流侧电容设计裕量倍数，单位：无，范围：1.2~3
Cin1_ESR=6e-3; % 输入输出直流侧电容ESR，单位：Ω，范围：20%~500%
QCin1=800;                  % 输入输出直流电容品质因数，单位：无，范围：50%~200%
Cin1_single=1e-6;         % 输入直流侧单个电容容值，单位：F，范围：47%~470%

Cin1_num=ceil(Cin1_min*Cin1_margin/Cin1_single);    % 输入直流侧电容个数     -->输出
Cin1=Cin1_num*Cin1_single;                          % 输入直流侧电容容值     -->输出
%% Step4 - 输出电容设计
%输出电容关键参数
Cout1_min=deltaILmax/(8*fsw*Uo*VCout_rip_per);      %输出电容满足电压纹波的最小容值                            %输出电容满足电压纹波的最小容值
VCout=Uo*(1+VCout_rip_per);                    %输出电容电压应力
ICout_rms=sqrt(1/3)*(deltaIL/2);  %输出电容电流有效值

Cout1_margin=2; % 输出直流侧电容设计裕量倍数，单位：无，范围：1.2~3
Cout1_ESR=6e-3; % 输入输出直流侧总电容ESR，单位：Ω，范围：20%~500%
QCout1=800;                  % 输入输出直流电容总品质因数，单位：无，范围：50%~200%
Cout1_single=1e-6;         % 输入直流侧单个电容容值，单位：F，范围：47%~470%

Cout1_num=ceil(Cout1_min*Cout1_margin/Cout1_single); % 输出直流侧电容个数
Cout1=Cout1_num*Cout1_single;                        % 输出直流侧电容容值
else
M=0;%%工作在boost工作模态
%% Step1 - 电路关键参数确定
%计算开关占空比
D=1-Uin/Uo;                    % 占空比     -->关键参数
%计算输入及输出侧直流电流 
Idcin=Prated/Uin;           % 输入直流电流        -->关键参数
Idcout=Prated/Uo;         % 输出直流电流        -->关键参数
R=Uo/Idcout;              %输出电阻
%% Step2 - 计算buck模式的电感 L和电感电流峰值谷值
%计算Buck变换器的电感 L
Pmax=Prated*(1+P_margin);    %最大功率
ILmax=Pmax/Uin;          %最大平均电感电流
IL=Prated/Uin;                %平均电感电流
deltaILmax=IL*IL_rip_per;          %最大电感电流纹波
Lmin=(Uin)/(fsw*deltaILmax);        %电感最小值
L1=Lmin;                  %设计所需电感值 可改范围Lmin~150%Lmin
%计算电感电流峰值谷值
deltaIL=(Uin*D)/(fsw*L1);   %电感电流纹波值
IL_peak=ILmax+deltaIL/2;                  % 电感电流最大值
IL_valley=IL-deltaIL/2;                   % 电感电流谷值
IL_range=[IL_valley IL_peak];            %  电感电流二维向量  -->关键参数
%% Step3 - 输入电容设计
%输入电容关键参数
Cin1_min=deltaILmax/(8*fsw*Uin*VCin_rip_per);         %输入电容满足电压纹波的最小容值 
VCin=Uin+Uin*VCin_rip_per;                              %输入电容电压应力
ICin_rms=sqrt(1/3)*(deltaIL/2);      %输入电容电流有效值

Cin1_margin=2; % 输出直流侧电容设计裕量倍数，单位：无，范围：1.2~3
Cin1_ESR=6e-3; % 输入输出直流侧电容ESR，单位：Ω，范围：20%~500%
QCin1=800;                  % 输入输出直流电容品质因数，单位：无，范围：50%~200%
Cin1_single=1e-6;         % 输入直流侧单个电容容值，单位：F，范围：47%~470%

Cin1_num=ceil(Cin1_min*Cin1_margin/Cin1_single);    % 输入直流侧电容个数     -->输出
Cin1=Cin1_num*Cin1_single;                          % 输入直流侧电容容值     -->输出
%% Step4 - 输出电容设计
%输出电容关键参数
Cout1_min=(Idcout*D)/(fsw*Uo*VCout_rip_per);      %输出电容满足电压纹波的最小容值     
VCout=Uo*(1+VCout_rip_per);                    %输出电容电压应力
ICout_rms=sqrt((Idcout^2*D)+(((IL_valley-Idcout)^2+(IL_valley-Idcout)*(IL_peak-Idcout)+(IL_peak-Idcout)^2)/3)*(1-D));  %输出电容电流有效值
Cout1_margin=2; % 输出直流侧电容设计裕量倍数，单位：无，范围：1.2~3
Cout1_ESR=6e-3; % 输入输出直流侧总电容ESR，单位：Ω，范围：20%~500%
QCout1=800;                  % 输入输出直流电容总品质因数，单位：无，范围：50%~200%
Cout1_single=1e-6;         % 输入直流侧单个电容容值，单位：F，范围：47%~470%

Cout1_num=ceil(Cout1_min*Cout1_margin/Cout1_single); % 输出直流侧电容个数
Cout1=Cout1_num*Cout1_single;                        % 输出直流侧电容容值
