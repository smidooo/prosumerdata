

from datetime import datetime
import time, requests, json
import numpy as np

from apiKeys import *  # Keys for APIs are stored in this external file




def APICall(tstart, tnow, intervall):
    pageHome_ = Host+'data.json?id='+str(FeedNrHome)+'&start='+str(tstart)+'&end='+str(tnow)+'&interval='+str(int(intervall))+'&skipmissing=0'
    pageSol_ = Host+'data.json?id='+str(FeedNrSol)+'&start='+str(tstart)+'&end='+str(tnow)+'&interval='+str(int((intervall)))+'&skipmissing=0'
    pageHome = pageHome_+ApiKeyHome
    pageSol = pageSol_+ApiKeySol

    rH_ = requests.get(pageHome)
    rS_ = requests.get(pageSol)


    rH = json.loads(rH_.text)
    rS = json.loads(rS_.text)

    t = []
    E = []
    Es = []

    # ATTENTION: most recent values might result in "None" (i.e. noninteger values)

    for k in range(len(rH)):
        if type(rH[k][0]) is int and type(rH[k][1]) is int:
            t.append(rH[k][0]) # t in ms
            E.append(rH[k][1])
            Es.append(rS[k][1])


    dt = np.diff(t)[0]/1000.
    PH = np.diff(E)/dt*3600.*1e-3 #kW
    PS = np.diff(Es)/dt*3600.0*1e-3

    MeasuredData = {
         'time' : np.array(t)/1000., #'time in seconds'
         'Demand' : PH, # kW
         'Solar' : PS # kW
         }

    return MeasuredData

# test
tnow_ = time.mktime(datetime.now().timetuple()) - 60 * 20 #unix time in seconds
tnow = int(tnow_ * 1e3) #unix time in ms

tstart = int(tnow - 12 * 3600 * 1e3) # 12 hours in the past
intervall = 60

r = APICall(tstart, tnow, intervall)

Eprod = np.sum(r['Solar']*intervall/3600.) # in kWh

print('Produced last 12 hours (kWh) = ', Eprod)
