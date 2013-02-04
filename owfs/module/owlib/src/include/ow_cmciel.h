/*
$Id: ow_cmciel.h,v 1.4 2012/12/01 14:44:10 alfille Exp $
    OWFS -- One-Wire filesystem
    OWHTTPD -- One-Wire Web Server
    Written 2003 Paul H Alfille
	email: palfille@earthlink.net
	Released under the GPL
	See the header file: ow.h for full attribution
	1wire/iButton system from Dallas Semiconductor
*/

#ifndef OW_CMCIEL_H
#define OW_CMCIEL_H

#ifndef OWFS_CONFIG_H
#error Please make sure owfs_config.h is included *before* this header file
#endif
#include "ow_standard.h"

/* ------- Structures ----------- */

DeviceHeader(mTS017);
DeviceHeader(mCM001);
DeviceHeader(mAM001);
DeviceHeader(mRS001);

#endif /* OW_CMCIEL_H */