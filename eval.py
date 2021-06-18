import pandas as pd
import numpy as np
import easygui
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm

##################Results DataFrames as Class#######################

class ResultsDF:

    def __init__(self, name = 'unnamed'):
        self.file = easygui.fileopenbox(default= 'G:/Shared drives/Nanoelectronics Team Drive/Data/2021/Marta').replace('\\', '/')
        #self.file = 'C:/Users/marta/OneDrive/Escritorio/Data/20210211/Meas4/MSM01_meas2.csv'
        self.df = pd.read_csv(self.file)
        self.name = name

    def plot_IV(self, device=None, ID=None, repeat=None):
        '''Supply either an ID or a device number with the repeat number'''
        if repeat == None and ID == None:
            print('specify device and repeat OR ID.')
        if ID != None:
            df1 = self.df[self.df['ID'] == ID]
            x = list(map(float, df1['V_SD'].tolist()[0].replace('[', '').replace(']', '').split(',')))
            y = list(map(float, df1['I_SD'].tolist()[0].replace('[', '').replace(']', '').split(',')))
            plt.plot(x, y)
        if repeat != None and device != None:
            df1 = self.df.loc[(self.df['device'] == device) & (self.df['repeat'] == repeat)]
            x = list(map(float, df1['V_SD'].tolist()[0].replace('[', '').replace(']', '').split(',')))
            y = list(map(float, df1['I_SD'].tolist()[0].replace('[', '').replace(']', '').split(',')))
            plt.plot(x, y)

    def get_IV(self, save = 0, device=None, ID=None, repeat=None):
        if repeat == None and ID == None:
            print('specify device and repeat OR ID.')
        if ID != None:
            df1 = self.df[self.df['ID'] == ID]
            x = list(map(float, df1['V_SD'].tolist()[0].replace('[', '').replace(']', '').split(',')))
            y = list(map(float, df1['I_SD'].tolist()[0].replace('[', '').replace(']', '').split(',')))
        if repeat != None and device != None:
            df1 = self.df.loc[(self.df['device'] == device) & (self.df['repeat'] == repeat)]
            x = list(map(float, df1['V_SD'].tolist()[0].replace('[', '').replace(']', '').split(',')))
            y = list(map(float, df1['I_SD'].tolist()[0].replace('[', '').replace(']', '').split(',')))
        df2 = pd.DataFrame({'V_SD': x, 'I_SD': y})
        if save == 1:
            df2.to_csv(easygui.filesavebox(filetypes='*.csv').replace('\\', '/')+'.csv')
        return (df2)

    def plot_device(self, device = 0):
        df1 = self.df[self.df['device'] == device]
        plt.errorbar(df1['time'], df1['G'], yerr = df1['std_err'], marker='s', mfc='red',
        mec='green', ms=20, mew=4)

    def plot_all(self, title = 'title'):
        deviceList = self.df.device.unique()
        linestyles = ['-', '--', '-.', ':']
        #plt.figure(num = str(self.name)+'_all')
        plt.title(title)
        plt.xlabel('time (s)')
        plt.ylabel('G (S)')
        for device in deviceList:
            df1 = self.df[self.df['device'] == device]
            plt.plot(df1['time'], df1['G'], color='C' + str(device), label=device, linestyle=linestyles[device % 4 - 1])
            plt.legend()

    def get_dead_devices(self, cutoff = 5e-6):
        deviceList = self.df.device.unique()
        deadList = []
        for device in deviceList:
            df1 = self.df[self.df['device'] == device]
            if df1['G'].max() < cutoff:
                deadList.append(device)
        return(deadList)

    def get_live_devices(self, cutoff = 5e-6):
        deviceList = self.df.device.unique()
        liveList = []
        for device in deviceList:
            df1 = self.df[self.df['device'] == device]
            if df1['G'].max() > cutoff:
                liveList.append(device)
        return(liveList)

################Functions########################

