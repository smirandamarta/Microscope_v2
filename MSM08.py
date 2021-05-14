from eval import *

S = ResultsDF('sample_A')
print(S.df.head())

#drop dead devices and cut off beginning
S.df = S.df.loc[(S.df.time > 500)]
liveList = S.get_live_devices(cutoff=1e-5)
S.df = S.df.loc[(S.df.device.isin(liveList))]

#split into 3 data frames
df1 = S.df.loc[(S.df.time > 500) & (S.df.repeat < 45) & (S.df.device.isin(liveList))]
df2 = S.df.loc[(S.df.repeat > 45) & (S.df.repeat < 89) & (S.df.device.isin(liveList))]
df3 = S.df.loc[(S.df.repeat > 90) & (S.df.device.isin(liveList))]

#Get G average for each device
av1 = get_G_average(df1)
av2 = get_G_average(df2)
av3 = get_G_average(df3)

#percentage
pChange = pd.DataFrame()
for device in liveList:
    dt1 = av1[av1.device == device]
    dt2 = av2[av2.device == device]
    dt3 = av3[av3.device == device]
    pChange = pChange.append({'device': device, 'PH7_1': dt1.G.mean(), 'PH4': dt2.G.mean(), 'PH7_2': dt3.G.mean()}, ignore_index=True)

pChange['start'] = pChange.PH7_1/pChange.PH7_1
pChange['7to4'] = pChange.PH4/pChange.PH7_1
pChange['4to7'] = pChange.PH7_2/pChange.PH7_1

pChange['abs7to4'] = pChange.PH4 - pChange.PH7_1


# Figure percentage change

pC = (pChange['7to4']-1)*100
aC = pChange['abs7to4']

print(av1.G.mean())
print(av2.G.mean())
print(av3.G.mean())

#Figures show

plt.style.use('seaborn')
cm = 1/2.54
fig1, ((ax1, ax2), (ax3, ax4)) = plt.subplots(ncols=2, nrows=2, figsize=(20*cm, 20*cm))
ax1.set_title('individual devices')
ax2.set_title('all devices box plot')
ax3.set_title('relative change distribution')
ax4.set_title('absolute change distribution')

#F1
deviceList = av1.device.unique()
linestyles = ['-', '--', '-.', ':']
#plt.figure(num = str(self.name)+'_all')
#x1.set_xlabel('PH')
#ax1.set_ylabel('G (S)')
for device in deviceList:
    x = ['PH7a', 'PH4', 'PH7b']
    y = [float(av1.G[av1.device == device]), float(av2.G[av2.device == device]), float(av3.G[av3.device == device])]
    yerr = [float(av1.G_sterr[av1.device == device]), float(av2.G_sterr[av2.device == device]), float(av3.G_sterr[av3.device == device])]
    ax1.errorbar(x, y, yerr= yerr)
    #plt.legend()
ax1.set_ylabel('G (S)')

#F2

x = ['PH7a', 'PH4', 'PH7b']
y = [av1.G, av2.G, av3.G]
ax2.violinplot(y, showmeans=True)
ax2.set_xlim([0, 4])
ax2.set_xticks([1,2,3])
ax2.set_xticklabels(labels=x)
ax2.set_ylabel('G (S)')

#F3

ax3.hist(pC)
ax3.set_xlabel('G change from PH7a to PH4 (%)')
ax3.set_ylabel('number of devices')

#F4

ax4.hist(aC)
ax4.set_xlabel('G change from PH7a to PH4 (S)')
ax4.set_ylabel('number of devices')

plt.show()
