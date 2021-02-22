import pandas as pd
from scipy import stats

def import_and_fit_file(FileNameAndPath):
    #df = pd.read_csv("C:\MUXdata\FileName_Lp21.tsv", sep='\t')
    df = pd.read_csv(FileNameAndPath, sep='\t')
    slope, intercept, r_value, p_value, std_err = stats.linregress(df)
    return {'G': [slope], 'std_err': [std_err]}

def fit_for_Master(df,xVar='V_SD',yVar='I_SD'):
    slope, intercept, r_value, p_value, std_err = stats.linregress(df[xVar],df[yVar])
    return {'G': [slope], 'std_err': [std_err]}

def merge(Params, Fit, Master):
    Params.update(Fit)
    DF = pd.DataFrame(Params)
    Master = Master.append(DF, ignore_index = True)
    return Master