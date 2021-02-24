import pandas as pd
import easygui
import matplotlib.pyplot as plt
class ResultsDF:

#comment for github
# Jaccl commits
    def __init__(self, name = 'unnamed'):
        self.file = easygui.fileopenbox().replace('\\', '/')
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
        deadList = []
        for device in deviceList:
            df1 = self.df[self.df['device'] == device]
            if df1['G'].max() > cutoff:
                deadList.append(device)
        return(deadList)

if __name__ == "__main__":
    S = ResultsDF('sample_A')
    print(S.df.head())
    S.plot_all()