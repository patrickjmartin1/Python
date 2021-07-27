#!/usr/bin/env python3

import socket
import time
import pyModeS as pms
import csv


# Create a class for storing a modifying data on each ADS-B cue aircraft
class Planes:
    def __init__(self, name):
        # Setup all the initial variables
        self.name = name
        self.msg_odd = ""
        self.msg_even = ""
        self.lat = 0
        self.lon = 0
        self.t_even = 0
        self.t_odd = 0

    def update_msg(self, msg):
        # Update even and odd messages appropriately
        try:
            if pms.adsb.oe_flag(msg):
                self.msg_odd = msg
                self.t_odd = int(time.time())
            else:
                self.msg_even = msg
                self.t_even = int(time.time())
        except RuntimeError:
            print('Error caught in msg update')
            pass

    def update_position(self):
        # Update the position based on even and odd messages
        if self.msg_even == "" or self.msg_odd == "":
            print('Error caught in update position')
            raise RuntimeError("Even and odd messages not populated yet")
        self.lat, self.lon = pms.adsb.position(self.msg_even, self.msg_odd, self.t_even, self.t_odd)

    def update_file(self, csv_name):
        # Update the output file with this cue info
        if self.lat == 0 or self.lon == 0:
            print('Error caught in update file')
            raise RuntimeError("Lat/Lon Have not yet been defined")
        f = open(csv_name, 'a', newline='')
        csv_writer = csv.writer(f, dialect='excel')
        csv_writer.writerow([self.name, self.lat, self.lon, str(time.time())])
        f.close()


def main_func():
    #Create a blank dictionary that will have ICAO numbers as keys and the plane class as a value for each key
    aircraft = {}

    #Setup a log file for storing the data
    save_path = 'C:\\passive_radar\\ads_recordings\\'
    csv_name = save_path + str(int(time.time())) + '_log.csv'
    f = open(csv_name, 'a', newline='')
    csv_writer = csv.writer(f, dialect='excel')
    csv_writer.writerow(['ICAO', 'Lat', 'Lon', 'Time'])
    f.close()

    HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
    # HOST = '192.168.0.8'  # iPad Address
    # HOST = '127.0.1.1'  # Raspberry Pi address
    # HOST = ''  # iPad Address
    PORT = 30002       # Port to listen on (non-privileged ports are > 1023)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print('Connecting...')
        s.connect((HOST, PORT))
        print('Connected! Great Success')
        while True:
            try:
                data = s.recv(1024)
            except:
                data = False
            if data:
                data_full = data.decode()
                data_split = data_full.splitlines()
                for line in data_split:
                    # print(line)
                    msg = line[-29:]
                    dwn_lnk_fmt = pms.df(msg)
                    if dwn_lnk_fmt in [17, 18]:
                        print('Downlink FMT: {dlf}'.format(dlf=dwn_lnk_fmt))
                        icao = pms.adsb.icao(msg)
                        type_code = pms.adsb.typecode(msg)

                        if icao not in aircraft.keys():
                            aircraft.update({icao:Planes(icao)})
                        this_plane = aircraft[icao]

                        if 1 <= type_code <= 4:
                            print('Typecode: {tc}'.format(tc = type_code))
                            print('ICAO: {ic}'.format(ic = icao))
                            callsign = pms.adsb.callsign(msg)
                            print('Callsign: {cs}'.format(cs = callsign))

                        if 5 <= type_code <= 18:
                            print('Typecode: {tc}'.format(tc=type_code))
                            print('ICAO: {ic}'.format(ic=icao))
                            print(msg)
                            try:
                                this_plane.update_msg(msg)
                            except RuntimeError:
                                continue
                            try:
                                this_plane.update_position()
                                print(this_plane.lat, this_plane.lon)
                            except RuntimeError:
                                continue
                            # try:
                            this_plane.update_file(csv_name)
                            # except RuntimeError:
                                # continue

                        if type_code == 19:
                            vel = pms.adsb.velocity(msg)  # Handles both surface & airborne messages
                            heading = pms.adsb.speed_heading(msg)  # Handles both surface & airborne messages
            else:
                time.sleep(1)


if __name__ == "__main__":
    main_func()
