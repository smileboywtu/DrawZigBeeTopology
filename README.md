Draw ZigBee Topology
====================

use python3 and graphviz to draw zigbee topology, here the topology information is read from a serial connect to zigbee coordinator, and plugin into the computer with a default port "COM3", you may change this port as you need.

Topology Information Frame
==========================

every relation in the network just send four bytes to this program:

| self address | parent address |
|:------------:|:---------------|
| LSB  -  MSB  |  LSB  -   MSB  |

this program just get the real short address in the network and draw the relation ship using the graphviz.

Dependency
==========

* python 3.4+
* pyserial
* graphviz(with python module and system module installed)


Work Flow
=========
![Alt text](http://g.gravizo.com/g?
digraph workflow {
	"uart" -> "view"
	"uart" -> "control"
	"control" -> "view"[label="queue"]
	{rank=same; "view", "control":}
}) 

Demon
=====
![Alt text](http://g.gravizo.com/g?
digraph topology {
	"0x00" [label=Coord]
		"0xbae5" -> "0x00"
		"0xd996" -> "0x00"
}) 

Contact
=======

email: 294101042@qq.com

