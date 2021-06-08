from test_chip import *

fileName = 'testMSM14_dry'
comment = 'GS, FBW, DC GND, no filter, amp 1E5 with preamp'
R_ev = 1e3
type = 'all' # top, bottom, all

df, basePath = micr_measure(repeats=20,
                            fileName=fileName,
                            currentVoltagePreAmp_gain=1E5,
                            deviceList=[i for i in range(1,47)],
                            comment=comment)

print(check_noise(df))

dfc = check_values(df, R_ev=R_ev, type=type, tol=0.1, rel_std=0.005, R_zero_tol=1e6, zero_std_tol=1e6,
                   save=True, basePath=basePath)

print('done')