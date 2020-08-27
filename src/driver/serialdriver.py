import serial
import serial.tools.list_ports

from debuglogger import DebugLogger
from driver.instrumentdriver import InstrumentDriver


class SerialDriver(InstrumentDriver):
    """Abstract class for drivers designed for instruments which can be controlled by a serial connection"""

    def __init__(self, enabled: bool, product: str, baudrate: int, parity: str, stopbits: int, bytesize: int, timeout: float,
                 debug_logger: DebugLogger, object_id: str):
        super(SerialDriver, self).__init__(enabled, debug_logger, object_id)
        if self.get_status_code() == 2:
            self.serial_connection = self.open_connection(product=product,
                                                          baudrate=baudrate,
                                                          parity=parity,
                                                          stopbits=stopbits,
                                                          bytesize=bytesize,
                                                          timeout=timeout)
            if self.serial_connection is not None:
                if self.serial_connection.isOpen():
                    status_code = self.ask_instrument_status()
                    self.set_status_code(status_code)

    def open_connection(self, product: str, baudrate: int, parity: str, stopbits: int, bytesize: int, timeout: float) -> serial:
        """

        :param product: Instrument's "product" name
        :param baudrate:
        :param parity:
        :param stopbits:
        :param bytesize:
        :param timeout:
        :return:
        """
        port = self.get_port(product)
        if port is None:
            print("No port found for ["+product+"]")
            self.set_status_code(2)
            return None

        try:
            serial_connection = serial.Serial(
                port=port,
                baudrate=baudrate,
                parity=parity,
                stopbits=stopbits,
                bytesize=bytesize,
                timeout=timeout
            )
        except OSError as e:
            print(str(e))
            self.set_status_code(2)
            return None

        # Open connection if not already open
        if not serial_connection.isOpen():
            serial_connection.open()

        self.set_status_code(5)

        return serial_connection

    @staticmethod
    def get_port(product: str) -> str:
        """
        Get the port ("/dev/ttyXXXX") where the instrument identified by "product" is connected.

        :param product: Instrument's product name
        :return: Instrument port.
        """
        instrument_list = list(serial.tools.list_ports.comports())
        for instrument in instrument_list:
            if product == instrument.product:
                return instrument.device

        return None