def get_live_devices(df, cutoff = 5e-6):
    deviceList = df.device.unique()
    liveList = []
    for device in deviceList:
        df1 = df[df['device'] == device]
        if df1['G'].max() > cutoff:
            liveList.append(device)
    return(liveList)

def get_dead_devices(df, cutoff = 5e-6):
    deviceList = df.device.unique()
    deadList = []
    for device in deviceList:
        df1 = df[df['device'] == device]
        if df1['G'].max() < cutoff:
            deadList.append(device)
    return(deadList)

def plot_all(df, title = 'MSM04', cutoff = 1E-5, save = True, basepath = 'G:/Shared drives/Nanoelectronics Team Drive/Data/2021/Marta/Noise measurements - June 1st week/Fishtank/MSM04_realbufferpH7_topH4'):
    #deviceList = df.device.unique()
    dfa = get_G_average(df)

    liveDevices = get_live_devices(df, cutoff=cutoff)
    deadDevices = get_dead_devices(df, cutoff=cutoff)

    linestyles = ['-', '--', '-.', ':']
    plt.style.use('seaborn')
    centimetre = 1 / 2.54
    color = iter(cm.tab20(np.linspace(0, 1, len(liveDevices)))) #change 46 to i

    fig, ax1 = plt.subplots(figsize=(30*centimetre, 20*centimetre))
    plt.subplots_adjust(left=None, bottom=None, right=0.8, top=None, wspace=None, hspace=None)

    G_mean = dfa.G[dfa.device.isin(liveDevices)].mean()
    G_std = dfa.G_std[dfa.device.isin(liveDevices)].mean()
    add_text = 'G_mean_live = ' + '{:.2E}'.format(G_mean) + '\n' + 'G_mean_std_live = ' + '{:.2E}'.format(G_std)
    ax1.text(1.03, 0.0, add_text, transform=ax1.transAxes)

    ax1.set_title(title)
    ax1.set(xlabel = 'time (s)', ylabel='G (S)')
    for i, device in enumerate(liveDevices):
        df1 = df[df['device'] == device]
        ax1.plot(df1['time'], df1['G'], color=next(color), label=device, linestyle=linestyles[i % 4 - 1])
        ax1.legend(ncol=2, loc=9, bbox_to_anchor=(1.13, 1.0))

    for device in deadDevices:
        df1 = df[df['device'] == device]
        ax1.plot(df1['time'], df1['G'], color= 'gray', label=device, linestyle='-')
        ax1.legend(ncol=2, loc=9, bbox_to_anchor=(1.13, 1.0))

    if save == True:
        save_at = basepath + '/summary.png'
        fig.savefig(save_at)

def get_G_average(df):
    deviceList = df.device.unique()
    ResultsDF = pd.DataFrame()
    for device in deviceList:
        df1 = df[df['device'] == device]
        #print(df1)
        ResultsDF = ResultsDF.append({'device': device, 'G': df1.G.mean(), 'G_std': df1.G.std(),
                                      'G_sterr': df1.G.sem()}, ignore_index=True)
    return ResultsDF

