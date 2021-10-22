import subprocess
import re

cmd = ["ioreg", "-c", "AppleSmartBattery"]

output = str(subprocess.check_output(cmd)).split("\\n")

for o in output:
    if '"BatteryInstalled" =' in o:
        installed = "Yes" in o
if installed:
    for o in output:
        if '"DesignCapacity" =' in o:
            designcapacity = int(re.sub("\\D", "", o))
        elif '"CurrentCapacity" =' in o:
            currentcapacity = int(re.sub("\\D", "", o))
        elif '"MaxCapacity" =' in o:
            maxcapacity = int(re.sub("\\D", "", o))
        elif '"ExternalConnected" =' in o:
            external = "Yes" in o
        elif '"IsCharging" =' in o:
            charging = "Yes" in o
        elif '"FullyCharged" =' in o:
            fullycharged = "Yes" in o
        elif '"Voltage" =' in o:
            voltage = int(re.sub("\\D", "", o))

    if fullycharged:
        print("充電完了")
    elif charging:
        print("充電中")
    elif external:
        print("電源接続中。充電していません")
    else:
        print("充電していません")
    print("%.1f V" % (voltage/1000), "%.1f Wh" % ((currentcapacity/1000)*(voltage/1000)))
    print("Remain: %.1f%% (%d/%d)" % (currentcapacity/maxcapacity*100, currentcapacity, maxcapacity))
    print("AttritionRate: %.1f%% (%d/%d)" % (maxcapacity/designcapacity*100, maxcapacity, designcapacity))
else:
    print("バッテリーを搭載していません。")