import csv
import yaml
import datetime

# CSV Format:
# Zeitstempel, Bezug, Einspeisung, PV-Produktion, LP1, LP2, LP3,LP-Gesamt, Speicher- Import, Speicher-Export, Verbraucher 1, Verbraucher 1 Expoert, Verbraucher 2, Verbraucher 2 Export, Verbraucher 3, LP4, LP5, LP6, LP7, LPÜ8, Speicher SoC, SoC-LP1, SoC LP2, Temp1, Temp2, Temp3,, Smarthomedevic3e1 .... SMHD10, Temp4, Temp 5, Temp6


def SplitString(string, length):
    return (string[0+i:length+i] for i in range(0, len(string), length))

def TS2Hours(time1, time2):
    EndTime = list(SplitString(time1, 2))
    StartTime = list(SplitString(time2, 2))
    return ((float(EndTime[0]) - float(StartTime[0])) + (float(EndTime[1]) - float(StartTime[1]))/60)

class CSystem:
    def __init__(self, PVpeak, BatteryCappacity, MaxCharge, MaxDischarge):
        self.PVpeak = int(PVpeak)
        self.BatteryCappacity = int(BatteryCappacity)
        self.MaxCharge = int(MaxCharge)
        self.MaxDischarge = int(MaxDischarge)

class CState:
    def __init__ (self):
        self.Bezug = 0
        self.Einspeisung = 0
        self.PV = 0
        self.LP = 0
        self.BatteryImport = 0
        self.BatteryExport = 0
        self.BatteryState = 0

class CLogLine:
    def __init__ (self):
        self.TS = ""
        self.Bezug = 0
        self.Einspeisung = 0
        self.PV = 0
        self.LP1 = 0
        self.LP2 = 0
        self.LP3 = 0
        self.LPGesamt = 0
        self.SpeicherImport = 0
        self.SpeicherExport = 0
        self.Verbraucher1 = 0
        self.Verbraucher1Export = 0
        self.Verbraucher2 = 0
        self.Verbraucher2Export = 0
        self.Verbraucher3 = 0
        self.LP4 = 0
        self.LP5 = 0
        self.LP6 = 0
        self.LP7 = 0
        self.LP8 = 0
        self.SpeicherSoC = 0
        self.SoCLP1 = 0
        self.SoCLP2 = 0
        self.Temp1 = 0
        self.Temp2 = 0
        self.Temp3 = 0
        self.SHD1 = 0
        self.SHD2 = 0
        self.SHD3 = 0
        self.SHD4 = 0
        self.SHD5 = 0
        self.SHD6 = 0
        self.SHD7 = 0
        self.SHD8 = 0
        self.SHD9 = 0
        self.SMHD10 = 0
        self.Temp4 = 0
        self.Temp5 = 0
        self.Temp6 = 0
    def __init__ (self, row):
        self.TS = row[0]
        self.Bezug = float(row[1])
        self.Einspeisung = float(row[2])
        self.PV = float(row[3])
        self.LP1 = float(row[4])
        self.LP2 = float(row[5])
        self.LP3 = float(row[6])
        self.LPGesamt = float(row[7])
        self.SpeicherImport = float(row[8])
        self.SpeicherExport = float(row[9])
        self.Verbraucher1 = float(row[10])
        self.Verbraucher1Export = float(row[11])
        self.Verbraucher2 = float(row[12])
        self.Verbraucher2Export = float(row[13])
        self.Verbraucher3 = float(row[14])
        self.LP4 = float(row[15])
        self.LP5 = float(row[16])
        self.LP6 = float(row[17])
        self.LP7 = float(row[18])
        self.LP8 = float(row[19])
        self.SpeicherSoC = float(row[20])
        self.SoCLP1 = float(row[21])
        self.SoCLP2 = float(row[22])
        self.Temp1 = float(row[23])
        self.Temp2 = float(row[24])
        self.Temp3 = float(row[25])
        self.SHD1 = float(row[26])
        self.SHD2 = float(row[27])
        self.SHD3 = float(row[28])
        self.SHD4 = float(row[29])
        self.SHD5 = float(row[30])
        self.SHD6 = float(row[31])
        self.SHD7 = float(row[32])
        self.SHD8 = float(row[33])
        self.SHD9 = float(row[34])
        self.SMHD10 = float(row[35])
        self.Temp4 = float(row[36])
        self.Temp5 = float(row[37])
        self.Temp6 = float(row[38])

