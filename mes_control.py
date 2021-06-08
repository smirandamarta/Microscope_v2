import pandas as pd
import pyneMeas.Instruments as I
import pyneMeas.utility as U
from pi_control import PiMUX
import pandas as pd
import janUtils as jan
import time
import matplotlib.pyplot as plt
import easygui
from datetime import datetime


if __name__ == '__main__':

    # 1. set parameters
    Pi_IP_address = '129.94.163.203' # USER INPUT get IP address from mobile hotspot settings 129.94.163.203 for OMB
    currentVoltagePreAmp_gain = 1E3 # USER INPUT Femto current preamplifier gain

    start_sd = 0.0 # USER INPUT start value for IV sweep
    end_sd = -0.5 # USER INPUT end value for IV sweep
    step_sd = 0.1 # USER INPUT step size for IV sweep
    V_SD = U.targetArray([start_sd,end_sd,start_sd],stepsize=step_sd) #creates array of V_sd value for voltage sweep

    # Number of and delay between cycles measuring all devices
    repeats = 20   # USER INPUT number of IV curves measured per device
    delay = 0 # USER INPUT delay between sets of IV measurements - measure all devices -> delay -> measure all devices
    basePath  = easygui.diropenbox().replace('\\', '/') # opens window to select folder for data to be saved
    fileName = 'MSM04_realbufferpH7_topH4' # USER INPUT file name

    deviceList = [i for i in range(1,47)] # USER INPUT enter all devices you want to measure

    # 2.Define device/instruments
    my_Pi = PiMUX(IP = Pi_IP_address) # sets up raspberry pi

    daqout_S = I.USB6216Out(0,usbPort = 'Dev2') # sets up NIDAQ
    daqout_S.setOptions({
        "feedBack":"Int",
        "extPort":6, # Can be any number 0-7 if in 'Int'
        "scaleFactor":1
    })
    daqin_D = I.USB6216In(2,usbPort='Dev2') #sets up NIDAQ
    daqin_D.set('scaleFactor',currentVoltagePreAmp_gain) # sets up NIDAQ to work with the current preamp

    my_Pi.setMuxToOutput(0) # sets multiplexer to state with all outputs off

    myTime = I.TimeMeas()  # gets time
    Dct = {} # sets up IV sweep including where to save the files
    Dct['basePath'] = basePath
    Dct['fileName'] = fileName
    Dct['setters'] = {daqout_S: 'V_SD'}
    Dct['readers'] = {myTime:  'time',
                      daqin_D: 'I_SD'}
    Dct['sweepArray'] = V_SD

    MasterDF = pd.DataFrame(columns = ['ID', 'repeat', 'time', 'datetime', 'device', 'V_SD', 'I_SD', 'G', 'std_err']) #Sets up results table
    t0 = time.time() # gets time

    # Starting the measurement
    addlegend = True # variable used to make sure the legend only gets added once to realtime plot
    linestyles = ['-', '--', '-.', ':'] # list used to altenate between line styles for different devices

    for j in range(repeats):
        for device in deviceList:
            my_Pi.setMuxToOutput(device) # sets multiplexer to the desired device
            time.sleep(0.5) # short wait to settle. May not be necessary. Can investigate later
            time_1 = time.time() - t0 # Gets time relative to start time of the measurement
            df = U.sweep(Dct) # Perform IV sweep using the NIDAQ pyne module
            Params = {'ID': [U.readCurrentID()], 'repeat': j, 'time': [time_1], 'datetime': [datetime.now()], 'device': [device], 'V_SD': [list(df['V_SD'])],
                      'I_SD': [list(df['I_SD'])]} # inserts data for results table
            print(str(Params['ID']) + ' + ' + str(j)) # prints status to console
            MasterDF = jan.merge(Params, jan.fit_for_Master(df,'V_SD','I_SD'), MasterDF) # Performs linear fit of IV sweep to get G and adds G to result table
            df1 = MasterDF[MasterDF['device'] == device] # creates dataframe with just one device to plot as a distinct line in live plot
            # live plotting. Adding legend on first repeat zero
            if addlegend == True:
                plt.plot(df1['time'], df1['G'], color='C' + str(device), label=device, linestyle=linestyles[device%4-1])
                plt.legend()
            elif addlegend == False:
                plt.plot(df1['time'], df1['G'], color='C' + str(device), label=device, linestyle=linestyles[device%4-1])
            plt.pause(0.01) # needed for live plotting to work
        addlegend = False
        time.sleep(delay) # delay set by user input

    my_Pi.setMuxToOutput(0)  # sets multiplexer to 0

    MasterDF.to_csv(basePath + '/' + fileName + '.csv') # save results table after each repeat

    MasterDF.to_csv(basePath+'/'+fileName+str(Params['ID'])+'.csv') #save final results table with ID of the last sweep.

    for device in deviceList: # saves result tables for individual devices
        df_ind = MasterDF[MasterDF['device'] == device]
        df_ind.to_csv(basePath+ '/'+ fileName +'_device_' + str(device)+'.csv')
