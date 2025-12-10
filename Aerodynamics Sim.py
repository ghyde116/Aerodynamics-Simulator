import turtle, time, random

screenWidth, screenHeight = 800, 600 #  screen dimensions
rowCount, columnCount = 100, 100 #  grid dimensions
cellSpacing = 8 #  spacing between cells in the grid

tickSpeed = 0 #  delay between simulation steps (seconds)
viscosity = 3 #  higher values = more viscous fluid
penSize = 4 #  area painted around mouse click

 #  screen setup
screen = turtle.Screen()
screen.colormode(1.0)
screen.screensize(screenWidth, screenHeight)
screen.tracer(0)
screen.listen()

 #  asset stamp turtle
assetStamp = turtle.Turtle()
assetStamp.hideturtle()
assetStamp.speed(0)
assetStamp.penup()

def createGrid(rows, columns, spacing): #  create grid coordinates and index
    gridCoords, gridIndex = [], []
    startX = -(rows * spacing / 2) + spacing / 2 #  calculate starting x and y positions
    startY = -(columns * spacing / 2) + spacing / 2
    indexCounter = 0
    for rowIndex in range(rows):
        for columnIndex in range(columns):
            gridCoords.append([startX + rowIndex * spacing, startY + columnIndex * spacing]) #  calculate cell center coordinates
            gridIndex.append([[rowIndex, columnIndex], indexCounter]) #  store cell indices and corresponding index
            indexCounter += 1
    return gridCoords, gridIndex #  return list of coordinates and corresponding index

def drawGrid(gridCoords): #  draw grid lines
    gridTurtle = turtle.Turtle()
    gridTurtle.hideturtle()
    gridTurtle.speed(0)
    gridTurtle.penup()
    xCoords = sorted({coord[0] for coord in gridCoords}) #  
    yCoords = sorted({coord[1] for coord in gridCoords})
    if len(xCoords) < 2 or len(yCoords) < 2:
        return
    xSpacing = xCoords[1] - xCoords[0]
    ySpacing = yCoords[1] - yCoords[0]
    minX = xCoords[0] - xSpacing / 2
    maxX = xCoords[-1] + xSpacing / 2
    minY = yCoords[0] - ySpacing / 2
    maxY = yCoords[-1] + ySpacing / 2
    for xVal in xCoords:
        gridTurtle.goto(xVal - xSpacing / 2, minY)
        gridTurtle.pendown()
        gridTurtle.goto(xVal - xSpacing / 2, maxY)
        gridTurtle.penup()
    for yVal in yCoords:
        gridTurtle.goto(minX, yVal - ySpacing / 2)
        gridTurtle.pendown()
        gridTurtle.goto(maxX, yVal - ySpacing / 2)
        gridTurtle.penup()
    gridTurtle.goto(maxX, minY)
    gridTurtle.pendown()
    gridTurtle.goto(maxX, maxY)
    gridTurtle.penup()
    gridTurtle.goto(minX, maxY)
    gridTurtle.pendown()
    gridTurtle.goto(maxX, maxY)
    screen.update()

def createCellsDict(indexList): #  create cells dictionary from grid index list
    d = {}

    for item in indexList:
         #  item structure: [[rowIndex, columnIndex], overallIndex]
        d[str(item[1])] = {
            'cellState': 'empty',
            'indexX': item[0][0], 
            'indexY': item[0][1], 
            'color': (1.0, 1.0, 1.0)
            }
    
    return d

def drawGridAssets(): # draw solid and air cells
    global cells, gridCoords, cellSize
    assetStamp.clear()
    for cellKey, cellData in cells.items():
        state = cellData['cellState']
        if state in ('solid', 'air'):
            idx = cellData['indexX'] * columnCount + cellData['indexY']
            if 0 <= idx < len(gridCoords):
                coordX, coordY = gridCoords[idx]
                assetStamp.goto(coordX - cellSize / 2, coordY - cellSize / 2)
                if state == 'solid':
                    assetStamp.color('black') #  solid cells are black
                else:
                    colorTuple = cellData.get('color', (1.0, 1.0, 1.0)) #  default to white
                    if colorTuple[1] == 1:
                        continue
                    else:
                        assetStamp.color(colorTuple)
                assetStamp.begin_fill()
                for _ in range(4): #  draw square cell
                    assetStamp.forward(cellSize)
                    assetStamp.left(90)
                assetStamp.end_fill()
    screen.update() #  call at the end to prevent flickering

