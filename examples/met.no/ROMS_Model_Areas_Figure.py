#!/usr/bin/env python

# Created from ROMS Model Areas Figure.ipynb
# Aims to reproduces the figure at https://dokit.met.no/fou/hi/roms_model_group/start.

import datetime

from metno import bdiana, plotcommands
from metno.ipython_extensions import embed

if __name__ == "__main__":

    b = bdiana.BDiana(log_level = 5)
    b.setup()
    b.addModel("Arctic-20km.24h_avg", "http://thredds.met.no/thredds/dodsC/sea/arctic20km/24h/aggregate_be", clear = True)
    b.addModel("Nordic-4km.24h_avg", "http://thredds.met.no/thredds/dodsC/sea/nordic4km/24h/aggregate_be")
    b.addModel("NorKyst-800m.24h_avg", "http://thredds.met.no/thredds/dodsC/sea/norkyst800m/24h/aggregate_be")
    
    m = plotcommands.Map(map = "Gshhs-Auto", backcolour = "white", land = "on")
    m.setOption("land.colour", "gray")
    
    f1 = plotcommands.Field(model = "Arctic-20km.24h_avg",
                            plot = "BOTTOM_DEPTH",
                            colour = "orange",
                            plottype = "contour",
                            linetype = "solid",
                            linewidth = 1,
                            antialiasing = True)
    f1.setOption("line.interval", 500)
    
    f2 = plotcommands.Field(model = "Nordic-4km.24h_avg",
                            plot = "BOTTOM_DEPTH",
                            colour = "darkcyan",
                            plottype = "contour",
                            linetype = "solid",
                            linewidth = 1,
                            antialiasing = True)
    f2.setOption("line.interval", 500)
    
    f3 = plotcommands.Field(model = "NorKyst-800m.24h_avg",
                            plot = "BOTTOM_DEPTH",
                            colour = "darkblue",
                            plottype = "contour",
                            linetype = "solid",
                            linewidth = 1,
                            antialiasing = True)
    f3.setOption("line.interval", 500)
    
    l1 = plotcommands.Label(data = "", fontsize = 8)
    
    b.setPlotCommands([m, f1, f2, f3, l1])
    b.setPlotTime(datetime.datetime.now())
    
    b.plotImage(210 * 2, 210 * 2).save("ROMS-model-areas.png")
    b.plotPDF(210, 210, "ROMS-model-areas.pdf", units = "mm")
