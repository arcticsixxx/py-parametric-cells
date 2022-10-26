import pya 
import math 

class Subcircuit(pya.PCellDeclarationHelper):
    
    def __init__(self):
        
        super(Subcircuit, self).__init__()

        self.param("l", self.TypeLayer, "Layer", default=pya.LayerInfo(1, 0))
        self.param("s", self.TypeShape, "", default=pya.DPoint(0,0))
        self.param("width", self.TypeDouble, "Contact area's width", default=100)
        self.param("length", self.TypeDouble, "Contact area's length", default=100)

        self.param("width_mem", self.TypeDouble, "Width_mem", default=0.0, hidden=True)
        self.param("length_mem", self.TypeDouble, "Length_mem", default=0.0, hidden=True)

    def display_text_impl(self):
        return f"Sibcircuit(L={self.layer}, Width={self.width}, Length={self.length}"

    def coerce_parameters_impl(self):
        width_handle = None 
        length_handle = None 

        if (self.width < 75 and self.length < 75 or self.width > 250 and self.length > 250): 
            raise(RuntimeError("Width and length must be larger than 75 and less than 250"))

        if isinstance(self.width, pya.DPoint):
            width_handle = self.width.distance(pya.DPoint(0, 0))

        if isinstance(self.length, pya.DPoint):
            length_handle = self.length.distance(pya.DPoint(0, 0))

        if abs(self.width - self.width_mem) < 1e-6 and abs(self.width - self.width_mem):
            self.width_mem = width_handle
            self.width = width_handle
            self.length = length_handle
            self.length_mem = length_handle
        else:
            self.width_mem = self.width
            self.width_handle = pya.DPoint(-self.width, 0)
            self.length_mem = self.length
            self.length_handle = pya.DPoint(-self.length, 0)

        
    def can_create_from_shape_impl(self):
        return self.shape.is_box() or self.shape.is_polygon() or self.shape.is_path()

    def parameters_from_shape_impl(self):
        self.width = self.shape.bbox().width()
        self.length = self.shape.bbox().width()
        self.layer = self.layout.get_info(self.layer)

    def transformation_from_shape_impl(self):
        return pya.Trans(self.shape.bbox().center())

    def produce_impl(self):
        width_dbu = self.width / self.layout.dbu
        length_dbu = self.length / self.layout.dbu

        self.cell.shapes(self.l_layer).insert(pya.Box(0, 0, length_dbu, width_dbu))

class TestLib(pya.Library):

    def __init__(self) -> None:
        self.description = "Test Test Test"
        self.layout().register_pcell("Subcircuit", Subcircuit())
        self.register("TestLib")

TestLib()