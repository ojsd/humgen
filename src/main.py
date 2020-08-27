import sys
import threading
from PyQt5.QtWidgets import QApplication

from gui.mainwindow import MainWindow
from uim.elpressuim import ElPressUim
from uim.pressurepumpuim import PressurePumpUim
from uim.pump11eliteuim import Pump11EliteUim
from uim.redflowmeteruim import RedFlowMeterUim
from uim.temperaturecavityuim import TemperatureUim
from uim.valvemxseries2uim import ValveMxSeries2Uim
from uim.electrovalveuim import ElectrovalveUim
from uim.picarrocodeuim import PicarroCodeUim
from uim.stateuim import StateUim
from uim.maintenancetoolsuim import MaintenanceToolsUim
from uim.debugloguim import DebuglogUim

from driver.electrovalvedriver import ElectrovalveDriver
from driver.elpressdriver import ElPressDriver
from driver.pump11elitedriver import Pump11EliteDriver
from driver.redflowmeterdriver import RedFlowMeterDriver
from driver.temp18b20driver import TempDS18B20Driver
from driver.temperaturedriver import TemperatureDriver
from driver.valvemxseries2driver import ValveMxSeries2Driver
from driver.alzarddriver import AlzardDriver
from driver.humgendriver import HumgenDriver
from driver.relaydriver import RelayDriver

from datalogger import DataLogger
from debuglogger import DebugLogger
from config import Config
from state import State
from humdep import HumDep
from maintenancetools import MaintenanceTools


# Enable/disable all drivers, for debug purpose.
general_enabled = True

########################################################################################################################
# DEBUG LOGGER
########################################################################################################################
debug_logger = DebugLogger("debug")

########################################################################################################################
# CONFIG
########################################################################################################################
config = Config("settings.ini")


########################################################################################################################
# INSTRUMENT DRIVERS
########################################################################################################################

# Valves
valve1 = ElectrovalveDriver(general_enabled, debug_logger, object_id="E_VALVE1", config=config)
valve2 = ElectrovalveDriver(general_enabled, debug_logger, object_id="E_VALVE2", config=config)

# Pressure controller
pressure_product = config.read("PRESSURE", "serial_product_name")
pressure = ElPressDriver(general_enabled, pressure_product, debug_logger=debug_logger, object_id="PRESSURE", config=config)

# Switch for pressure pump
pressure_pump_switch = RelayDriver(general_enabled, debug_logger, object_id="P_SWITCH", config=config)

# Syringe pump
# /!\ Product may be "Syringe Pump" or "Pico Elite" depending on firmware version!
pump_product = config.read("PUMP", "serial_product_name")
pump = Pump11EliteDriver(general_enabled, pump_product, debug_logger, object_id="PUMP", config=config)

# Valve
valve_product = config.read("VALVE2x3", "serial_product_name")
valve2x3 = ValveMxSeries2Driver(general_enabled, valve_product, debug_logger, object_id="VALVE2x3", config=config)

# Flow meters
flow_com_lock = threading.Lock()
flowA = RedFlowMeterDriver(general_enabled,
                           product=config.read("FLOW_A", "serial_product_name"),
                           debug_logger=debug_logger,
                           object_id="FLOW_A",
                           com_lock=flow_com_lock,
                           address=int(config.read("FLOW_A", "address")))
flowB = RedFlowMeterDriver(general_enabled,
                           product=config.read("FLOW_B", "serial_product_name"),
                           debug_logger=debug_logger,
                           object_id="FLOW_B",
                           com_lock=flow_com_lock,
                           address=int(config.read("FLOW_B", "address")))

# Picarro code
picarro_code = AlzardDriver(general_enabled, debug_logger, object_id="P_CODE", config=config)

# Temperature
temperature_sensor = TempDS18B20Driver(general_enabled, debug_logger, object_id="T_SENSOR", config=config)
temperature_switch = RelayDriver(general_enabled, debug_logger, object_id="T_SWITCH", config=config)
temperature = TemperatureDriver(temperature_switch, temperature_sensor, debug_logger, object_id="TEMPCTRL", config=config)

# Humgen
humgen = HumgenDriver(valve1, valve2, pressure_pump_switch, pressure, pump, flowA, flowB, valve2x3, picarro_code,
                      config, debug_logger, object_id="HUMGEN")

# HumDep
humdep = HumDep(humgen, config, debug_logger, "HUMDEP")

# State
state = State(humgen, humdep, config, debug_logger, object_id="STATE")

# MaintenanceTools
maintenancetools = MaintenanceTools(valve1, valve2, pressure, pump, flowA, flowB, valve2x3, config)


########################################################################################################################
# WINDOWS
########################################################################################################################

app = QApplication(sys.argv)
main_window = MainWindow(state, temperature)
main_window_ui = main_window.get_main_ui()
pump_ui = main_window.get_pump_ui()
electrovalve_ui = main_window.get_electrovalve_ui()
flow_ui = main_window.get_flow_ui()
pressure_ui = main_window.get_pressure_ui()
valve2x3_ui = main_window.get_valve2x3_ui()
maintenancetools_ui = main_window.get_maintenancetools_ui()
temperature_ui = main_window.get_temperature_ui()
debuglog_ui = main_window.get_debuglog_window()
state_ui = main_window.get_state_window()


########################################################################################################################
# GUI MANAGERS
########################################################################################################################

# Set up Valve GUI
valve1_gui = ElectrovalveUim(valve1, 1, main_window_ui, electrovalve_ui)
valve2_gui = ElectrovalveUim(valve2, 2, main_window_ui, electrovalve_ui)

# Set up cavity temperature
temperature_gui = TemperatureUim(temperature, main_window_ui, temperature_ui)

# Set up syringe pump GUI
pump_gui = Pump11EliteUim(pump, main_window_ui, pump_ui)

# Set up valve2x3 GUI
valve2x3_gui = ValveMxSeries2Uim(valve2x3, main_window_ui, valve2x3_ui)

# Set up flow controller GUI
flowA_gui = RedFlowMeterUim(flowA, "A", main_window_ui, flow_ui)
flowB_gui = RedFlowMeterUim(flowB, "B", main_window_ui, flow_ui)

# Set up pressure controller GUI
pressure_gui = ElPressUim(pressure, main_window_ui, pressure_ui)

# Set up pressure pump switch GUI
pressure_pump_switch_gui = PressurePumpUim(pressure_pump_switch, main_window_ui)

# Set up picarro code GUI
picarro_code_gui = PicarroCodeUim(picarro_code, main_window_ui)

# Set up state GUI
state_gui = StateUim(state, main_window_ui, state_ui)

# Set up maintenanceTools GUI
maintenancetools_gui = MaintenanceToolsUim(maintenancetools, maintenancetools_ui)

# Set up Debug log GUI
debuglog_gui = DebuglogUim(debug_logger, debuglog_ui, main_window.debuglog_window)


########################################################################################################################
# DATA LOGGER
########################################################################################################################
data_logger = DataLogger("data", humgen)


########################################################################################################################
# LAUNCH APPLICATION
########################################################################################################################

main_window.show()
sys.exit(app.exec_())
