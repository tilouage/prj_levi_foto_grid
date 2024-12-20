import itertools
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as pltcolors
from matplotlib.widgets import Button
from PIL import Image

# console input
img_path = input('Filepath naar de gewenste foto: ')

dpi = 100
# text scaled te hoog als dpi verhoogd wordt, kun je zelf nog aanpassen als je wilt
# dpi_text = input('Gewenste dpi (dots per inch), default = 100: ')
# if dpi_text.isnumeric():
#     dpi = int(dpi_text)

# load image
image = Image.open(img_path)
imgWidth, imgHeight = image.size

# init figure
fig = plt.figure(figsize=(float(image.size[0] / dpi), image.size[1] / dpi), dpi=dpi)

# add image subplot
imAx = fig.add_subplot(1, 1, 1)
imAx.imshow(image)

# grid functions
def updateFigure():
    fig.canvas.draw()
    # fig.canvas.flush_events()

def updateGrid():
    global showGrid
    global currentRasterColor
    global linewidth

    if showGrid:
        imAx.grid(color=currentRasterColor, linewidth=linewidth)
    else:
        imAx.grid(False)
    updateFigure()

def toggleRaster(clickEvent):
    global showGrid
    global bToggleRaster

    showGrid = not showGrid
    labelText = 'AAN' if not showGrid else 'UIT'
    bToggleRaster.label.set_text(labelText)
    updateGrid()

def switchRasterColor(clickEvent):
    global colors
    global currentRasterColor
    global bColor

    currentRasterColor = next(colors)
    bColor.color = currentRasterColor
    updateGrid()

def increaseLineWidth(clickEvent):
    global linewidth

    linewidth += 1
    updateGrid()

def decreaseLineWidth(clickEvent):
    global linewidth

    linewidth = 1 if linewidth == 1 else linewidth - 1
    updateGrid()

def setRasterSize(tickInterval):
    global imgWidth

    xticks = np.arange(0, imgWidth, tickInterval)
    yticks = np.arange(0, imgHeight, tickInterval)
    imAx.set_xticks(xticks, None)
    imAx.set_yticks(yticks)
    updateFigure()

def enlargeRaster(clickEvent):
    global tickInterval

    tickInterval += 5
    setRasterSize(tickInterval)

def reduceRaster(clickEvent):
    global tickInterval

    tickInterval = 5 if tickInterval == 5 else tickInterval - 5
    setRasterSize(tickInterval)

# show grid
showGrid = False

# raster linewidth
linewidth = 1

# ticks (streep op x en y as)
tickInterval = 20
setRasterSize(tickInterval)

# raster color
colors = itertools.cycle(list(pltcolors.BASE_COLORS.keys()) + list(pltcolors.TABLEAU_COLORS.keys()))
currentRasterColor = next(colors)

# add button actions
bColor = Button(plt.axes([0.95, 0.95, 0.025, 0.05]), '', color=currentRasterColor)
bColor.on_clicked(switchRasterColor)
bToggleRaster = Button(plt.axes([0.975, 0.95, 0.025, 0.05]), 'AAN')
bToggleRaster.on_clicked(toggleRaster)
bLargerRaster = Button(plt.axes([0.95, 0.89, 0.05, 0.05]), 'Raster +')
bLargerRaster.on_clicked(enlargeRaster)
bSmallerRaster = Button(plt.axes([0.95, 0.83, 0.05, 0.05]), 'Raster -')
bSmallerRaster.on_clicked(reduceRaster)
bLargerLines = Button(plt.axes([0.95, 0.77, 0.05, 0.05]), 'Lijn +')
bLargerLines.on_clicked(increaseLineWidth)
bSmallerLines = Button(plt.axes([0.95, 0.71, 0.05, 0.05]), 'Lijn -')
bSmallerLines.on_clicked(decreaseLineWidth)

# fullscreen
plt.tight_layout()
plt.get_current_fig_manager().window.showMaximized()

# show plot
plt.show()

# save subplot
out_path = input('Afbeelding opslaan op filepath (leeg=verwerpen): ')

if out_path is not None and out_path != '':
    subplotExtent = imAx.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    fig.savefig(out_path, bbox_inches=subplotExtent)
