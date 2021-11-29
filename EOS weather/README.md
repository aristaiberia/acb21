# EOS weather
EOS weather is a Custom CLI example.

It creates new commands in Arista EOS CLI.

In this example the new commands allows to use [Openweather](https://openweathermap.org/) in an Arista switch.

The new commands have all the Arista EOS CLI features like the rest: autocompletion, syntax check, etc. They can also be executed via the Arista EOS API like any other command.

The implementation is done with 2 files:
* YAML definition - This component describes all of the static pieces of the CLI extension. This includes any daemons, modes, and commands that need to be defined. The file is Weather.yaml and should reside in /usr/share/CliExtension/
* Command handlers - This component describes the actions that will be performed when a command is entered. Additionally it will also map a command defined in the YAML file to a command handler. The file is Weather.py and should reside in /usr/lib/python2.7/site-packages/CliPlugin/

Once both files are in the right place you should restart ConfigAgent. One way to do it is by running ```bash sudo killall ConfigAgent```

The original locations.json file can be downloaded [here](http://bulk.openweathermap.org/sample/city.list.json.gz) or you can use the locations.json file in this repo that has removed locations with unicode chars.

To use the [Openweather API](https://openweathermap.org/api) you should create a free acount.

With EOS weather you will have some new CLI commands, like ```management weather``` and ```show weather```:

```
VLABTEST#show ?
  aaa                    Show AAA values
  address                Global address locking show commands
  agent                  Show agent settings
<…>
  vxlan                  VXLAN configuration and statistics
  weather                ***weather***
  xmpp                   Show XMPP status
  zerotouch              ZeroTouch status

VLABTEST#configure 
VLABTEST(config)#management ?
<…>
  tech-support  Configure tech-support policy
  telnet        Configure telnet
  weather       ***Configure ACB weather feature***
  xmpp          Configure XMPP
```

You can use the new commands as any other command.

```
VLABTEST(config)#management weather 
VLABTEST(config-mgmt-weather)#?
  apikey         apikey
  locationsfile  locationsfile
  url            url
  ----------------------------------------
  comment        Up to 240 characters, comment for this mode
  default        Set a command to its defaults
  exit           Leave mgmt-weather mode
  no             Disable the command that follows
  show           Display details of switch operation
  !!             Append to comment

VLABTEST(config)#show running-config section weather
management weather
   apikey XXXX
   locationsfile /mnt/flash/locations.json
   url https://api.openweathermap.org/data/2.5/weather
```

```
LABTEST(config)#show weather location name Madrid
name Madrid
id 3117735
pressure 1021 bar
sunset 2021-11-17 16:56:25 UTC
sunrise 2021-11-17 07:03:27 UTC
temp 11.87 C
temp_min 8.45 C
temp_max 13.54 C
feels_like 10.5 C
humidity 53 %

VLABTEST(config)#show weather location name Barcelona
name Barcelona
id 3128760
pressure 1021 bar
sunset 2021-11-17 16:30:37 UTC
sunrise 2021-11-17 06:42:22 UTC
temp 12.18 C
temp_min 8.44 C
temp_max 14.15 C
feels_like 11.52 C
humidity 79 %
```

You can also use the API to call them like any other Arista EOS command:

![API usage](https://github.com/aristaiberia/acb21/blob/main/EOS%20weather/images/API.png)
