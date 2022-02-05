from tkinter import *

class region:
    def __init__(self, x1, y1, x2, y2, theDomain):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.neighbors = list()
        self.domainReset = list(theDomain)
        self.domain = theDomain
        self.tried = set()
        self.color = 'white'
        self.color_index = int()
        canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill="white", outline='black', width=10)

    def color_reg(self, c):
        self.color = c
        square = canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill=c, outline='black', width=10)

    def neighbors(self):
        return self.neighbor

    def set_neighbors(self, array):
        self.neighbor = list(array)

    def reset_domain(self):
        for y in self.domain:
            self.domain.remove(y)
        for x in self.domainReset:
            self.domain.append(x)

    def updateScreen(self):
        c = self.color
        square = canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill=c, outline='black', width=10)

window = Tk()
window.title("Map Coloring")

GAME_HEIGHT = 700
GAME_WIDTH = 700
SPEED = 1500
NUM_OF_COLORS = 3
CURRENT_ASSIGNMENTS = 0
DEAD_ENDS = 0
CONSTRAINTS_CHECKED = 0
TYPE = ""

def type_set(x="all"):
    global TYPE
    if x == "ass":
        TYPE = "Assignments Only"
    elif x == "neb":
        TYPE = "Neighbors"
    elif x == "red":
        TYPE = "Reduced Domain"
    elif x == "sing":
        TYPE = "Single Item Domain"
    elif x == "all":
        TYPE = "All regions"

mb = Menubutton(window, text="Concider", relief=RAISED)
mb.menu = Menu(mb)
mb["menu"] = mb.menu
mb.menu.add_radiobutton(label="Assigments Only", command=lambda: type_set("ass"))
mb.menu.add_radiobutton(label="Neighbors", command=lambda: type_set("neb"))
mb.menu.add_radiobutton(label="Reduced Domain", command=lambda: type_set("red"))
mb.menu.add_radiobutton(label="Single Item Domain", command=lambda: type_set("sing"))
mb.menu.add_radiobutton(label="All regions", command=lambda: type_set("all"))
mb.pack()
#speed = Menubutton(window, text="Speed", relief=RAISED)
#speed.menu = Menu(speed)
#speed["menu"] = speed.menu
#speed.menu.add_radiobutton(label="Fast")
#speed.menu.add_radiobutton(label="Slow")
#speed.pack()
start_button = Button(window, text="Start", font=('consolas', 20))
start_button.pack()
ca_label = Label(window, text="Current Assignments:{}".format(CURRENT_ASSIGNMENTS), font=('consolas', 20))
ca_label.pack()
de_label = Label(window, text="Dead Ends:{}".format(DEAD_ENDS), font=('consolas', 20))
de_label.pack()
cc_label = Label(window, text="Constraints Checked:{}".format(CONSTRAINTS_CHECKED), font=('consolas', 20))
cc_label.pack()
nc_label = Label(window, text="Number of Colors:{}".format(NUM_OF_COLORS), font=('consolas', 20))
nc_label.pack()

window.rowconfigure(0, minsize=50)
window.columnconfigure(0, minsize=50)

canvas = Canvas(window, bg='white', height=GAME_HEIGHT, width=GAME_WIDTH)
# canvas.grid(row=2, column=[0, 1])
canvas.pack()

DOMAIN = ['red', 'green', 'blue']
COLORS = ['red', 'green', 'blue', 'yellow']
INITIALDOMAIN = [True, True, True, True]

one = region(10, 10, 200, 200, INITIALDOMAIN)
two = region(200, 10, 410, 410, INITIALDOMAIN)
three = region(10, 200, 200, 690, INITIALDOMAIN)
four = region(200, 410, 690, 690, INITIALDOMAIN)
five = region(410, 10, 690, 410, INITIALDOMAIN)

one.set_neighbors({two, three})
two.set_neighbors({one, three, four, five})
three.set_neighbors({one, two, four})
four.set_neighbors({three, two, five})
five.set_neighbors({two, four})

regions = [two, five, three, four, one]

