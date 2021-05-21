from test_chip import *

fileName = 'test1_top'
comment = 'fish tank, 1kOhm bottom, to compare with microscope setup.'
R_ev = 1e3
type = 'bottom' # top, bottom, all

df, basePath = micr_measure(repeats=20,
                            fileName=fileName,
                            deviceList=[i for i in range(1, 47)],
                            comment=comment)

dfc = check_values(df, R_ev=R_ev, type=type, tol=0.1, rel_std=0.005, R_zero_tol=1e6, zero_std_tol=1e6,
                   save=True, basePath=basePath)

print('done')