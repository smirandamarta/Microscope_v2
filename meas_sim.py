import pandas as pd
import pyneMeas.Instruments as I
import pyneMeas.utility as U
from pi_control import PiMUX
import pandas as pd
import janUtils as jan
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import easygui
from datetime import datetime
from pathlib import Path
from matplotlib.pyplot import cm
import numpy as np
from eval import *

def plot_all_live_add_legend(ax1):
    ax1.legend(ncol=2, loc=9, bbox_to_anchor=(1.13, 1.0))
    print('added legend')

def plot_all_live(df, deviceList, fig, ax1, title='sample name', cutoff=1E-5, label=False):

        legend = False
        first_legend = True
        if deviceList == list(df.device) and first_legend == True:
            legend = True
            print('now')

        dfa = get_G_average(df)

        liveDevices = get_live_devices(df, cutoff=cutoff)
        print(liveDevices)
        deadDevices = get_dead_devices(df, cutoff=cutoff)

        linestyles = ['-', '--', '-.', ':']
        color = iter(cm.tab20(np.linspace(0, 1, len(liveDevices))))  # change 46 to i

        G_mean = dfa.G[dfa.device.isin(liveDevices)].mean()
        G_std = dfa.G_std[dfa.device.isin(liveDevices)].mean()
        add_text = 'G_mean_live = ' + '{:.2E}'.format(G_mean) + '\n' + 'G_mean_std_live = ' + '{:.2E}'.format(G_std)
        t1 = ax1.text(1.03, 0.0, add_text, transform=ax1.transAxes)
        t1.set_text(str(add_text))

        ax1.set_title(title)
        ax1.set(xlabel='time (s)', ylabel='G (S)')

        for i, device in enumerate(liveDevices):
            df1 = df[df['device'] == device]
            if label == True:
                ax1.plot(df1['time'], df1['G'], color=next(color), label=device, linestyle=linestyles[i % 4 - 1])
            if label == False:
                ax1.plot(df1['time'], df1['G'], color=next(color), linestyle=linestyles[i % 4 - 1])
            print(legend)
        if legend == True and device == liveDevices[-1]:
            print(str(device) + str(liveDevices[-1]))
            print('now')
            #ax1.legend(ncol=2, loc=9, bbox_to_anchor=(1.13, 1.0))
            legend = False
        for device in deadDevices:
            df1 = df[df['device'] == device]
            ax1.plot(df1['time'], df1['G'], color='gray', label=device, linestyle='-')
            #if legend == True:
            #    ax1.legend(ncol=2, loc=9, bbox_to_anchor=(1.13, 1.0))

        legend = False

        plt.pause(0.01)  # needed for live plotting to work
        return legend

def simulate_measurement(deviceList=[i for i in range(10)], repeats = 1, delay = 0.1, plot_speed=1):

    add_legend = True
    MasterDF = pd.DataFrame(
        columns=['ID', 'repeat', 'time', 'datetime', 'device', 'V_SD', 'I_SD', 'G', 'std_err'])  # Sets up results table
    t0 = time.time()  # gets time

    V_SD = np.arange(0, -0.6, -0.1)
    ID = 1

    plt.style.use('seaborn')
    centimetre = 1 / 2.54

    fig, ax1 = plt.subplots(figsize=(30 * centimetre, 20 * centimetre))
    plt.subplots_adjust(left=None, bottom=None, right=0.8, top=None, wspace=None, hspace=None)

    for j in range(repeats):
        for i, device in enumerate(deviceList):
            I_SD = V_SD + np.random.random(V_SD.shape[0])*0.1
            df = pd.DataFrame({'V_SD': V_SD, 'I_SD': I_SD})

            Params = {'ID': [ID], 'repeat': [j], 'time': [time.time()], 'datetime': [datetime.now()],
                      'device': [device], 'V_SD': [list(V_SD)],
                      'I_SD': [list(I_SD)]}  # inserts data for results table
            #print(str(Params['ID']) + ' + ' + str(j))  # prints status to console
            MasterDF = jan.merge(Params, jan.fit_for_Master(df, 'V_SD', 'I_SD'), MasterDF)
            ID += 1
            time.sleep(delay)

            if i%plot_speed == 0:
                if len(MasterDF.device.unique()) < len(deviceList):
                    plot_all_live(MasterDF, deviceList=deviceList, fig=fig, ax1=ax1, label=False)
                else:
                    plot_all_live(MasterDF, deviceList=deviceList, fig=fig, ax1=ax1, label=True)

                    if add_legend == True:
                        plot_all_live_add_legend(ax1)
                        add_legend = False

    return MasterDF

if __name__ == '__main__':
    t0 = time.time()
    df = simulate_measurement(repeats=10, delay= 0.1, plot_speed=5)
    t1 = time.time()
    print(t1-t0)
    plot_all(df)