COLORS = ['red', 'green', 'blue', 'yellow']

def pack():
    ca_label.config(text="Current Assignmnets:{}".format(CURRENT_ASSIGNMENTS))
    de_label.config(text="Dead Ends:{}".format(DEAD_ENDS))
    cc_label.config(text="Constraints Checked:{}".format(CONSTRAINTS_CHECKED))

def reset():
    global CURRENT_ASSIGNMENTS
    global DEAD_ENDS
    global CONSTRAINTS_CHECKED
    CURRENT_ASSIGNMENTS = 0
    DEAD_ENDS = 0
    CONSTRAINTS_CHECKED = 0

def dfs(regionToColor, colorPosition):
    domain = regions[regionToColor].domain.copy()
    neigbhors_domains_upon_this_call = dict()
    # save all neighbor domains upon this call
    for n in regions[regionToColor].neighbors:
        neigbhors_domains_upon_this_call[n] = n.domain.copy()
    for theColorLoopIndex in range(len(COLORS)):
        colorToTry = (colorPosition + theColorLoopIndex) % (len(COLORS) - 1)
        if regions[regionToColor].domain[colorToTry] == True :
            print(regionToColor)
            print(regions[regionToColor].domain)
            print(regions[regionToColor].domain.copy().pop(theColorLoopIndex))

            print(regions[regionToColor].domain)
            tryColor(regionToColor, colorToTry)
            regions[regionToColor].domain = domain
            for n in regions[regionToColor].neighbors:
                n.domain = neigbhors_domains_upon_this_call[n].get()

def tryColor(regionToColor, colorLoopIndex) :
    global CURRENT_ASSIGNMENTS
    global DEAD_ENDS
    regions[regionToColor].color_reg(COLORS[colorLoopIndex])
    window.after(SPEED, regions[regionToColor].updateScreen)
    CURRENT_ASSIGNMENTS += 1
    for i in range(len(regions[regionToColor].domain)):
        if i != colorLoopIndex:
            regions[regionToColor].domain[i] = False
    variablesConsidered = list()
    if TYPE == "Assignments Only":
        variablesConsidered.append(regions[regionToColor])
    if TYPE == "Neighbors":
        variablesConsidered.append(regions[regionToColor])
        for neighbor in regions[regionToColor].neighbors:
            variablesConsidered.append(neighbor)
    # for each region considered
    for regionConsidered in variablesConsidered:
        domainOfRegionConsidered = regionConsidered.domain
        # for each variable in the domain of the region
        for index in range(len(domainOfRegionConsidered)):
            value = domainOfRegionConsidered[index]
            # if that color is still in the domain, check constraint satisfaction
            if (value):
                for neighbor in regionConsidered.neighbors:
                    # if all other indicies are false
                    copy = neighbor.domain.copy()
                    copy.pop(index)
                    if not any(copy):
                        # remove color from this domain
                        regionConsidered.domain[index] = False
            # if Di empty, backup
            if not any(regionConsidered.domain):
                DEAD_ENDS += 1
                regions[regionToColor].color_reg('white')
                window.after(SPEED, regions[regionToColor].updateScreen)
                return
    if (regionToColor < len(regions) - 1):
        print("dfs")
        window.after(SPEED, dfs, regionToColor + 1, (colorLoopIndex + 1) % (len(COLORS) - 1))