# Read Config File
config_file = 'config.yml'
with open(config_file, 'r') as file:
    config = yaml.safe_load(file)

print("Analysing logfiles")
print("Start: " + str(config['time']['start']))
print("End:   " + str(config['time']['end']))
print("")

FirstLog = 1
ZeroLine = 0
System = CSystem(config['PV']['peak'], config['battery']['cappacity'], config['battery']['max_charge_power'], config['battery']['max_discharge_power'])
State = CState()
StateStart = CState()
LastLine = CState()
day = config['time']['start']
#folder = "daily/"
folder = config['LogFolder']['Folder']
while (day <= config['time']['end']):
    FileName = folder + str(day.strftime("%Y")) + str(day.strftime("%m")) + str(day.strftime("%d")) + ".csv"
    #print ("Analysing logfile: " + FileName)
    day += datetime.timedelta(days=1)
    with open(FileName, newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            ActualLine = CLogLine(row)
            if FirstLog == 0:
                if ((ActualLine.Einspeisung != 0) or (ActualLine.Bezug != 0)):
                    # Calculation starts here
                    # Was there acutally PV feed to the power grid?
                    if ActualLine.Einspeisung > LastLine.Einspeisung:
                        # could the battery be charged
                        if State.BatteryState < System.BatteryCappacity:
                            # need to calculate time, as there are missing lines possible
                            ChargeTime = TS2Hours(ActualLine.TS, LastLine.TS)
                            ChargeEnergy = ActualLine.Einspeisung - LastLine.Einspeisung
                            ChargePower = ChargeEnergy/ChargeTime
                            Einspeisung = 0 # assuming no limit for battery
                            # limiting charge power
                            if ChargePower > System.MaxCharge:
                                ChargeEnergy = ChargeEnergy * System.MaxCharge / ChargePower
                                ChargePower = System.MaxCharge
                                Einspeisung = ActualLine.Einspeisung - LastLine.Einspeisung - ChargeEnergy
                            # limiting battery state, cant overcharge
                            if (System.BatteryCappacity - State.BatteryState) < ChargeEnergy:
                                ChargeEnergy = System.BatteryCappacity - State.BatteryState
                                Einspeisung = ActualLine.Einspeisung - LastLine.Einspeisung - ChargeEnergy
                            # Chargeing Limited to its limits, now we can aggregate the values
                            State.Einspeisung = State.Einspeisung + Einspeisung
                            State.BatteryImport = State.BatteryImport + ChargeEnergy
                            State.BatteryState = State.BatteryState + ChargeEnergy # TODO can put efficency here to reduce SoC
                            # TODO above add efficency to allow full charge, not limiting to max with charging, need to be max with carging*efficency
                        else:
                            # everything was feed to the power grid
                            State.Einspeisung = State.Einspeisung + ActualLine.Einspeisung - LastLine.Einspeisung
                    # was there actually energy from power grid
                    if ActualLine.Bezug > LastLine.Bezug:
                        # could energy from battery be used
                        if State.BatteryState > 0:
                            DischargeTime = TS2Hours(ActualLine.TS, LastLine.TS)
                            DischargeEnergy = ActualLine.Bezug - LastLine.Bezug
                            DischargePower = DischargeEnergy/DischargeTime
                            Bezug = 0 # assuming no limit for battery
                            # limit dicharge power
                            if DischargePower > System.MaxDischarge:
                                DischargeEnergy = DischargeEnergy * System.MaxDischarge / DischargePower
                                DischargePower = System.MaxDischarge
                                Bezug = ActualLine.Bezug - LastLine.Bezug - DischargeEnergy
                            # limiting battery state, cant discharge below zero SoC
                            if State.BatteryState < DischargeEnergy:
                                DischargeEnergy = State.BatteryState
                                Bezug = ActualLine.Bezug - LastLine.Bezug - DischargeEnergy
                            # Discharge Limited to its limits, now we can aggregate the values
                            State.Bezug = State.Bezug + Bezug
                            State.BatteryExport = State.BatteryExport + DischargeEnergy
                            State.BatteryState = State.BatteryState - DischargeEnergy
                        else:
                            # everything was used from power grid
                            State.Bezug = State.Bezug + ActualLine.Bezug - LastLine.Bezug
                else:
                    ZeroLine = 1
            else:
                StateStart.Einspeisung = ActualLine.Einspeisung
                StateStart.Bezug = ActualLine.Bezug
                StateStart.PV = ActualLine.PV
                StateStart.LP = ActualLine.LP1 + ActualLine.LP2 + ActualLine.LP3 + ActualLine.LP4 + ActualLine.LP5 + ActualLine.LP6 + ActualLine.LP7 + ActualLine.LP8
                StateStart.BatteryExport = ActualLine.SpeicherExport
                FirstLog = 0
            # check for Errors
            if ZeroLine == 0:
                LastLine = ActualLine
                Einspeisung = ActualLine.Einspeisung - StateStart.Einspeisung
                Bezug = ActualLine.Bezug - StateStart.Bezug
            else:
                ZeroLine = 0


StateEnd = CState()
StateEnd.Einspeisung = ActualLine.Einspeisung
StateEnd.Bezug = ActualLine.Bezug
StateEnd.PV = ActualLine.PV
StateEnd.LP = ActualLine.LP1 + ActualLine.LP2 + ActualLine.LP3 + ActualLine.LP4 + ActualLine.LP5 + ActualLine.LP6 + ActualLine.LP7 + ActualLine.LP8
StateEnd.BatteryExport = ActualLine.SpeicherExport
StateEnd.BatteryImport = ActualLine.SpeicherImport

Einspeisung = StateEnd.Einspeisung - StateStart.Einspeisung
Bezug = StateEnd.Bezug - StateStart.Bezug
PV_value = StateEnd.PV - StateStart.PV
LP_value = StateEnd.LP - StateStart.LP
BatteryImport = StateEnd.BatteryImport - StateStart.BatteryImport
BatteryExport = StateEnd.BatteryExport - StateStart.BatteryExport

print("")
print("Orignal Values:")
print("")
print("Einspeisung:    {:>15}" .format(Einspeisung) + " Wh")
print("Einspeisung:    {:>15}" .format(Einspeisung) + " Wh")
print("Bezug:          {:>15}" .format(Bezug) + " Wh")
print("PV:             {:>15}" .format(PV_value) + " Wh")
print("LP:             {:>15}" .format(LP_value) + " Wh")
print("Battery Import: {:>15}" .format(BatteryImport) + " Wh")
print("Battery Export: {:>15}" .format(BatteryExport) + " Wh")
print("")

# print result
print("New Values:")
print("Einspeisung:    {:>15}" .format(State.Einspeisung) + " Wh")
print("Bezug:          {:>15}" .format(State.Bezug) + " Wh")
print("PV:             {:>15}" .format(State.PV) + " Wh")
print("LP:             {:>15}" .format(State.LP) + " Wh")
print("Battery Import: {:>15}" .format(State.BatteryImport) + " Wh")
print("Battery Export: {:>15}" .format(State.BatteryExport) + " Wh")
print("")

# print difference
print("Reduced Energy usage from power grid: {:>15}" .format(StateEnd.Bezug - StateStart.Bezug - State.Bezug) + " Wh")
print("Reduced feed to the power grid:       {:>15}" .format(StateEnd.Einspeisung - StateStart.Einspeisung - State.Einspeisung) + " Wh")
print("Battery State at the end:             {:>15}" .format(State.BatteryState) + " Wh")
print("Checksum:                             {:>15}" .format(StateEnd.Bezug - StateStart.Bezug - State.Bezug - (StateEnd.Einspeisung - StateStart.Einspeisung - State.Einspeisung) + State.BatteryState) + " Wh")
