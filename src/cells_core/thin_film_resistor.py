import pya 
import math 

class ThinFilmResistor(pya.PCellDeclarationHelper):
    
    def __init__(self):
        
        super(ThinFilmResistor, self).__init__()
        
        self.tfr1 = pya.LayerInfo(80, 7, "TFR1")
        self.tfr2 = pya.LayerInfo(81, 8, "TFR2")
        self.tfr3 = pya.LayerInfo(82, 9, "TFR3")
        self.met1 = pya.LayerInfo(91, 10, "Met1")
        
        self.param("tfr1", self.TypeLayer, "Layer of TFR1", default=self.tfr1)
        self.param("tfr2", self.TypeLayer, "Layer of TFR2", default=self.tfr2)
        self.param("tfr3", self.TypeLayer, "Layer of TFR3", default=self.tfr3)
        self.param("met1", self.TypeLayer, "Layer of Met1", default=self.met1)
          
        self.param("s", self.TypeShape, "", default=pya.DPoint(0,0))
        self.param("width", self.TypeDouble, "Contact area's width", default=6)
        self.param("length", self.TypeDouble, "Contact area's length", default=8)

    def display_text_impl(self):
        return f"Sibcircuit(Width={self.width}, Length={self.length}"

    def coerce_parameters_impl(self):
        width_handle = None 
        length_handle = None 

        if (self.width < 6  or self.width > 300 ): 
            raise(RuntimeError("Width  must be larger than 6 and less than 300"))
        
        if(self.length < 8 or self.length > 300):
            raise(RuntimeError("Lenght  must be larger than 8 and less than 300"))

        
    def can_create_from_shape_impl(self):
        return self.shape.is_box() or self.shape.is_polygon() or self.shape.is_path()

    def parameters_from_shape_impl(self):
        self.width = self.shape.bbox().width()
        self.length = self.shape.bbox().width()

    def transformation_from_shape_impl(self):
        return pya.Trans(self.shape.bbox().center())

    def produce_impl(self):
        leftCoordX = self.length*150
        leftCoordY = -self.width*18
        rightCoordX = self.length*223.52941176470588
        rightCoordY = self.width*118
        
        leftCoordX2 = -self.length*26.47
        rightCoordX2 = self.length*50

        
        self.cell.shapes(self.tfr1_layer).insert(pya.Box(0, 0, self.length*200, self.width*100))
        self.cell.shapes(self.tfr2_layer).insert(pya.Box(0, 0, self.length*200, self.width*100))
        self.cell.shapes(self.tfr3_layer).insert(pya.Box(0, 0, self.length*200, self.width*100))
        self.cell.shapes(self.met1_layer).insert(pya.Box(leftCoordX, leftCoordY, rightCoordX, rightCoordY))
        self.cell.shapes(self.met1_layer).insert(pya.Box(leftCoordX2, leftCoordY, rightCoordX2, rightCoordY))

class TestLib(pya.Library):

    def __init__(self) -> None:
        self.description = "Test Test Test"
        self.layout().register_pcell("ThinFilmResistor", ThinFilmResistor())
        self.register("TestLib")

TestLib()