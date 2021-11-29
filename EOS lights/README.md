# EOS lights
EOS lights is an event handler example

![Topology diagram](https://github.com/aristaiberia/acb21/blob/main/EOS%20lights/images/topology.png)

By using event handlers, EOS lights switchess on and off [Philips Hue Bulbs](https://www.philips-hue.com/) based on interfaces status. It also makes a party if the string **party** is found in the switch logs.

It does it by using the [Philips Hue API](https://developers.meethue.com/develop/get-started-2/) from the Arista switch.

```
event-handler ET1-HANDLER
   trigger on-intf Ethernet1 operstatus
   action bash /mnt/flash/switch_lights.sh
   delay 0
!
event-handler ET2-HANDLER
   trigger on-intf Ethernet2 operstatus
   action bash /mnt/flash/switch_lights.sh
   delay 0
!
event-handler PARTY1
   action bash /mnt/flash/eos_lights.py --controller 10.10.0.48 --key aHo3iNrzkdmw3ehRUrn8cMYq5YcwPgKdsvtE7Opc --party 1
   delay 0
   !
   trigger on-logging
      poll interval 3
      regex party1
!
event-handler PARTY2
   action bash /mnt/flash/eos_lights.py --controller 10.10.0.48 --key aHo3iNrzkdmw3ehRUrn8cMYq5YcwPgKdsvtE7Opc --party 2
   delay 0
   !
   trigger on-logging
      poll interval 3
      regex party2
```
