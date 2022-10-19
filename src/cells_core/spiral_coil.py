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
    self.param("innHandle", self.TypeShape, "", default = pya.DPoint(0, 0))
    self.param("outHandle", self.TypeShape, "", default = pya.DPoint(0, 0))
     
    # Скрытые PCell параметры
    self.param("innMem", self.TypeDouble, "Inner memory", default = 0.0, hidden = True)
    self.param("outMem", self.TypeDouble, "Out memory", default = 0.0, hidden = True)

  def display_text_impl(self):
    # Текст описания ячейки
    return "Spiral(L=" + str(self.layer) + ",Outer radius=" + ('%.3f' % self.outRadius) + ")"
  
  def coerce_parameters_impl(self):
    
    innHandleRadius = None
    outHandleRadius = None

    if isinstance(self.innHandle, pya.DPoint): 
      #Расчет дистанции от внутренней управляемой точки до центра
      innHandleRadius = self.innHandle.distance(pya.DPoint(0, 0))

    if isinstance(self.outHandle, pya.DPoint): 
      #Расчет дистанции от внешней управляемой точки до центра
      outHandleRadius = self.outHandle.distance(pya.DPoint(0, 0))

    if abs(self.innRadius-self.innMem) < 1e-6 and abs(self.outRadius-self.outMem) < 1e-6:
      self.innMem = innHandleRadius
      self.innRadius = innHandleRadius
      self.outMem = outHandleRadius
      self.outRadius = outHandleRadius
    else:
      self.innMem = self.innRadius
      self.innHandle = pya.DPoint(-self.innRadius, 0)
      self.outMem = self.outRadius
      self.outHandle = pya.DPoint(-self.outRadius, 0)
    
    if self.numPoints <= 4:
      self.numPoints = 4
  
  def can_create_from_shape_impl(self):
    return self.shape.is_box() or self.shape.is_polygon() or self.shape.is_path()
  
  def parameters_from_shape_impl(self):
    self.innRadius = self.shape.bbox().width() * self.layout.dbu / 4
    self.outRadius = self.shape.bbox().width() * self.layout.dbu / 2
    self.layer = self.layout.get_info(self.layer)
  
  def transformation_from_shape_impl(self):
    return pya.Trans(self.shape.bbox().center())
  
  def produce_impl(self):
    innRadiusDbu = self.innRadius / self.layout.dbu
    outRadiusDbu = self.outRadius / self.layout.dbu
    
    pts = []
    da = math.pi * 2 / self.numPoints
    dr = (self.width+self.spacing)/self.numPoints/self.layout.dbu
    currRadius = innRadiusDbu
    currAngle = 0

    while currRadius < outRadiusDbu:

      pts.append(pya.Point.from_dpoint(pya.DPoint(currRadius * math.cos(currAngle), currRadius * math.sin(currAngle))))
      currRadius += dr
      currAngle = (currAngle+da)%(math.pi*2)
    
    self.cell.shapes(self.l_layer).insert(pya.Path(pts,self.width/self.layout.dbu))


class MyLib(pya.Library):

  def __init__(self):
    self.description = "My First Library"
    self.layout().register_pcell("Spiral", Spiral())
    self.register("MyLib")

MyLib()