def check_values(df, R_ev = 1e3, type = 'top', tol = 0.1, rel_std = 0.005, R_zero_tol = 1e6, zero_std_tol = 1e6,
                 save = False, basePath = 'G:/Shared drives/Nanoelectronics Team Drive/Data/2021/Marta/test'):

    completeReport = ('R expected: ' + str(R_ev) + 'Ohm \n' +
                    'type: ' + str(type) + '\n' +
                      'tol = ' + str(tol) + '\n' +
                      'rel std = ' + str(rel_std) + '\n' +
                      'R_zero_tol = '+ str(R_zero_tol) + '\n' +
                      'base path = ' + basePath + '\n \n')

    ev = 1/(R_ev+100) #100 ohm internal resistance of multiplexer
    zero_tol = 1/R_zero_tol

    topDevices = [i for i in range(1, 12 + 1)] + [i for i in range(24, 34 + 1)]
    bottomDevices = [i for i in range(13, 23 + 1)] + [i for i in range(35, 46 + 1)]
    allDevices = topDevices + bottomDevices

    dfa = get_G_average(df)

    G_OK = []
    noise_OK = []
    G_bad = []
    noise_bad = []

    if type == 'top':
        liveDevices = topDevices
        deadDevices = bottomDevices
    elif type == 'bottom':
        liveDevices = bottomDevices
        deadDevices = topDevices
    elif type == 'all':
        liveDevices = allDevices
        deadDevices = []

    # check live devices
    for device in liveDevices:
        G = float(dfa.G.loc[dfa.device == device])
        std = float(dfa.G_std.loc[dfa.device == device])
        if (G*(1+tol) > ev) & (G*(1-tol) < ev):
            G_OK.append(device)
        else:
            G_bad.append(device)
        if (std/G < rel_std):
            noise_OK.append(device)
        else:
            noise_bad.append(device)

    G_a_live = dfa.G[dfa.device.isin(G_OK)].mean()
    STD_a_live = dfa.G_std[dfa.device.isin(G_OK)].mean()

    report_c = ('G average of devices within range =  ' + str(G_a_live) + ' S \n' +
              'STD average of devices within range =  ' + str(STD_a_live) + ' S \n \n' +
              'Report for connected devices = ' + str(liveDevices) + '\n' 
              'G within range for devices: ' + str(G_OK) + '\n' 
              'G out of range for devices: ' + str(G_bad) + '\n'
              'noise within range for devices: ' + str(noise_OK) + '\n'
              'noise out of range range for devices: ' + str(noise_bad) + '\n \n'
          )
    #print(report_c)
    #check disconnected devices
    completeReport = completeReport + report_c

    G_OK = []
    noise_OK = []
    G_bad = []
    noise_bad = []
    for device in deadDevices:
        G = float(dfa.G.loc[dfa.device == device])
        std = float(dfa.G_std.loc[dfa.device == device])
        if (G < zero_tol) & (G*tol < zero_tol):
            G_OK.append(device)
        else:
            G_bad.append(device)
        if (std/G < zero_std_tol):
            noise_OK.append(device)
        else:
            noise_bad.append(device)

    if type != 'all':
        G_a_live = dfa.G[dfa.device.isin(G_OK)].mean()
        STD_a_live = dfa.G_std[dfa.device.isin(G_OK)].mean()
        #print('G average of disconnected devices within range =  ' + str(G_a_live) + ' S')
        #print('STD average of disconnected devices within range =  ' + str(STD_a_live) + ' S')

        report_d = ('G average of disconnected devices within range =  ' + str(G_a_live) + ' S \n'+
                    'STD average of disconnected devices within range =  ' + str(STD_a_live) + ' S \n \n' +
                    'Report for disconnected devices = ' + str(deadDevices) + '\n' 
                    'G within range for devices: ' + str(G_OK) + '\n'
                    'G out of range for devices: ' + str(G_bad) + '\n'
                    'noise within range for devices: ' + str(noise_OK) + '\n'
                    'noise out of range range for devices: ' + str(noise_bad) + '\n'
              )
        completeReport = completeReport + report_d

    print(completeReport)

    if save == True:
        dfa.to_csv(basePath + '/dfa.csv')
        print('saved dfa')

        with open(basePath + '/testchip_summary.txt', 'w') as f:
            f.write(completeReport)

    return dfa

def check_noise(df, basePath = 'G:/Shared drives/Nanoelectronics Team Drive/Data/2021/Marta/test'):
    dfa = get_G_average(df)
    print(dfa.G_std.mean())
    #return (dfa.G_std)

if __name__ == "__main__":
    S = ResultsDF()
    S.plot_all()
    print('ok')


   #print(S.get_dead_devices())
    #for github