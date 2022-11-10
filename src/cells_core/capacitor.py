import pya

class Capacitor(pya.PCellDeclarationHelper):

  def __init__(self):

    super(Capacitor, self).__init__()
    
    self.met1 = pya.LayerInfo(91, 10, "Met1")
    self.met2 = pya.LayerInfo(92, 13, "Met2")
    self.via1 = pya.LayerInfo(71, 11, "Via1")
    self.mesa = pya.LayerInfo(40, 2, "Mesa")
    
    self.param("met1", self.TypeLayer, "Layer of met1", default=self.met1, hidden=True)
    self.param("met2", self.TypeLayer, "Layer of met1", default=self.met2, hidden=True)
    self.param("via1", self.TypeLayer, "Layer of via1", default=self.via1, hidden=True)
    self.param("mesa", self.TypeLayer, "Layer of mesa", default=self.mesa, hidden=True)
    
    self.param("width_cap", self.TypeInt, "Capacitor width", default=30)
    self.param("lenght_cap", self.TypeInt, "Capacitor lenght", default=30)
    
  def insertPolygons(self, pts_layer, layer):
    for pts in pts_layer[0:]:
      polygon = pya.SimplePolygon(pts)
      self.cell.shapes(layer).insert(polygon)
      
  def display_text_impl(self):
  
    return f"Capacitor(W={self.width_cap}, L={self.lenght_cap})"
    
  def coerce_parameters_impl(self):
    
    if (self.width_cap < 20 or self.width_cap > 450 or self.lenght_cap < 20 or self.lenght_cap > 450):
      raise(RuntimeError("Параметры не могут быть меньше 20 мкм, а также превышить 450 мкм"))
      
    if (self.width_cap / self.lenght_cap > 20 or self.lenght_cap / self.width_cap > 20):
      raise(RuntimeError("Соотношение параметров W/L (L/W) не может превышать 20"))
  
  def produce_impl(self):
    
    pts_mesa = [[pya.Point(-6000,self.lenght_cap * 500 + 20000), pya.Point(6000,self.lenght_cap * 500 + 20000), pya.Point(6000,self.lenght_cap * 500 + 10000), pya.Point(-6000,self.lenght_cap * 500 + 10000)],
               [pya.Point(-self.width_cap * 500, -self.lenght_cap * 500), pya.Point(self.width_cap * 500,-self.lenght_cap * 500), pya.Point(self.width_cap * 500,self.lenght_cap * 500),pya.Point(-self.width_cap * 500,self.lenght_cap * 500)],
               [pya.Point(-6000,-self.lenght_cap * 500 - 20000), pya.Point(6000,-self.lenght_cap * 500 - 20000), pya.Point(6000,-self.lenght_cap * 500 - 10000), pya.Point(-6000,-self.lenght_cap * 500 - 10000)]]
               
    pts_met2 = [[pya.Point(-5500, self.lenght_cap * 500 + 19500), pya.Point(5500, self.lenght_cap * 500 + 19500), pya.Point(5500, self.lenght_cap * 500 + 4500), pya.Point(self.width_cap * 500 + 4500, self.lenght_cap * 500 + 4500),
               pya.Point(self.width_cap * 500 + 4500, -self.lenght_cap * 500 - 4500), pya.Point(-self.width_cap * 500 - 4500, -self.lenght_cap * 500 - 4500), pya.Point(-self.width_cap * 500 - 4500, self.lenght_cap * 500 + 4500), pya.Point(-5500, self.lenght_cap * 500 + 4500)],
               [pya.Point(-5500, -self.lenght_cap * 500 - 10500), pya.Point(5500, -self.lenght_cap * 500 - 10500), pya.Point(5500, -self.lenght_cap * 500 - 19500), pya.Point(-5500,-self.lenght_cap * 500 - 19500)]]
    
    pts_met1 = [[pya.Point(-4000, self.lenght_cap * 500 + 18000), pya.Point(4000, self.lenght_cap * 500 + 18000), pya.Point(4000, self.lenght_cap * 500 + 12000), pya.Point(-4000, self.lenght_cap * 500 + 12000)],
               [pya.Point(-self.width_cap * 500 - 3000, self.lenght_cap * 500 + 3000), pya.Point(self.width_cap * 500 + 3000, self.lenght_cap * 500 + 3000), pya.Point(self.width_cap * 500 + 3000, -self.lenght_cap * 500 - 3000), pya.Point(4000, -self.lenght_cap * 500 - 3000),
               pya.Point(4000, -self.lenght_cap * 500 - 18000), pya.Point(-4000, -self.lenght_cap * 500 - 18000), pya.Point(-4000, -self.lenght_cap * 500 - 3000), pya.Point(-self.width_cap * 500 - 3000, -self.lenght_cap * 500 - 3000)]]
                
    pts_via1 = [[pya.Point(-3000, self.lenght_cap * 500 + 17000), pya.Point(3000, self.lenght_cap * 500 + 17000), pya.Point(3000, self.lenght_cap * 500 + 13000), pya.Point(-3000, self.lenght_cap * 500 + 13000)],
               [pya.Point(-3000, -self.lenght_cap * 500 - 17000), pya.Point(3000, -self.lenght_cap * 500 - 17000), pya.Point(3000, -self.lenght_cap * 500 - 13000), pya.Point(-3000, -self.lenght_cap * 500 - 13000)]]
    
    self.insertPolygons(pts_mesa, self.mesa_layer)
    self.insertPolygons(pts_met2, self.met2_layer)
    self.insertPolygons(pts_met1, self.met1_layer)
    self.insertPolygons(pts_via1, self.via1_layer)
    
class PCellLib(pya.Library):

  def __init__(self):
  
    self.description = "My PCell library"
    self.layout().register_pcell("Capacitor", Capacitor())
    self.register("PCellLib")

PCellLib()

