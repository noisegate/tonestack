import curses
import serial

ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate=9600,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
    )

class Bar(object):

    def __init__(self, screen,x ,y, name):
        self.screen = screen
        self.x = x
        self.y = y
        self.height = 10
        self.width = 5
        self.name = name


    def set(self, val):

        ival = int(val * self.height)

        self.screen.addstr(self.y-2, self.x, self.name)

        for i in range(self.height):
            for j in range(self.width):
                self.screen.addstr(self.y + i, self.x+j, " ")

        for i in range(ival):
            for j in range(self.width):
                self.screen.addstr(self.y + self.height - i, self.x+j, " ", curses.A_REVERSE)

        for j in range(self.width):
            self.screen.addstr(self.y+self.height/2, self.x+j, "-", curses.A_REVERSE)

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

        self.Bassbar = Bar(self.screen, 10,20, "Bass" )
        self.Midbassbar = Bar(self.screen, 20, 20,"Alt")
        self.Midbar = Bar(self.screen, 30,20,"Mid")
        self.Midtreblebar = Bar(self.screen,40, 20,"Tenor")
        self.Treblebar = Bar(self.screen, 50, 20,"Treble")

    def loop(self):
        go = 1

        while(go):
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
                self.screen.addstr(0,0,"Tone Control Interface".center(self.width), curses.A_REVERSE)
                self.screen.addstr(5,2, "V = Volume")
                self.screen.addstr(6,2, "B = Bass  ")
                self.screen.addstr(7,2, "N = Mid bass")
                self.screen.addstr(8,2, "M = Mid   ")
                self.screen.addstr(9,2, "Y = Mid treble")
                self.screen.addstr(10,2,"T = Treble")
                self.screen.addstr(11,2,"d = defeat")
                self.screen.addstr(12,2,"E = Bass  Enhance")
                self.screen.addstr(13,2,"q = quit  ")

            if (i>0):
                self.screen.addstr(3,2,''.join(msg))
                msgstr = ''.join(msg)
                vals = msgstr.split(':')
                self.Bassbar.set(float(vals[0]))
                self.Midbassbar.set(float(vals[1]))
                self.Midbar.set(float(vals[2]))
                self.Midtreblebar.set(float(vals[3]))
                self.Treblebar.set(float(vals[4]))
       
                self.screen.refresh()


    def quit(self):
        self.screen.clear()
        self.screen.refresh()
        curses.endwin()
        ser.close()
if __name__ == '__main__':
    instance = Interface()
    instance.loop()

