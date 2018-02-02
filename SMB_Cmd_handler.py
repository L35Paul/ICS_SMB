
"""
	- Action Commands

	CmdType     | CmdChar     | P1      | P1 range | P2       | P2 Range  | Description
	------------|-------------|---------|----------|----------|-----------|-------------------------------------------
	~           |  A          | Char    | A to Z   | n/a      | n/a       | Store Board ID Char
	~           |  B          | Sens#   | 1 to 12  | Beta     | 0 to +inf | Store thermistor BETA value to EEPROM
	~           |  C          | n/a     | n/a      | n/a      | n/a       | Clear and restore
	~           |  D          | LOOP#   | 1 to 2   | Value    | 0 to 100  | PID Derivative D factor
	~           |  E          | n/A     | n/a      | n/A      | n/a       | Reset CPU
	~           |  F          | ID      | 1 to  2  | state    | 0 t0 1    | Switched High Power output
	~           |  G          | Sens#   | 1 to 12  | gain     | infinite  | Store gain value to EEPROM
	~           |  I          | LOOP#   | 1 to 2   | Value    | 0 to 100  | PID Integral I factor
	~           |  J          | LOOP#   | 1 to 2   | Value    | 1 to 12   | Loop control sensor#
	~           |  L          | HtrEna  | 1 to 2   | /Dis Ena | 0,1,2     | 0=Disabled, 1=Fixed Percent, 2=PID Control
	~           |  M          | Samples | 1 to 51  | n/a      | n/a       | Store #of Over samples to use
	~           |  O          | Sens#   | 1 to 12  | offset   | infinite  | Store Resistance offset in ohms to EEPROM
	~           |  P          | LOOP#   | 1 to 2   | Value    | 0 to 100  | PID Proportional P factor
	~           |  Q          | A/D #   | 1 to 6   | Fltr Val | 0 to 15   | ADC Filter Setting
	~           |  R          | Sens#   | 1 to 12  | R@25C    | infinite  | Store thermistor Resistance @25C to EEPROM
	~           |  S          | Sens#   | 1 to 12  | SnsType  | infinite  | Store Sensor Type (0=RAW;1=DT670;2=THERMISTOR;3=RTD)
	~           |  T          | Sens#   | 1 to 12  | n/a      | n/a       | Store Transmit Temp Data setting (0=FALSE;1=TRUE)
	~           |  U          | Sens#'s | 12 bits  | Units    | 0,1,2     | Store Temperature Units to EEPROM (0=K;1=C;2=F)
	~           |  V          | DAC#    | 1 to 2   | Value    | 0 to 100% | Set Heater power %
	~           |  W          | LOOP#   | 1 to 2   | Value    | -460->500 | Set LOOP SetPoint
	~           |  X          | A/D #   | 1 to 6   | Current  | 0 to 3    | Store Excitation current setting to EEPROM (0=NONE, 1=10uA, 2=220uA, 3=1mA)
	~           |  Z          | DAC#    | 1 to 2   | counts   | 0 to 2046 | set DAC output
	~           |  a          | Const#  | 0 to 5   | Value    | +/- inf   | Store RTD polynomial constants K5X^5 + K4X^4 + K3X^3 + K2X^2 + K1X + K0
	~           |  g          | Sens#   | 1 to 12  | AD gain  | 1,2,4,8...| Store AD Amplifier gain value to EEPROM
	~           |  f          | Sens#   | 1 to 12  | Ref Volt | 1.0 to 5.0| Store AD Reference voltage used for each channel
	~           |  j          | voltage | 0 to 1.25| n/a      | n/a       | Store Low Voltage Threshold
	~           |  c          | A/D #   | 1 to 6   | n/a      | n/a       | Initialize the ADC

	- Query Commands

	CmdType     | CmdChar     | P1      | P1 range | Returns   | Range     | Description
	------------|-------------|---------|----------|-----------|-----------|-------------------------------------------
	?           |  A          | Char    | A to Z   | Board ID  | n/a       | Read Board ID Char
	?           |  B          | Sens#   | 1 to 12  | TBeta     | 0 to +inf | Read thermistor BETA value from EEPROM
	?           |  C          | Sens#   | 1 to 12  | Cal       | n/a       | Read temp cal params from EEPROM
	?           |  D          | LOOP#   | 1 to 2   | D Value   | 0 to 100  | Read PID Derivative D factor
	?           |  F          | ID      | 1 to  2  | Pwr Stat  | 0 to 1    | Read Switched High Power output Status
	?           |  G          | Sens#   | 1 to 12  | gain      | 0 to +inf | Read gain value from EEPROM
	?           |  H          | n/A     | n/a      | Humidity  | 0 to 100% | Read Humidity Sensor (Humidity : Temp)
	?           |  I          | LOOP#   | 1 to 2   | I Value   | 0 to 100  | Read PID Integral I factor
	?           |  J          | LOOP#   | 1 to 2   | Loop Sns# | 1 to 12   | Read Loop control sensor#
	?           |  K          | Sen#    | 1 to 12  | Temp      | +/-inf    | Read sensor temperature
	?           |  L          | HtrEna  | 1 to 2   | Htr Stat  | 0,1,2     | Read Htr Amp status(0=Disabled, 1=Fixed Percent, 2=PID Control)
	?           |  M          | Samples | 1 to 51  | OverSmpl# | 0 to 100  | Read #of Over samples to use
	?           |  N          | SW Ref  | n/a      | Rev       | n/a       | Read the software revision
	?           |  O          | Sens#   | 1 to 12  | T offset  | +/-inf    | Read Resistance offset in ohms from EEPROM
	?           |  P          | LOOP#   | 1 to 2   | P Value   | 0 to 100  | Read PID Proportional P factor
	?           |  Q          | A/D #   | 1 to 6   | Fltr Val  | 0 to 15   | Read Filter Setting
	?           |  R          | Sens#   | 1 to 12  | R@25C     | 0 to +inf | Read thermistor Resistance @25C from EEPROM
	?           |  S          | Sens#   | 1 to 12  | SnsType   | 0,1,2,3   | Read SensorType (0=RAW;1=DT670;2=THERMISTOR;3=RTD)
	?           |  T          | Sens#   | 1 to 12  | Xmit?     | 0 to 1    | Read Transmit Temp Data setting (0=FALSE;1=TRUE)
	?           |  U          | Sens#   | 1 to 12  | Units     | 0,1,2     | Read Temperature Units from EEPROM (0=K;1=C;2=F)
	?           |  V          | DAC#    | 1 to 2   | %         | 0 to 100% | Read Heater power %
	?           |  W          | LOOP#   | 1 to 2   | Value     | -460->500 | Read LOOP SetPoint
	?           |  X          | A/D #   | 1 to 6   | Current   | 0 to 3    | Store Excitation current setting to EEPROM (0=NONE, 1=10uA, 2=220uA, 3=1mA)
	?           |  a          | Const#  | 0 to 5   | Constants | +/- inf   | Read RTD polynomial constants K5X^5 + K4X^4 + K3X^3 + K2X^2 + K1X + K0
	?           |  r          | Sens#   | 1 to 12  | R sensor  | 0 to inf  | Read RTD Resistance at temperature
	?           |  g          | Sens#   | 1 to 12  | AD gain   | 1,2,4,8...| Read AD Amplifier gain value from EEPROM
	?           |  v          | Sens#   | 1 to 12  | V sensor  | 0 to inf  | Read RTD Voltage at temperature
	?           |  f          | Sens#   | 1 to 12  | Ref Volt  | 1.0 to 5.0| Read AD Reference voltage used for selected channel
	?           |  t          | n/a     | n/a      | temps     |  +/- inf  | Read temperatures from all channels
	?           |  i          | Heater# | 1 to 2   | Amps      |  0 to  .3 | Read Heater Current
	?           |  j          | voltage | 0 to 1.25| n/a       | n/a       | Read Low Voltage Threshold
"""
from xml.dom import minidom

import Gbl

