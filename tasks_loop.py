import threading
import time
import natsort
import os


class DoTasks(threading.Thread):
    def __init__(self, smbdb, tlm_dict, bang_bangs, adcs, heaters, qcommand, qtransmit):
        self.db = smbdb
        self.tlm_dict = tlm_dict
        self.bb = bang_bangs
        self.adcs = adcs
        self.heaters = heaters
        self.qcmd = qcommand
        self.qxmit = qtransmit
        threading.Thread.__init__(self)

    def run(self):
        try:
            while True:
                # See if there is command to execute.
                if not self.qcmd.empty():
                    self.process_queued_cmd(self.qcmd.get())
                    self.qcmd.task_done()

                # Read out ADC conversion data
                for adc in self.adcs:
                    adc.read_conversion_data()

                time.sleep(.5)

        except KeyboardInterrupt:  # Ctrl+C pressed
            del self

    def process_queued_cmd(self, cmd_dict):
        if cmd_dict['ERROR'] < 0:
            result = -1

        else:
            if cmd_dict['CMD_TYPE'] == '?' and cmd_dict["READ"] == 1:
                result = self.process_read_cmd(cmd_dict)
            elif cmd_dict['CMD_TYPE'] == '~' and cmd_dict["WRITE"] == 1:
                result = self.process_write_cmd(cmd_dict)
            else:
                cmd_dict['ERROR'] = -1
                output = "bad command"
                self.qxmit.put(output.encode('utf-8'))

    def process_read_cmd(self, cmd_dict):
        output = ''
        cmd = cmd_dict['CMD']
        p1 = cmd_dict['P1_DEF']
        p1min = cmd_dict["P1_MIN"]
        p1max = cmd_dict["P1_MAX"]

        if p1 < p1min or p1 > p1max:
            output = "bad command"
            self.qxmit.put(output.encode('utf-8'))
            return -1

        if not self.qxmit.full():

            # fetch Heater Mode (0=Disabled, 1=Fixed Percent, 2=PID Control)
            if cmd == 'L':
                htr_dict = self.db.db_fetch_heater_params(p1)
                value = str(htr_dict['mode'])
                output = str("heater_mode = %s" % value)

            # Read temperatures from all channels
            elif cmd == 't':
                for item in natsort.natsorted(self.tlm_dict):
                    if 'rtd' in item:
                        output += item + " = {0:3.3f}\r\n".format(self.tlm_dict[item])

            # Read RTD Resistance at temperature
            elif cmd == 'r':
                for item in natsort.natsorted(self.tlm_dict):
                    if 'adc_sns_ohms' in item:
                        output += item + " = {0:6.1f}ohms\r\n".format(self.tlm_dict[item])

            # Read voltage at a temp sensor.
            elif cmd == 'v':
                for item in natsort.natsorted(self.tlm_dict):
                    if 'adc_sns_volts' in item:
                        output += item + " = {0:0.6f}v\r\n".format(self.tlm_dict[item])

            # Read Board ID
            elif cmd == 'A':
                value = self.db.db_fetch_board_id()
                output = str("board_id = %s" % value)

            # Read Hi Power output state
            elif cmd == 'F':
                value = self.bb[p1-1].output_state
                output = str("output_state = %s" % value)

            # Read Software Rev
            elif cmd == 'N':
                value = self.db.db_software_rev()
                output = "software_rev={0:3.3f}".format(value)

            # Read Temp Unit Setting (0=K 1=C 2=F).
            elif cmd == 'U':
                value_dict = self.db.db_adc_fetch_params(p1)
                output = str("Temp_unit = %s" % value_dict["temperature_unit"])

            # Read Sensor Type(1=PT100 2=PT1000 3=NCT_THERMISTOR)
            elif cmd == 'S':
                value_dict = self.db.db_adc_fetch_params(p1)
                output = str("sensor_type = %s" % value_dict["sensor_type"])

            # Read PID Proportional P factor.
            elif cmd == 'P':
                value_dict = self.db.db_fetch_heater_params(p1)
                output = str("P_term = %s" % value_dict["P"])

            # Read PID Integral I factor.
            elif cmd == 'I':
                value_dict = self.db.db_fetch_heater_params(p1)
                output = str("I_term = %s" % value_dict["I"])

            # Read PID Derivative D factor
            elif cmd == 'D':
                value_dict = self.db.db_fetch_heater_params(p1)
                output = str("D_term = %s" % value_dict["D"])

            # Read Heater Looop Set Point.
            elif cmd == 'W':
                value_dict = self.db.db_fetch_heater_params(p1)
                output = str("Set_pt= %s" % value_dict["set_pt"])

            # Read Heater Loop Control Sensor Number.
            elif cmd == 'J':
                value_dict = self.db.db_fetch_heater_params(p1)
                output = str("Ctrl Sensor = %s" % value_dict["ctrl_sensor"])

            # Read Heater Current (A).
            elif cmd == 'V':
                value_dict = self.db.db_fetch_heater_params(p1)
                output = str("htr_current = %s" % value_dict["htr_current"])

            # Read One Temp Sensor.
            elif cmd == 'K':
                output = "temp={0:3.3f}K".format(self.tlm_dict["rtd" + str(p1)])

            # Read Exciation Current Setting.
            elif cmd == 'X':
                setting_dict = self.db.db_adc_fetch_names_n_values('IOCon1', p1)
                value = setting_dict['iout0']
                output = "excitation_current_setting = %s" % value

            # Read Filter Type Setting.
            elif cmd == 'Q':
                setting_dict = self.db.db_adc_fetch_names_n_values('Filter_0', p1)
                value = setting_dict['filter']
                output = "filter_setting = %s" % value

            # Read sensor type connected to ADC.
            elif cmd == 'S':
                value_dict = self.db.db_fetch_heater_params(p1)
                output = str("sns_type = %s" % value_dict["sensor_type"])

            # Read humidity sensor
            elif cmd == "H":
                output = str("cmd not yet implemented")

            else:
                return -1

            self.qxmit.put(output.encode('utf-8'))
            return 1

    def process_write_cmd(self, cmd_dict):
        cmd = cmd_dict['CMD']
        p1 = cmd_dict['P1_DEF']
        p2 = cmd_dict['P2_DEF']
        p1min = cmd_dict["P1_MIN"]
        p1max = cmd_dict["P1_MAX"]
        p2min = cmd_dict["P2_MIN"]
        p2max = cmd_dict["P2_MAX"]
        output =  '~' + cmd + ', ' + str(p1) +  ', ' + str(p2)

        if p1 < p1min or p1 > p1max or p2 < p2min or p2 > p2max:
            output = "bad command"
            self.qxmit.put(output.encode('utf-8'))
            return -1

        # set heater mode
        if cmd == 'L':
            self.heaters[p1 - 1].set_htr_mode(p2)

        # Store Board ID
        elif cmd == 'A':
            self.db.db_update_board_id(p1)

        # Store Temp Unit (0=K;1=C;2=F)
        elif cmd == 'U':
            self.adcs[p1-1].adc_set_temp_units(p2)

        # Set Heater Current (Amps)
        elif cmd == 'V':
            self.heaters[p1 - 1].htr_set_heater_current(p2)

        # Store Excit uA (0=NONE,1=50,2=100,3=250,4=500,5=750, 6,7=1000)
        elif cmd == 'X':
            self.adcs[p1-1].set_exciatation_current(p2)

        # ADC Filter Setting
        # (0=sinc^4 1=rsv'd 2=sinc^3 3=rsv'd 4=fast sinc^4 5=fast sinc^3 6=rsv'd 7=post filter enabled
        elif cmd == 'Q':
            self.adcs[p1 - 1].set_filter_type(p2)

        # Heater P Setting
        elif cmd == 'P':
            self.db.db_update_htr_params(p2, 'P', p1)
            self.heaters[p1-1].heater_p_term = p2

        # Heater I Setting
        elif cmd == 'I':
            self.db.db_update_htr_params(p2, 'I', p1)
            self.heaters[p1 - 1].heater_i_term = p2

        # Heater D Setting
        elif cmd == 'D':
            self.db.db_update_htr_params(p2, 'D', p1)
            if p1 < len(self.heaters) + 1:
                self.heaters[p1 - 1].heater_d_term = p2

        # Heater Loop Control Sensor
        elif cmd == 'J':
            self.db.db_update_htr_params(p2, 'ctrl_sensor', p1)
            self.heaters[p1 - 1].heater_ctrl_sensor = p2

        # Set Heater Loop Setpoint
        elif cmd == 'W':
            self.db.db_update_htr_params(p2, 'set_pt', p1)
            self.heaters[p1 - 1].heater_set_pt = p2

        # Enable/disable High Power Output
        elif cmd == 'F':
            if int(p2) == 1:
                self.bb[p1-1].power_on_output()
            else:
                self.bb[p1 - 1].power_off_output()

        # set sensor type that is connected to ADC
        elif cmd == 'S':
            self.adcs[p1 - 1].adc_set_sensor_type(p2)

        # reboot rasberry pi
        elif cmd == 'E':
            os.system('sudo shutdown -r now')
            output = '~' + cmd

        else:
            return -1
        self.qxmit.put(output.encode('utf-8'))
        return 1

#TODO: wire in command for reading humidity sensor
