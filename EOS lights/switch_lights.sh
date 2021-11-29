#!/usr/bin/bash

# EOS passes env variables:
# OPERSTATE=linkdown
# OPERSTATE=linkup
# INTF=EthernetX

# The Light ID maps to the ethernet interface
# Ethernet1 -> Light ID1
# Ethernet2 -> Light ID2

LIGHTID=${INTF: -1}

if [ "$OPERSTATE" = "linkdown" ]; then
   MODE=off
fi

if [ "$OPERSTATE" = "linkup" ]; then
   MODE=on
fi

CMD="/mnt/flash/eos_lights.py --controller 10.10.0.48 --key aHo3iNrzkdmw3ehRUrn8cMYq5YcwPgKdsvtE7Opc --$MODE $LIGHTID"
$CMD
