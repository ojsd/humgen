from debuglogger import DebugLogger
from config import Config
from driver.electrovalvedriver import ElectrovalveDriver
from driver.elpressdriver import ElPressDriver
from driver.relaydriver import RelayDriver
from driver.pump11elitedriver import Pump11EliteDriver
from driver.redflowmeterdriver import RedFlowMeterDriver
from driver.valvemxseries2driver import ValveMxSeries2Driver
from driver.alzarddriver import AlzardDriver


class HumgenDriver:
    """
    Driver for the HumidityGenerator instrument as a whole.
    """

    def __init__(self,
                 valve1: ElectrovalveDriver,
                 valve2: ElectrovalveDriver,
                 pressure_pump_switch: RelayDriver,
                 pressure: ElPressDriver,
                 pump: Pump11EliteDriver,
                 flowA: RedFlowMeterDriver,
                 flowB: RedFlowMeterDriver,
                 valve2x3: ValveMxSeries2Driver,
                 picarro_code: AlzardDriver,
                 config: Config,
                 debug_logger: DebugLogger,
                 object_id: str):
        # Initialize logger
        self.debug_logger = debug_logger
        self.object_id = object_id
        self.config = config

        # Initialize intruments' driver
        self.valve1 = valve1
        self.valve2 = valve2
        self.pressure_pump_switch = pressure_pump_switch
        self.pressure = pressure
        self.pump = pump
        self.flowA = flowA
        self.flowB = flowB
        self.valve2x3 = valve2x3
        self.picarro_code = picarro_code

        # Initialize variables
        self.isocalib_rate = config.read("STATE", "isocalib_rate_ul_min")
        self.calib_primary_flow = config.read("STATE", "primary_flow_sccm")
        self.calib_secondary_flow = config.read("STATE", "secondary_flow_sccm")

    def set_stdA_flow_path(self, primary_flow: float = None, secondary_flow: float = None):
        # Initialize dry air flow rates: either from param or from config file
        if primary_flow is None:
            primary_flow = self.config.read("STATE", "primary_flow_sccm")
        if secondary_flow is None:
            secondary_flow = self.config.read("STATE", "secondary_flow_sccm")

        self.valve2x3.set_position_to_chambers()
        self.flowA.set_control_digital_setpoint()
        self.flowA.set_setpoint_gas_flow(primary_flow)
        self.flowB.set_control_digital_setpoint()
        self.flowB.set_setpoint_gas_flow(secondary_flow)
        self.valve1.open_valve()
        self.valve2.close_valve()
        self.pressure.set_flow(self.config.read("PRESSURE", "setpoint_mbar"))

    def set_stdB_flow_path(self, primary_flow: float = None, secondary_flow: float = None):
        # Initialize dry air flow rates: either from param or from config file
        if primary_flow is None:
            primary_flow = self.config.read("STATE", "primary_flow_sccm")
        if secondary_flow is None:
            secondary_flow = self.config.read("STATE", "secondary_flow_sccm")

        self.valve2x3.set_position_to_chambers()
        self.flowA.set_control_digital_setpoint()
        self.flowA.set_setpoint_gas_flow(secondary_flow)
        self.flowB.set_control_digital_setpoint()
        self.flowB.set_setpoint_gas_flow(primary_flow)
        self.valve1.close_valve()
        self.valve2.open_valve()
        self.pressure.set_flow(self.config.read("PRESSURE", "setpoint_mbar"))
