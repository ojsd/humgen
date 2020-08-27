import threading
from time import sleep
from abc import ABC, abstractmethod
from driver.instrumentdriver import InstrumentDriver


class AbstractUim(ABC):

    def initialize_display(self, instrument: InstrumentDriver):
        """
        If the underlying instrument is properly working, initialize widgets according to instrument's initial
        status and launch the thread which periodically updates all the widgets.
        Otherwise, disable all widgets related to the instrument.
        This function is meant to be used at the end of the __init__ function of the children classes.
        """
        if instrument.get_status_code() < 5:
            self.toggle_all_widgets(False)
        else:
            self.update_all_displays()
            self.launch_thread_for_update_display()

    def launch_thread_for_update_display(self):
        a = threading.Thread(None, self.__display_thread__)
        a.daemon = True
        a.start()

    def __display_thread__(self):
        while True:
            self.update_all_displays()
            sleep(1)

    @abstractmethod
    def update_all_displays(self):
        pass

    @abstractmethod
    def toggle_all_widgets(self, enabled: bool):
        """If enabled is false, all the widgets will be "greyed" and thus will not be editable."""
        pass
