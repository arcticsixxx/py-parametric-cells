import pya 

class SquareCoil(pya.PCellDeclarationHelper):

    def __init__(self) -> None:
        super(SquareCoil, self).__init__()

        self.param("layer", self.TypeLayer, "Layer", default = pya.LayerInfo(1, 0))
        self.param("width", self.TypeDouble, "Width", default = 1)
        self.param("spacing", self.TypeDouble, "Spacing", default = 1)


