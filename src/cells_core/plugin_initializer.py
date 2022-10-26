import pya 

from src.cells_core.sqare_coil import SquareCoil

class CoilsLibrary(pya.Library):
    def __init__(self) -> None:
        self.description = "Plugin implements several types of coils."
        self.layout().register_pcell("Square Coil", SquareCoil())
        self.register("CoilsLibrary")