def buildPosMap(cellsDict): #  build position map from cells dictionary (optimmization for faster lookup)
    
    d = {}

    for key, cellData in cellsDict.items():
        indexX = cellData['indexX']
        indexY = cellData['indexY']
        d[(indexX, indexY)] = key

    return d

def getKeyAt(ix, iy, posMap): #  get cell key at given indices using position map (optimization for faster lookup)
    return posMap.get((ix, iy))

def paintArea(centerX, centerY, state): #  paint area around given center cell
    positionMap = buildPosMap(cells)
    half = penSize // 2
    for dx in range(-half, -half + penSize):
        for dy in range(-half, -half + penSize):
            key = getKeyAt(centerX + dx, centerY + dy, positionMap)
            if key:
                cells[key]['cellState'] = state
                if state == 'solid':
                    cells[key]['color'] = (0.0, 0.0, 0.0)
                elif state == 'empty':
                    cells[key]['color'] = (1.0, 1.0, 1.0)

def onMouseLeft(clickX, clickY): #  paint solid on left click
    global gridCoords, xSpacing, ySpacing
    for i, (gridX, gridY) in enumerate(gridCoords):
        if -(xSpacing / 2) <= (clickX - gridX) <= (xSpacing / 2) and -(ySpacing / 2) <= (clickY - gridY) <= (ySpacing / 2): #  check if click is within cell bounds
            centerX = cells[str(i)]['indexX']
            centerY = cells[str(i)]['indexY']
            paintArea(centerX, centerY, 'solid')
            drawGridAssets()
            break

def onMouseRight(clickX, clickY): #  paint empty on right click
    global gridCoords, xSpacing, ySpacing
    for i, (gridX, gridY) in enumerate(gridCoords):
        if -(xSpacing / 2) <= (clickX - gridX) <= (xSpacing / 2) and -(ySpacing / 2) <= (clickY - gridY) <= (ySpacing / 2): #  check if click is within cell bounds
            centerX = cells[str(i)]['indexX']
            centerY = cells[str(i)]['indexY']
            paintArea(centerX, centerY, 'empty')
            drawGridAssets()
            break

gridCoords, gridIndex = createGrid(rowCount, columnCount, cellSpacing)
#drawGrid(gridCoords) #  uncomment to draw grid lines
xCoords = sorted({coord[0] for coord in gridCoords})
yCoords = sorted({coord[1] for coord in gridCoords})
xSpacing = xCoords[1] - xCoords[0]
ySpacing = yCoords[1] - yCoords[0]
cellSize = xSpacing
cells = createCellsDict(gridIndex)
 #  global variables created for faster access in functions

def countAirNeighbors(cell, posMap=None): #  count number of air neighbors around a given cell
    if posMap is None:
        posMap = buildPosMap(cells)
    if isinstance(cell, str):
        key = cell
        if key not in cells or cells[key]['cellState'] != 'air':
            return 0
        ix = cells[key]['indexX']; iy = cells[key]['indexY']
    elif isinstance(cell, int):
        key = str(cell)
        if key not in cells or cells[key]['cellState'] != 'air':
            return 0
        ix = cells[key]['indexX']; iy = cells[key]['indexY']
    elif isinstance(cell, (tuple, list)) and len(cell) == 2:
        ix, iy = cell
        key = posMap.get((ix, iy))
        if not key or cells[key]['cellState'] != 'air':
            return 0
    else:
        return 0
    count = 0
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            neighborKey = posMap.get((ix + dx, iy + dy))
            if neighborKey and cells[neighborKey]['cellState'] == 'air':
                count += 1
    return count

