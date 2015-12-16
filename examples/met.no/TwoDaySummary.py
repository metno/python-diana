# Created from FourDaySummary.ipynb
from metno import bdiana, plotcommands
import pyproj
from PyQt4.QtCore import QRect, Qt
from PyQt4.QtGui import QColor, QFont, QImage, QPainter

b = bdiana.BDiana()

b.setup("/etc/diana/setup/diana.setup-COMMON")
b.addModel("AROME", "http://thredds.met.no/thredds/dodsC/arome25/arome_metcoop_default2_5km_latest.nc", clear = True)

model = "AROME"
field = "accumprecip.24h"
times = b.getFieldTimes(model, field)

plot_times = []
for t in times:
    if t.hour == 6:
        plot_times.append(t)
        if len(plot_times) == 4:
            break

p = pyproj.Proj(proj="stere", datum="WGS84")
x1, y1 = p(4, 58)
x2, y2 = p(15, 65)

a = plotcommands.Area(proj4string = p.srs, rectangle = (x1, x2, y1, y2))
m = plotcommands.Map()
m.setOption("map", "Gshhs-Auto")
m.setOption("backcolour", "white")
m.setOption("land", "on")
m.setOption("land.colour", "0:64:0")

f = plotcommands.Field(model = model, plot = field, plottype = "contour")
f.setOption("palettecolours", "wms.precip1h.palett")
f.setOption("line.values", [0.5,1,2,4,6,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,105,110,115,120,125,130,135,140,145,150,155,160,165,170,175,180,185,190,195,200,205,210,215,220,225,230,235,240,245,250,255,260,265,270,275,280,285,290,295,300])
f.setOption("colour", "off")
f.setOption("table", 1)
f.setOption("extreme.type", "Value")

b.setPlotCommands([a, m, f])

images = []
for t in plot_times:
  b.setPlotTime(t)
  images.append((t, b.plotImage(150, 300)))
  

l = plotcommands.Label()
l.setOption("anno", "<table,fcolour=white>")
l.setOption("fontsize", 12)
l.setOption("polystyle", "none")
l.setOption("halign", "right")
l.setOption("valign", "top")

b.setPlotCommands([f, l])
b.setPlotTime(t)

anno = QImage(150, 300, QImage.Format_RGB16)
anno.fill(QColor(Qt.white))
b._plot(150, 300, anno, plot_method = b.controller.plotAnnotations)

image = QImage((len(plot_times) * (150 + 25)) + 150, 330, QImage.Format_RGB16)
image.fill(QColor(Qt.white))
font = QFont()
font.setPixelSize(20)
painter = QPainter()
painter.begin(image)
painter.setFont(font)
x = 0
for t, im in images:
    painter.drawImage(x, 0, im)
    painter.drawText(QRect(x, 305, 150, 25), Qt.AlignCenter, t.strftime("%A"))
    x += 150 + 25
painter.drawImage(x, 0, anno)
painter.end()

image.save("2-day-summary.png")


