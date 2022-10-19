import pya
import math

class Spiral(pya.PCellDeclarationHelper):
  """
  Объявление PCell для спирали
  """

  def __init__(self):

    super(Spiral, self).__init__()

    # Pcell параметры
    self.param("layer", self.TypeLayer, "Layer", default = pya.LayerInfo(1, 0))
    self.param("numPoints", self.TypeInt, "Number of points", default = 64) 
    self.param("innRadius", self.TypeDouble, "Inner Radius", default = 1)
    self.param("outRadius", self.TypeDouble, "Outer Radius", default = 10)
    self.param("width", self.TypeDouble, "Width", default = 1)
    self.param("spacing", self.TypeDouble, "Spacing", default = 1)
    self.param("innHandle", self.TypeDouble, "", default = pya.DPoint(0, 0))
    self.param("outHandle", self.TypeDouble, "", default = pya.Dpoint(0, 0))
        
    # Скрытые PCell параметры
    self.param("innerMem", self.TypeDouble, default = 0.0, hidden = True)
    self.param("outerMem", self.TypeDouble, default = 0.0, hidden = True)

  def display_text_impl(self):
    # Текст описания ячейки
    return "Spiral(L=" + str(self.layer) + ",Outer radius=" + ('%.3f' % self.outRadius) + ")"
  
  def coerce_parameters_impl(self):

    innderHandleRadius = None
    outerHandleRadius = None

    if isinstance(self.innHandle, pya.DPoint):
      #Расчет дистанции от внутренней управляемой точки до центра
      innderHandleRadius = self.innHandle.distance(pya.DPoint(0,0))

    if isinstance(self.outHandle, pya.DPoint):
      #Расчет дистанции от внешней управляемой точки до центра
      outerHandleRadius = self.outHandle.distance(pya.DPoint(0,0))

    # Проверка что была изменена именно точка, а не параметр
    if abs(self.innRadius - self.innMem) < 1e-6:
      self.innMem = self.innerHandleRadius
      self.outMem = self.outerHandleRadius

  
  def can_create_from_shape_impl(self):
    # Implement the "Create PCell from shape" protocol: we can use any shape which 
    # has a finite bounding box
    return self.shape.is_box() or self.shape.is_polygon() or self.shape.is_path()
  
  def parameters_from_shape_impl(self):
    # Implement the "Create PCell from shape" protocol: we set r and l from the shape's 
    # bounding box width and layer
    self.r = self.shape.bbox().width() * self.layout.dbu / 2
    self.l = self.layout.get_info(self.layer)
  
  def transformation_from_shape_impl(self):
    # Implement the "Create PCell from shape" protocol: we use the center of the shape's
    # bounding box to determine the transformation
    return pya.Trans(self.shape.bbox().center())
  
  def produce_impl(self):
  
    # This is the main part of the implementation: create the layout

    # fetch the parameters
    ru_dbu = self.ru / self.layout.dbu
    
    # compute the circle
    pts = []
    da = math.pi * 2 / self.n
    for i in range(0, self.n):
      pts.append(pya.Point.from_dpoint(pya.DPoint(ru_dbu * math.cos(i * da), ru_dbu * math.sin(i * da))))
    
    # create the shape
    self.cell.shapes(self.l_layer).insert(pya.Polygon(pts))


class MyLib(pya.Library):
  """
  The library where we will put the PCell into 
  """

  def __init__(self):
  
    # Set the description
    self.description = "My First Library"
    
    # Create the PCell declarations
    self.layout().register_pcell("Circle", Circle())
    # That would be the place to put in more PCells ...
    
    # Register us with the name "MyLib".
    # If a library with that name already existed, it will be replaced then.
    self.register("MyLib")


# Instantiate and register the library
MyLib()