def updateCells(viscosityValue): #  update cell states
    global cells, rowCount, columnCount

    posMap = buildPosMap(cells) #  faster lookup

    newPositions = {}
    occupied = set() #  track occupied positions to avoid conflicts

    cellKeys = list(cells.keys())
    random.shuffle(cellKeys) #  randomize processing order to prevent bias

    for key in cellKeys:
        if cells[key]['cellState'] != 'air':
            continue

        ix = cells[key]['indexX']
        iy = cells[key]['indexY']
        oldIndex = int(key)


        if ix == rowCount - 1: #  Last column
            cells[key]['cellState'] = 'empty'
            cells[key]['color'] = (1.0, 1.0, 1.0)
            continue #  Do not move this air cell

        cells[key]['cellState'] = 'empty'
        cells[key]['color'] = (1.0, 1.0, 1.0)

        nx = ix + 1
        ny = iy
        moved = False #  flag to track if cell has moved

        targetIndex = nx * columnCount + ny
        targetKey = str(targetIndex)

        if (targetKey in cells
            and cells[targetKey]['cellState'] == 'empty'
            and targetIndex not in occupied):

            newPositions[key] = targetIndex
            occupied.add(targetIndex)
            moved = True #  mark as moved

        if not moved:
            for d in range(1, viscosityValue + 1):

                candidates = []

                 #  Up scan (higher row index)
                uy = iy + d
                if uy < columnCount:
                    candidates.append((nx, uy))

                 #  Down scan
                dy = iy - d
                if dy >= 0:
                    candidates.append((nx, dy))

                for cx, cy in candidates: #  check candidate positions
                    if cx >= rowCount: #  out of bounds
                        continue

                    candIndex = cx * columnCount + cy #  
                    candKey = str(candIndex)

                    if (candKey in cells
                        and cells[candKey]['cellState'] == 'empty'
                        and candIndex not in occupied): #  move to candidate position

                        newPositions[key] = candIndex
                        occupied.add(candIndex)
                        moved = True #  mark as moved
                        break

                if moved:
                    break


        if not moved: #  stay in place if no movement occurred
            if oldIndex not in occupied:
                newPositions[key] = oldIndex
                occupied.add(oldIndex)


    for oldKey, newIndex in newPositions.items(): #  update cell states based on new positions
        k = str(newIndex)
        cells[k]['cellState'] = 'air'
        cells[k]['color'] = (1.0, 1.0, 1.0)


    posMap = buildPosMap(cells) #  rebuild position map after updates
    for k, data in cells.items():
        if data['cellState'] == 'air':
            cnt = countAirNeighbors(k, posMap)
            pct = cnt / 8.0
            data['color'] = (1.0, 1.0 - pct, 1.0 - pct)

def spawnAir(spawnSpacing): #  spawn air in uniform rows, usually spaced by 1 cell apart
    global cells, columnCount
    spacingValue = spawnSpacing + 1
    for cellIndex in range(columnCount):
        if cellIndex % spacingValue == 0: #  spawn air at intervals defined by spacingValue
            cells[str(cellIndex)]['cellState'] = 'air'
            cells[str(cellIndex)]['color'] = (1.0, 1.0, 1.0)

def run(delay=tickSpeed, spawnDelay=2, spawnSpacing=1): #  main simulation loop (wind tunnel)
    global isRunning, viscosity
    if spawnDelay < 1:
        spawnDelay = 1
    isRunning = True
    iterationCount = 0
    spawnAir(spawnSpacing)
    drawGridAssets()
    fpsAverage = []
    sampleSize = 10
    while isRunning: #  built in fps display to terminal 
        startTime = time.time()
        updateCells(viscosity)
        drawGridAssets()
        iterationCount += 1
        if iterationCount % spawnDelay == 0:
            spawnAir(spawnSpacing)
            drawGridAssets()
        time.sleep(delay)
        endTime = time.time()
        fps = round(1 / (endTime - startTime), 2)
        fpsAverage.append(fps)
        if len(fpsAverage) == sampleSize:
            del fpsAverage[0]
        averageFps = round(sum(fpsAverage) / len(fpsAverage), 2)
        print(f"Step {iterationCount}\nAverage FPS: {averageFps}")

def pauseRun(): #  escape key to pause simulation
    global isRunning
    isRunning = False

 #  key and mouse bindings

screen.onscreenclick(onMouseLeft, 1) #  left click to paint solid
screen.onscreenclick(onMouseRight, 3) #  right click to paint empty
screen.onkey(run, "Return") #  enter key to start simulation
screen.onkey(pauseRun, "Escape") #  escape key to pause simulation
screen.mainloop() #  keep window open
