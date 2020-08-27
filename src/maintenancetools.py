import time
from debuglogger import DebugLogger
from config import Config
from driver.electrovalvedriver import ElectrovalveDriver
from driver.elpressdriver import ElPressDriver
from driver.pump11elitedriver import Pump11EliteDriver
from driver.redflowmeterdriver import RedFlowMeterDriver
from driver.temp18b20driver import TempDS18B20Driver
from driver.valvemxseries2driver import ValveMxSeries2Driver
from driver.alzarddriver import AlzardDriver

class MaintenanceTools:
    
    def __init__(self,
                 valve1: ElectrovalveDriver,
                 valve2: ElectrovalveDriver,
                 pressure: ElPressDriver,
                 pump: Pump11EliteDriver,
                 flowA: RedFlowMeterDriver,
                 flowB: RedFlowMeterDriver,
                 valve2x3: ValveMxSeries2Driver,
                 config: Config):
        # Initialize instruments' driver
        self.valve1 = valve1
        self.valve2 = valve2
        self.pressure = pressure
        self.pump = pump
        self.flowA = flowA
        self.flowB = flowB
        self.valve2x3 = valve2x3
       
    def purge_pump(self, cycles: int):
        for i in range(0, cycles):
            self.valve2x3.set_position_to_chambers()
            self.pump.set_infusion_rate(max(self.pump.get_infusion_rate_limits()))
            self.pump.infuse()
            while self.pump.is_moving:
                print("purge n°" + str(i))
                time.sleep(0.5)
            self.valve2x3.set_position_from_standards()
            self.pump.set_withdraw_rate(max(self.pump.get_withdraw_rate_limits()))            
            self.pump.withdraw()
            while self.pump.is_moving:
                print("refill n°" + str(i))
                time.sleep(0.5)