def neighbors(r, c):
    global CURRENT_ASSIGNMENTS
    global DEAD_ENDS
    global CONSTRAINTS_CHECKED
    if r < len(regions):
        reg = regions[r]
        if len(reg.tried) == NUM_OF_COLORS:
            x = (regions[r - 1].color_index + 1) % NUM_OF_COLORS
            reg.tried.clear()
            window.after(SPEED, reg.color_reg, 'white')
            CURRENT_ASSIGNMENTS -= 1
            DEAD_ENDS += 1
            pack()
            reg.domain = list()
            for y in (0, len(DOMAIN) - 1):
                reg.domain[x] == DOMAIN[y]
            window.after(SPEED, neighbors, r - 1, x)
        else:
            col = COLORS[c]
            reg.color = col
            reg.color_index = c
            reg.tried.add(col)
            reg.domain = list()
            reg.domain.append(col)
            CURRENT_ASSIGNMENTS += 1
            pack()
            window.after(SPEED, reg.color_reg, col)
            c = (c + 1) % NUM_OF_COLORS
            procede = TRUE
            for neb in reg.neighbor:
                for a in list(neb.domain):
                    remove = TRUE
                    for b in neb.neighbor:
                        for d in b.domain:
                            CONSTRAINTS_CHECKED += 1
                            if d != a:
                                remove = FALSE
                    if remove:
                        neb.domain.remove(a)
                        if len(neb.domain) == 0:
                            CURRENT_ASSIGNMENTS -= 1
                            pack()
                            procede = FALSE
                            window.after(SPEED, neighbors, r, c)
                            break
                    else:
                        continue
                    break
                else:
                    continue
                break

            if procede:
                window.after(SPEED, neighbors, r + 1, c)


def check(r, c):
    global CURRENT_ASSIGNMENTS
    global DEAD_ENDS
    global CONSTRAINTS_CHECKED
    if r < len(regions):
        reg = regions[r]
        if len(reg.tried) == NUM_OF_COLORS:
            # p = COLORS.index(regions[r - 1].color)
            x = (regions[r - 1].color_index + 1) % NUM_OF_COLORS
            reg.tried.clear()
            window.after(SPEED, reg.color_reg, 'white')
            CURRENT_ASSIGNMENTS -= 1
            DEAD_ENDS += 1
            pack()
            window.after(SPEED, check, r - 1, x)
        else:
            col = COLORS[c]
            reg.color = col
            reg.color_index = c
            reg.tried.add(col)
            CURRENT_ASSIGNMENTS += 1
            pack()
            window.after(SPEED, reg.color_reg, col)
            c = (c + 1) % NUM_OF_COLORS
            j = 0
            procede = TRUE
            while j < len(reg.neighbor):
                neb = reg.neighbor[j]
                CONSTRAINTS_CHECKED += 1
                pack()
                if reg.color == neb.color:
                    procede = FALSE
                    CURRENT_ASSIGNMENTS -= 1
                    pack()
                    window.after(SPEED, check, r, c)
                    j = len(reg.neighbor)
                j = j + 1
            if procede:
                window.after(SPEED, check, r + 1, c)

def newRunWithAllChecks(r, c):
    global CURRENT_ASSIGNMENTS
    global DEAD_ENDS
    global CONSTRAINTS_CHECKED
    if r < len(regions):
        reg = regions[r]
        if len(reg.tried) == NUM_OF_COLORS:
            # p = COLORS.index(regions[r - 1].color)
            x = (regions[r - 1].color_index + 1) % NUM_OF_COLORS
            reg.tried.clear()
            window.after(SPEED, reg.color_reg, 'white')
            CURRENT_ASSIGNMENTS -= 1
            DEAD_ENDS += 1
            pack()
            window.after(SPEED, check, r - 1, x)
        else:
            col = COLORS[c]
            reg.color = col
            reg.color_index = c
            reg.tried.add(col)
            CURRENT_ASSIGNMENTS += 1
            pack()
            window.after(SPEED, reg.color_reg, col)
            c = (c + 1) % NUM_OF_COLORS
            j = 0
            procede = TRUE
            while j < len(reg.neighbor):
                neb = reg.neighbor[j]
                CONSTRAINTS_CHECKED += 1
                pack()
                if reg.color == neb.color:
                    procede = FALSE
                    CURRENT_ASSIGNMENTS -= 1
                    pack()
                    window.after(SPEED, check, r, c)
                    j = len(reg.neighbor)
                j = j + 1
            if procede:
                window.after(SPEED, check, r + 1, c)

def run():
    if TYPE == "Assignments Only":
        check(0,0)
    if TYPE == "Neighbors":
        newRunWithAllChecks(0,0)

start_button['command'] = run

window.mainloop()
