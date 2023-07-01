import argparse
from collections import deque

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import serial


# plot class
class AnalogPlot:
    # constr
    def __init__(self, strPort, maxLen):
        # open serial port
        self.ser = serial.Serial(strPort, 115200)
        self.ser.readline()

        self.ax = deque([0.0] * maxLen)
        self.ay = deque([0.0] * maxLen)
        self.maxLen = maxLen

        self.letter = ''

    # add to buffer
    def addToBuf(self, buf, val):
        if len(buf) < self.maxLen:
            buf.append(val)
        else:
            buf.pop()
            buf.appendleft(val)

    # add data
    def add(self, data):
        data[0] = 0
        assert (len(data) == 2)
        if self.letter == 'L':
            self.addToBuf(self.ax, data[1])
            self.addToBuf(self.ay, data[0])
        else:
            self.addToBuf(self.ax, data[0])
            self.addToBuf(self.ay, data[1])

    # update plot
    def update(self, frameNum, a0, a1):
        try:
            line = self.ser.readline()
            line = line.decode()[0:-2]

            if line.find('T') != -1:
                self.letter = 'T'
                index = line.find('T')
                line = line[index + 2:]
            else:
                self.letter = 'L'
                index = line.find('L')
                line = line[index + 2:]

            eq_index = line.find('=')
            line = line[eq_index + 1:]
            data = [0, float(line)]
            # print data
            if len(data) == 2:
                if self.letter == 'T':
                    ax.set_ylim(0, 1.2 * max(self.ay))
                else:
                    ax.set_ylim(0, 1.2 * max(self.ax))

                self.add(data)
                a0.set_data(range(self.maxLen), self.ax)
                a1.set_data(range(self.maxLen), self.ay)
        except KeyboardInterrupt:
            print('exiting')

        return a0,

        # clean up

    def close(self):
        # close serial
        self.ser.flush()
        self.ser.close()


def main():
    # create parser
    parser = argparse.ArgumentParser(description="LDR serial")
    # add expected arguments
    parser.add_argument('--port', dest='port', required=True)

    # parse args
    args = parser.parse_args()

    strPort = args.port

    print('reading from serial port %s...' % strPort)

    # plot parameters
    analogPlot = AnalogPlot(strPort, 100)

    print('plotting data...')

    # set up animation
    fig = plt.figure()
    global ax
    ax = plt.axes()
    ax.set_xlim(0, 100)
    a0, = ax.plot([], [], label="Natężenie światła")
    a1, = ax.plot([], [], label="Temperatura")
    ax.legend()
    anim = animation.FuncAnimation(fig, analogPlot.update,
                                   fargs=(a0, a1),
                                   interval=50, blit=False)

    # show plot
    plt.show()

    # clean up
    analogPlot.close()

    print('exiting.')


# call main
if __name__ == '__main__':
    main()
