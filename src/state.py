import threading
from time import sleep, time

from debuglogger import DebugLogger
from config import Config
from humdep import HumDep
from driver.humgendriver import HumgenDriver


class State:

    # State codes are binary in "reverse" order (LSB on the left, MSB on the right) to match Picarro's External Valve
    # Sequencer's order.
    state_codes = {"000": "manual",
                   "100": "air",
                   "010": "init_calib_step1",
                   "110": "init_calib_step2",
                   "001": "isocalib_stdA",
                   "101": "isocalib_stdB",
                   "011": "reset_calib",
                   "111": "humdep"}

    def __init__(self,
                 humgen: HumgenDriver,
                 humdep: HumDep,
                 config: Config,
                 debug_logger: DebugLogger,
                 object_id: str):
        self.humgen = humgen
        self.humdep = humdep

        # Initialize logger and config
        self.debug_logger = debug_logger
        self.object_id = object_id
        self.config = config

        # Initialize first state
        self.current_state = "---"
        self.to_state_air()

        # Initialize "listen to picarro code changes"
        self.listen_picarro = False

        # Launch thread: watch picarro code
        self.last_picarro_code = None
        thread_picarro_code = threading.Thread(target=self.__thread_watch_picarro_code__)
        thread_picarro_code.daemon = True
        thread_picarro_code.start()

    def to_state_air(self):
        self.current_state = "air"
        self.debug_logger.info(self.object_id, "Entering state: " + self.current_state)
        self.humdep.stop()
        self.humgen.pressure_pump_switch.unpower_output()
        self.humgen.valve1.close_valve()
        self.humgen.valve2.close_valve()
        self.humgen.valve2x3.set_position_to_chambers()
        self.humgen.pump.stop()
        self.humgen.flowA.set_control_fully_closed()
        self.humgen.flowB.set_control_fully_closed()
        self.humgen.pressure.set_flow(self.humgen.pressure.config.read("PRESSURE", "setpoint_mbar"))

    def to_state_manual(self):
        self.current_state = "manual"
        self.debug_logger.info(self.object_id, "Entering state: " + self.current_state)
        self.humdep.stop()
        self.humgen.pressure_pump_switch.unpower_output()
        self.humgen.valve1.close_valve()
        self.humgen.valve2.close_valve()
        self.humgen.valve2x3.set_position_to_chambers()
        self.humgen.pump.stop()
        self.humgen.flowA.set_control_fully_closed()
        self.humgen.flowB.set_control_fully_closed()
        self.humgen.pressure.set_flow(self.humgen.pressure.config.read("PRESSURE", "setpoint_mbar"))

    def to_state_init_calib_step1(self):
        self.current_state = "init_calib_step1"
        self.debug_logger.info(self.object_id, "Entering state: " + self.current_state)
        self.humdep.stop()
        self.humgen.pump.stop()
        self.humgen.valve2x3.set_position_to_chambers()
        self.humgen.flowA.set_control_fully_open()
        self.humgen.flowB.set_control_fully_open()
        self.humgen.valve1.open_valve()
        self.humgen.valve2.open_valve()
        self.humgen.pressure_pump_switch.power_output()
        self.humgen.pressure.set_flow(self.humgen.pressure.config.read("PRESSURE", "setpoint_mbar"))

    def to_state_init_calib_step2(self):
        self.current_state = "init_calib_step2"
        self.debug_logger.info(self.object_id, "Entering state: " + self.current_state)
        self.humdep.stop()
        infusion_rate = self.get_isocalib_boost_factor() * self.get_isocalib_rate()  # Infuse at a slighly higher rate to stabilize faster.
        self.humgen.pump.set_infusion_rate(infusion_rate)
        self.humgen.pump.infuse()
        self.humgen.valve2x3.set_position_to_chambers()
        self.humgen.flowA.set_control_digital_setpoint()
        self.humgen.flowA.set_setpoint_gas_flow(self.get_primary_flow())
        self.humgen.flowB.set_control_digital_setpoint()
        self.humgen.flowB.set_setpoint_gas_flow(self.get_primary_flow())
        self.humgen.valve1.open_valve()
        self.humgen.valve2.open_valve()
        self.humgen.pressure_pump_switch.power_output()
        self.humgen.pressure.set_flow(self.humgen.pressure.config.read("PRESSURE", "setpoint_mbar"))

    def to_state_isocalib_stdA(self):
        self.current_state = "isocalib_stdA"
        self.debug_logger.info(self.object_id, "Entering state: " + self.current_state)
        self.humdep.stop()
        self.humgen.pressure_pump_switch.power_output()        
        self.humgen.valve2x3.set_position_to_chambers()
        self.humgen.flowA.set_control_digital_setpoint()
        self.humgen.flowA.set_setpoint_gas_flow(self.get_primary_flow())
        self.humgen.flowB.set_control_digital_setpoint()
        self.humgen.flowB.set_setpoint_gas_flow(self.get_secondary_flow())
        self.humgen.valve1.open_valve()
        self.humgen.valve2.close_valve()
        self.humgen.pump.set_infusion_rate(self.get_isocalib_rate())
        self.humgen.pump.infuse()        
        self.humgen.pressure.set_flow(self.humgen.pressure.config.read("PRESSURE", "setpoint_mbar"))

    def to_state_isocalib_stdB(self):
        self.current_state = "isocalib_stdB"
        self.debug_logger.info(self.object_id, "Entering state: " + self.current_state)
        self.humdep.stop()
        self.humgen.pressure_pump_switch.power_output()        
        self.humgen.valve2x3.set_position_to_chambers()
        self.humgen.flowA.set_control_digital_setpoint()
        self.humgen.flowA.set_setpoint_gas_flow(self.config.read("STATE", "secondary_flow_sccm"))
        self.humgen.flowB.set_control_digital_setpoint()
        self.humgen.flowB.set_setpoint_gas_flow(self.get_primary_flow())
        self.humgen.valve1.close_valve()
        self.humgen.valve2.open_valve()
        self.humgen.pump.set_infusion_rate(self.get_isocalib_rate())
        self.humgen.pump.infuse()
        self.humgen.pressure.set_flow(self.humgen.pressure.config.read("PRESSURE", "setpoint_mbar"))

    def to_state_reset_calib(self):
        self.current_state = "reset_calib"
        self.debug_logger.info(self.object_id, "Entering state: " + self.current_state)
        self.humdep.stop()
        self.humgen.pressure_pump_switch.unpower_output()
        self.humgen.valve1.close_valve()
        self.humgen.valve2.close_valve()
        self.humgen.valve2x3.set_position_from_standards()
        self.humgen.pump.set_withdraw_rate(max(self.humgen.pump.get_withdraw_rate_limits()))
        self.humgen.pump.withdraw()
        self.humgen.flowA.set_control_fully_closed()
        self.humgen.flowB.set_control_fully_closed()
        self.humgen.pressure.set_flow(self.humgen.pressure.config.read("PRESSURE", "setpoint_mbar"))

    def to_state_humdep(self):
        self.current_state = "humdep"
        self.debug_logger.info(self.object_id, "Entering state: " + self.current_state)
        self.humgen.pressure.set_flow(self.humgen.pressure.config.read("PRESSURE", "setpoint_mbar"))
        self.humgen.pressure_pump_switch.power_output()
        self.humdep.launch()
        
    def get_current_state(self):
        return self.current_state

    def get_states(self):
        return list(self.state_codes.values())

    def __init_calib_common__(self):
        self.humgen.flowA.set_control_digital_setpoint()
        self.humgen.flowA.set_setpoint_gas_flow(self.humgen.calib_primary_flow)
        self.humgen.flowB.set_control_digital_setpoint()
        self.humgen.flowB.set_setpoint_gas_flow(self.humgen.calib_primary_flow)
        self.humgen.valve1.close_valve()
        self.humgen.valve2.close_valve()
        self.humgen.pressure.set_flow(self.config.read("PRESSURE", "setpoint_mbar"))

    def get_to_state_function(self, state_name: str):
        to_state_function = getattr(self, "to_state_" + state_name)
        return to_state_function

    def set_listen_picarro_code(self, listen: bool):
        self.listen_picarro = listen
        self.debug_logger.debug(self.object_id, "Listen to Picarro code changed to: " + str(self.listen_picarro))

    def get_listen_picarro_code(self) -> bool:
        return self.listen_picarro

    def get_isocalib_rate(self) -> float:
        return self.config.read("STATE", "isocalib_rate_ul_min")

    def set_isocalib_rate(self, rate: float):
        self.config.write("STATE", "isocalib_rate_ul_min", rate)

    def get_isocalib_boost_factor(self) -> float:
        return self.config.read("STATE", "isocalib_rate_boost_factor")

    def set_isocalib_boost_factor(self, factor: float):
        self.config.write("STATE", "isocalib_rate_boost_factor", factor)

    def get_primary_flow(self) -> float:
        return self.config.read("STATE", "primary_flow_sccm")

    def set_primary_flow(self, primary_flow: float):
        self.config.write("STATE", "primary_flow_sccm", primary_flow)

    def get_secondary_flow(self) -> float:
        return self.config.read("STATE", "secondary_flow_sccm")

    def set_secondary_flow(self, secondary_flow: float):
        self.config.write("STATE", "secondary_flow_sccm", secondary_flow)

    def __thread_watch_picarro_code__(self):
        while True:
            if self.listen_picarro:
                current_picarro_code = self.humgen.picarro_code.get_record()["code"]
                if current_picarro_code != self.last_picarro_code:
                    if current_picarro_code not in self.state_codes.keys():
                        self.debug_logger.error(self.object_id,
                                                "State code not valid: " + str(current_picarro_code))
                    else:
                        new_state_name = self.state_codes[current_picarro_code]
                        to_state_function = self.get_to_state_function(new_state_name)
                        to_state_function()
                    self.last_picarro_code = current_picarro_code
            sleep(0.5)

    def on_exit(self):
        """Actions to be performed when the Python program exits."""
        self.to_state_air()