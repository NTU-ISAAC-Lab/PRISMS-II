SPECIFICATIONS
--------------
FOCUSER
MODEL: MoonLite Model CR Newtonian Focusers
SIZE: 2"
CONTROLLER: Mini-V2 controller for High res stepper motors (Model MTS-500-V2)
LINK: https://focuser.com/products.php [Last Accessed 07/12/2022]

BRAND
NAME: Moonlite
WEBSITE: https://focuser.com/ [Last Accessed 08/12/2022]
______________________________________________________________________________________________
POSTION TO STEPS:
WARNING! when max is reached the stepper motor will keep moving while the mechanism is still and assume this is the distance.
	     Can not move to a negative position, make sure focuser is set beyond 0 by a fair amount
	     to avoid errors.

05/12/2023: In focus range with current lens configuration (blue cuff on lens); 2.290 - 17 m

______________________________________________________________________________________________
EXTERNAL SOFTWARE (NB! This software is not required to run PRISMS II)
-----------------
EXTERNAL SOFTWARE FOR INTERFACING: Moonlite Single Focuser
UTILITY: test the focuser is running as expected.
LINK: https://focuser.com/downloads.php [Last Accessed 08/12/2022]
______________________________________________________________________________________________
Additional notes:
This focuser by standard is ascii encoded, so all commands must be encoded before writting to the serial
e.g. command = ':GP#'
     command_to_serial = command.encode("ascii")

If in doubt about encoding, look at the port in powershell:
>new-Object System.IO.Ports.SerialPort COM7,115200,None,8,one
>$port
BaseStream             :
BaudRate               : 115200
BreakState             :
BytesToWrite           :
BytesToRead            :
CDHolding              :
CtsHolding             :
DataBits               : 8
DiscardNull            : False
DsrHolding             :
DtrEnable              : False
Encoding               : System.Text.ASCIIEncoding
Handshake              : None
IsOpen                 : False
NewLine                :

Parity                 : None
ParityReplace          : 63
PortName               : COM7
ReadBufferSize         : 4096
ReadTimeout            : -1
ReceivedBytesThreshold : 1
RtsEnable              : False
StopBits               : One
WriteBufferSize        : 2048
WriteTimeout           : -1
Site                   :
Container              :


