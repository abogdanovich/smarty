/*
$Id: ow_example_slave.h,v 1.1 2011/12/20 01:39:43 alfille Exp $
    OWFS -- One-Wire filesystem
    OWHTTPD -- One-Wire Web Server
    Written 2003 Paul H Alfille
	email: palfille@earthlink.net
	Released under the GPL
	See the header file: ow.h for full attribution
	1wire/iButton system from Dallas Semiconductor
*/

#ifndef OW_EXAMPLE_SLAVE_H
#define OW_EXAMPLE_SLAVE_H

#ifndef OWFS_CONFIG_H
#error Please make sure owfs_config.h is included *before* this header file
#endif
#include "ow_standard.h"

/* ------- Structures ----------- */

DeviceHeader(Example_slave);

#endif  /* OW_EXAMPLE_SLAVE_H */