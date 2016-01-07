import curses
import serial

ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate=9600,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
    )

class Interface(object):

    def __init__(self):
        self.screen = curses.initscr()
        self.size = self.screen.getmaxyx()
        self.height = self.size[0]
        self.width = self.size[1]
        curses.cbreak()
        curses.noecho()
        self.screen.nodelay(1)#nonblocking fethc getch
        self.callback=None
                                           
        self.halfwidth = self.width/2
        self.halfheight = self.height/2
        
        ser.isOpen()

    def loop(self):
        go = 1

        while(go):
            c = self.screen.getch()
            if (c == ord('B')):
                self.screen.addstr(2,2,"Bass +".ljust(30))
                ser.write('B')
            if (c == ord('b')):
                self.screen.addstr(2,2,"Bass -".ljust(30))
                ser.write('b')
            if (c == ord('M')):
                self.screen.addstr(2,2,"Mid +".ljust(30))
                ser.write('M')
            if (c == ord('m')):
                self.screen.addstr(2,2,"Mid -".ljust(30))
                ser.write('m')
            if (c == ord('N')):
                self.screen.addstr(2,2,"Mid Bass +".ljust(30))
                ser.write('N')
            if (c == ord('n')):
                self.screen.addstr(2,2,"Mid Bass -".ljust(30))
                ser.write('n')
            if (c == ord('T')):
                self.screen.addstr(2,2,"Treble +".ljust(30))
                ser.write('T')
            if (c == ord('t')):
                self.screen.addstr(2,2,"Treble -".ljust(30))
                ser.write('t')
            if (c == ord('Y')):
                self.screen.addstr(2,2,"Mid Treble +".ljust(30))
                ser.write('Y')
            if (c == ord('y')):
                self.screen.addstr(2,2,"Mid Treble -".ljust(30))
                ser.write('y')
            if (c == ord('d')):
                self.screen.addstr(2,2,"defeat".ljust(30))
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

            while ser.inWaiting() > 0:
                self.screen.addstr(3,2+i,ser.read(1))
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

                self.screen.refresh()



    def quit(self):
        self.screen.clear()
        self.screen.refresh()
        curses.endwin()
        ser.close()
if __name__ == '__main__':
    instance = Interface()
    instance.loop()

