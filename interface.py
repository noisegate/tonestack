import curses
import serial
from time import sleep

ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate=9600,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
    )

class Box(object):

    def __init__(self, screen, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen = screen

    def draw(self):

        for x in range(self.width-1):
            self.screen.addch(self.y, self.x+x, curses.ACS_HLINE)
            self.screen.addch(self.y+self.height-1, self.x+x, curses.ACS_HLINE)
        for y in range(self.height-1):
            self.screen.addch(self.y+y, self.x, curses.ACS_VLINE)
            self.screen.addch(self.y+y, self.x+self.width-1, curses.ACS_VLINE)

        #self.screen.scrollok(True)
        self.screen.addch(self.y, self.x, curses.ACS_ULCORNER)
        self.screen.addch(self.y, self.x+self.width-1, curses.ACS_URCORNER)
        self.screen.addch(self.y+self.height-1, self.x+self.width-1, curses.ACS_LRCORNER)
        self.screen.addch(self.y+self.height-1, self.x, curses.ACS_LLCORNER)

class Hline(object):

    def __init__(self, screen, x, y, length):
        self.screen = screen
        self.x = x
        self.y = y
        self.lenght = length

    def draw(self):

        for x in range(self.lenght-1):
            self.screen.addch(self.y, self.x + x, curses.ACS_HLINE)

        self.screen.addch(self.y, self.x, curses.ACS_LTEE)
        self.screen.addch(self.y, self.x+self.lenght-1, curses.ACS_RTEE)

class Checkbox(object):

    pass



class Bar(object):
    TONE = 1
    VOL = 2

    def __init__(self, screen,x ,y, name, legend, function):
        self.screen = screen
        self.x = x
        self.y = y
        self.height = 20
        self.width = 5
        self.name = name
        self.legend = legend
        self.function = function

    def set(self, val):

        if (self.function == self.TONE):
            ival = int(val * self.height/2)+self.height/2
            self.screen.addstr(self.y-1, self.x, "{0}dB".format(val/0.04*0.5))
        else:
            ival = int(val * self.height)
            self.screen.addstr(self.y-1, self.x, "{0}%".format(val*100))

        self.screen.addstr(self.y-2, self.x, self.name)
        self.screen.addstr(self.y+self.height+2,self.x,self.legend)

        for i in range(self.height):
            for j in range(self.width):
                self.screen.addstr(self.y + i, self.x+j, " ")

        for i in range(ival):
            for j in range(self.width):
                self.screen.addstr(self.y + self.height - i, self.x+j, " ", curses.A_REVERSE)

        for j in range(self.width):
            self.screen.addch(self.y+self.height/2, self.x+j, curses.ACS_HLINE, curses.A_REVERSE)


class Interface(object):

    def __init__(self):
        self.screen = curses.initscr()
        self.size = self.screen.getmaxyx()
        self.height = self.size[0]
        self.width = self.size[1]
        curses.cbreak()
        curses.noecho()
        curses.curs_set(0)
        self.screen.nodelay(1)#nonblocking fethc getch
        self.callback=None
                                           
        self.halfwidth = self.width/2
        self.halfheight = self.height/2
        
        ser.isOpen()

        offset = 35

        self.Bassbar = Bar(self.screen, offset+0,15, "115Hz","B/b", Bar.TONE )
        self.Midbassbar = Bar(self.screen, offset+10, 15,"330Hz","N/n", Bar.TONE)
        self.Midbar = Bar(self.screen, offset+20,15,"990Hz","M/m",Bar.TONE)
        self.Midtreblebar = Bar(self.screen,offset+30, 15,"3kHz","Y/y",Bar.TONE)
        self.Treblebar = Bar(self.screen, offset+40, 15,"9.9kHz","T/t",Bar.TONE)
        self.Volbar = Bar(self.screen, offset + 80, 15, "Volume","V/v",Bar.VOL)

        self.Eqbox = Box(self.screen, offset-2, 12 , 90, 28)
        self.Eqsplit = Hline(self.screen, offset-2, 25, 90)
        ser.write('?')


    def loop(self):
        go = 1

        while(go):
            sleep(0.1)
            c = self.screen.getch()
            if (c == ord('B')):
                self.screen.addstr(2,2,"State change: Bass +".ljust(30))
                ser.write('B')
            if (c == ord('b')):
                self.screen.addstr(2,2,"State change: Bass -".ljust(30))
                ser.write('b')
            if (c == ord('M')):
                self.screen.addstr(2,2,"State change: Mid +".ljust(30))
                ser.write('M')
            if (c == ord('m')):
                self.screen.addstr(2,2,"State change: Mid -".ljust(30))
                ser.write('m')
            if (c == ord('N')):
                self.screen.addstr(2,2,"State change: Mid Bass +".ljust(30))
                ser.write('N')
            if (c == ord('n')):
                self.screen.addstr(2,2,"State change: Mid Bass -".ljust(30))
                ser.write('n')
            if (c == ord('T')):
                self.screen.addstr(2,2,"State change: Treble +".ljust(30))
                ser.write('T')
            if (c == ord('t')):
                self.screen.addstr(2,2,"State change: Treble -".ljust(30))
                ser.write('t')
            if (c == ord('Y')):
                self.screen.addstr(2,2,"State change: Mid Treble +".ljust(30))
                ser.write('Y')
            if (c == ord('y')):
                self.screen.addstr(2,2,"State change: Mid Treble -".ljust(30))
                ser.write('y')
            if (c == ord('d')):
                self.screen.addstr(2,2,"State change: tone defeat".ljust(30))
                ser.write('d')
            if (c == ord('l')):
                self.screen.addstr(2,2,"left".ljust(30))
                ser.write('l')
            if (c == ord('r')):
                self.screen.addstr(2,2,"right".ljust(30))
                ser.write('r')


            if (c == ord('v')):
                self.screen.addstr(2,2,"V".ljust(30))
                ser.write('v')
            if (c == ord('V')):
                self.screen.addstr(2,2,"V".ljust(30))
                ser.write('V')

            if (c == ord('q')):
                self.quit()
                return

            i=0

            msg = []
            while ser.inWaiting() > 0:
                #self.screen.addstr(3,2+i,ser.read(1))
                dummy = ser.read(1)
                self.screen.addstr(4,2+i,dummy)
                msg.append(dummy)
                #self.screen.addstr(3,2,s)
                i=i+1
                #self.screen.addstr(0,0,"Tone Control Interface".center(self.width), curses.A_REVERSE)
                #self.screen.addstr(5,2, "V = Volume")
                #self.screen.addstr(6,2, "B = Bass  ")
                #self.screen.addstr(7,2, "N = Mid bass")
                #self.screen.addstr(8,2, "M = Mid   ")
                #self.screen.addstr(9,2, "Y = Mid treble")
                #self.screen.addstr(10,2,"T = Treble")
                #self.screen.addstr(11,2,"d = defeat")
                #self.screen.addstr(12,2,"E = Bass  Enhance")
                #self.screen.addstr(13,2,"q = quit  ")

            if (i>0):
                self.screen.addstr(3,2,''.join(msg))
                self.Eqbox.draw()
                self.Eqsplit.draw()
                msgstr = ''.join(msg)
                vals = msgstr.split(':')
                self.Bassbar.set(float(vals[0]))
                self.Midbassbar.set(float(vals[1]))
                self.Midbar.set(float(vals[2]))
                self.Midtreblebar.set(float(vals[3]))
                self.Treblebar.set(float(vals[4]))
                self.Volbar.set(float(vals[6]))
                self.screen.addstr(0,0,"Tone Control Interface".center(self.width), curses.A_REVERSE)
                self.screen.refresh()


    def quit(self):
        self.screen.clear()
        self.screen.refresh()
        curses.endwin()
        ser.close()
if __name__ == '__main__':
    instance = Interface()
    instance.loop()

