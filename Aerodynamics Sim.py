import turtle, time, random

screenWidth, screenHeight = 800, 600
rowCount, columnCount = 400, 400
cellSpacing = 2

tickSpeed = 0
viscosity = 3
penSize = 8

screen = turtle.Screen()
screen.colormode(1.0)
screen.screensize(screenWidth, screenHeight)
screen.tracer(0)
screen.listen()

assetStamp = turtle.Turtle()
assetStamp.hideturtle()
assetStamp.speed(0)
assetStamp.penup()

def createGrid(rows, columns, spacing):
    gridCoords, gridIndex = [], []
    startX = -(rows * spacing / 2) + spacing / 2
    startY = -(columns * spacing / 2) + spacing / 2
    indexCounter = 0
    for rowIndex in range(rows):
        for columnIndex in range(columns):
            gridCoords.append([startX + rowIndex * spacing, startY + columnIndex * spacing])
            gridIndex.append([[rowIndex, columnIndex], indexCounter])
            indexCounter += 1
    return gridCoords, gridIndex

def drawGrid(gridCoords):
    gridTurtle = turtle.Turtle()
    gridTurtle.hideturtle()
    gridTurtle.speed(0)
    gridTurtle.penup()
    xCoords = sorted({coord[0] for coord in gridCoords})
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

def createCellsDict(indexList):
    d = {}
    
    for item in indexList:
        d[str(item[1])] = {'cellState': 'empty', 'indexX': item[0][0], 'indexY': item[0][1], 'color': (1.0, 1.0, 1.0)}
    
    return d

def drawGridAssets():
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
                    assetStamp.color('black')
                else:
                    colorTuple = cellData.get('color', (1.0, 1.0, 1.0))
                    if colorTuple[1] == 1:
                        continue
                    else:
                        assetStamp.color(colorTuple)
                assetStamp.begin_fill()
                for _ in range(4):
                    assetStamp.forward(cellSize)
                    assetStamp.left(90)
                assetStamp.end_fill()
    screen.update()

def buildPosMap(cellsDict):
    
    d = {}

    for key, cellData in cellsDict.items():
        indexX = cellData['indexX']
        indexY = cellData['indexY']
        d[(indexX, indexY)] = key

    return d

def getKeyAt(ix, iy, posMap):
    return posMap.get((ix, iy))

def paintArea(centerX, centerY, state):
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

def onMouseLeft(clickX, clickY):
    global gridCoords, xSpacing, ySpacing
    for i, (gridX, gridY) in enumerate(gridCoords):
        if -(xSpacing / 2) <= (clickX - gridX) <= (xSpacing / 2) and -(ySpacing / 2) <= (clickY - gridY) <= (ySpacing / 2):
            centerX = cells[str(i)]['indexX']
            centerY = cells[str(i)]['indexY']
            paintArea(centerX, centerY, 'solid')
            drawGridAssets()
            break

def onMouseRight(clickX, clickY):
    global gridCoords, xSpacing, ySpacing
    for i, (gridX, gridY) in enumerate(gridCoords):
        if -(xSpacing / 2) <= (clickX - gridX) <= (xSpacing / 2) and -(ySpacing / 2) <= (clickY - gridY) <= (ySpacing / 2):
            centerX = cells[str(i)]['indexX']
            centerY = cells[str(i)]['indexY']
            paintArea(centerX, centerY, 'empty')
            drawGridAssets()
            break

gridCoords, gridIndex = createGrid(rowCount, columnCount, cellSpacing)
#drawGrid(gridCoords)
xCoords = sorted({coord[0] for coord in gridCoords})
yCoords = sorted({coord[1] for coord in gridCoords})
xSpacing = xCoords[1] - xCoords[0]
ySpacing = yCoords[1] - yCoords[0]
cellSize = xSpacing
cells = createCellsDict(gridIndex)

def countAirNeighbors(cell, posMap=None):
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

def updateCells(viscosityValue):
    global cells, rowCount, columnCount
    newAirPositions = []
    columnsMap = {}
    for cellKey, cellData in cells.items():
        colIndex = cellData['indexX']
        columnsMap.setdefault(colIndex, []).append(cellKey)
    columnOrder = list(columnsMap.keys())
    random.shuffle(columnOrder)
    for colIndex in columnOrder:
        columnKeys = list(columnsMap[colIndex])
        for cellKey in columnKeys:
            if cells[cellKey]['cellState'] != 'air':
                continue
            if colIndex >= rowCount - 1:
                cells[cellKey]['cellState'] = 'empty'
                cells[cellKey]['color'] = (1.0, 1.0, 1.0)
                continue
            cells[cellKey]['cellState'] = 'empty'
            cells[cellKey]['color'] = (1.0, 1.0, 1.0)
            nextPosKey = str(int(cellKey) + columnCount)
            newPos = int(cellKey)
            if nextPosKey in cells and cells[nextPosKey]['cellState'] in ('solid', 'air'):
                origX = cells[cellKey]['indexX']
                origY = cells[cellKey]['indexY']
                foundEmpty = False
                for drift in range(0, viscosityValue + 1):
                    candidates = []
                    if drift == 0:
                        candidates.append(origY)
                    else:
                        candidates.extend([origY + drift, origY - drift])
                        random.shuffle(candidates)
                    for candidateY in candidates:
                        candidateX = origX + 1
                        if candidateX >= rowCount or candidateY < 0 or candidateY >= columnCount:
                            continue
                        candidateIndex = candidateX * columnCount + candidateY
                        candidateKey = str(candidateIndex)
                        if candidateKey in cells and cells[candidateKey]['cellState'] == 'empty':
                            newPos = candidateIndex
                            foundEmpty = True
                            break
                    if foundEmpty:
                        break
            else:
                newPos = int(cellKey) + columnCount
            if newPos not in newAirPositions:
                newAirPositions.append(newPos)
            else:
                newAirPositions.append(int(cellKey))
    for pos in newAirPositions:
        stringPos = str(pos)
        if stringPos in cells:
            cells[stringPos]['cellState'] = 'air'
            cells[stringPos]['color'] = (1.0, 1.0, 1.0)
    posMap = buildPosMap(cells)
    for cellKey, cellData in cells.items():
        if cellData['cellState'] == 'air':
            cnt = countAirNeighbors(cellKey, posMap)
            pct = cnt / 8.0
            r = 1.0
            g = 1.0 - pct
            b = 1.0 - pct
            cellData['color'] = (r, g, b)

def spawnAir(spawnSpacing):
    global cells, columnCount
    spacingValue = spawnSpacing + 1
    for cellIndex in range(columnCount):
        if cellIndex % spacingValue == 0:
            cells[str(cellIndex)]['cellState'] = 'air'
            cells[str(cellIndex)]['color'] = (1.0, 1.0, 1.0)

def run(delay=tickSpeed, spawnDelay=2, spawnSpacing=1):
    global isRunning, viscosity
    if spawnDelay < 1:
        spawnDelay = 1
    isRunning = True
    iterationCount = 0
    spawnAir(spawnSpacing)
    drawGridAssets()
    fpsAverage = []
    sampleSize = 10
    while isRunning:
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
        print(f"fps: {fps}, step {iterationCount}")

def pauseRun():
    global isRunning
    isRunning = False

screen.onscreenclick(onMouseLeft, 1)
screen.onscreenclick(onMouseRight, 3)
screen.onkey(run, "Return")
screen.onkey(pauseRun, "Escape")
screen.mainloop()
