import pya 
import math 

class Subcircuit(pya.PCellDeclarationHelper):
    
    def __init__(self):
        
        super(Subcircuit, self).__init__()

        #self.SECOND_LAYER_MULTIPLIER = 1.25

        self.met1 = pya.LayerInfo(91, 10, "Met1")
        self.via1 = pya.LayerInfo(71, 11, "Via1")
        self.met1_2 = pya.LayerInfo(91, 10, "Met1")
        #self.met2 = pya.LayerInfo(92, 13, "Met2")
        #self.back = pya.LayerInfo(130, 16, "Back")

        self.param("met1", self.TypeLayer, "Layer of met1", default=self.met1, hidden=True)
        self.param("via1", self.TypeLayer, "Layer of via1", default=self.via1, hidden=True)
        self.param("met1_2", self.TypeLayer, "Layer of met1", default=self.met1_2)
        #self.param("met2", self.TypeLayer, "Layer of met2", default=self.met2)
        #self.param("back", self.TypeLayer, "Layer of back", default=self.back)
        
        self.param("width", self.TypeDouble, "Contact area's width", default=100)
        self.param("length", self.TypeDouble, "Contact area's length", default=100)
        self.param("scale_factor", self.TypeDouble, "The scaling factor for the second layer", default=1.25) 

        self.param("via1_width", self.TypeDouble, "Via1 Width", default=125, hidden=True)
        self.param("via1_length", self.TypeDouble, "Via1 length", default=125, hidden=True)
        

    def display_text_impl(self):
        return f"Sibcircuit(L={self.layer}, Width={self.width}, Length={self.length}, Scaling factor={self.scale_factor})"

    def coerce_parameters_impl(self):
        
        if (self.width < 75 or self.length < 75 or self.width > 250 or self.length > 250): 
            raise(RuntimeError("Width and length must be larger than 75 and less than 250"))

        if (self.scale_factor > 1.0 and self.scale_factor <= 2.0):
            self.via1_length = self.length * self.scale_factor
            self.via1_width = self.width * self.scale_factor
        
    def can_create_from_shape_impl(self):
        return self.shape.is_box() or self.shape.is_polygon() or self.shape.is_path()

    def parameters_from_shape_impl(self):
        self.width = self.shape.bbox().width()
        self.length = self.shape.bbox().width()
        self.layer = self.layout.get_info(self.layer)

    def transformation_from_shape_impl(self):
        return pya.Trans(self.shape.bbox().center())

    def produce_impl(self):
        inner_layer = pya.Box(0, 0, self.length, self.width)
        self.cell.shapes(self.met1_layer).insert(inner_layer)
        
        """ 
        Для того чтобы инстанцировать экземпляр класса Box, мы можем воспользоваться конструктором создания
        Box'а по двум точкам (левая нижняя/правая верхняя). Для получения левой нижней точки мы вызываем метод center()
        для первого слоя(первого Box'а) и образщаемся к атриббуту x, для получения значенияя x на координатной прямой,
        находящегося слева, мы отнимаем половину ширины Box'а(аттрибут length) и умножаем его на scale factor. Аналогично и
        для других точек. В результате мы получим новый слой, где бох будет в scaling factor раз больше Box'a на первом слое 
        """
        lft = inner_layer.center().x - (self.length / 2 * self.scale_factor)
        bot = inner_layer.center().y - (self.width / 2 * self.scale_factor)
        rgt = inner_layer.center().x + (self.length / 2 * self.scale_factor)
        top = inner_layer.center().y + (self.width / 2 * self.scale_factor)
        
        self.cell.shapes(self.via1_layer).insert(pya.Box(lft, bot, rgt, top))
        
        lft_th = inner_layer.center().x - (self.length / 2 * 1.35)
        bot_th = inner_layer.center().y - (self.width / 2 * 1.35)
        rgt_th = inner_layer.center().x + (self.length / 2 * 1.35)
        top_th = inner_layer.center().y + (self.width / 2 * 1.35)
        
        self.cell.shapes(self.met1_2_layer).insert(pya.Box(lft_th, bot_th, rgt_th, top_th))

class TestLib(pya.Library):

    def __init__(self) -> None:
        self.description = "Test Test Test"
        self.layout().register_pcell("Subcircuit", Subcircuit())
        self.register("TestLib")

TestLib()