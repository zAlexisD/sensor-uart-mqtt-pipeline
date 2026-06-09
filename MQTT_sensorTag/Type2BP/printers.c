/*
 * printers.c
 *
 *  Created on: May 19, 2026
 *      Author: alexis.doan
 */
#include "MyApp.h"
#include "UwbApi.h"

#if MQTT_FLAG

// ===== Personal print helpers for multiple elements structures =====
EXTERNC void myPrintDevInfo(phUwbDevInfo_t *devInfo){
	nLog("[CONFIG]",UWB_LOG_INFO_LEVEL,
			" Device Info: Device name: %s\n",
			devInfo->devName);
	nLog("[CONFIG]",UWB_LOG_INFO_LEVEL,
			" Device Info: UCI Generic Version: %02X.%02X\n",
			devInfo->uciGenericMajor,
			devInfo->uciGenericMinorMaintenanceVersion);
	nLog("[CONFIG]",UWB_LOG_INFO_LEVEL,
			" Device Info: NXP UCI Version: %02X.%02X.%02x\n",
			devInfo->nxpUciMajor,
			devInfo->nxpUciMinor,
			devInfo->nxpUciPatch);
	nLog("[CONFIG]",UWB_LOG_INFO_LEVEL,
			" Device Info: Firmware Version: %02X.%02X.%02X\n",
			devInfo->fwMajor,
			devInfo->fwMinor,
			devInfo->fwRc);
	nLog("[CONFIG]",UWB_LOG_INFO_LEVEL,
			" Device Info: Middle ware Version: %02X.%02X.%02X\n",
			devInfo->mwMajor,
			devInfo->mwMinor,
			devInfo->mwRc);
}

//TODO: Convert into significant data
EXTERNC void printRangingParam(phRangingParams_t *RangingParams){
	nLog("[CONFIG]",UWB_LOG_INFO_LEVEL,
			" Ranging Parameter: Device role: %s",
			convertUwbDevRole(RangingParams->deviceRole));
	nLog("[CONFIG]",UWB_LOG_INFO_LEVEL,
			" Ranging Parameter: Device Type: %s",
			convertUwbDevType(RangingParams->deviceType));
	nLog("[CONFIG]",UWB_LOG_INFO_LEVEL,
			" Ranging Parameter: Multi-node mode: %s",
			convertUwbMultiMode(RangingParams->multiNodeMode));
	// Convert byte array into plotable strings
	char MACaddr[3*sizeof(RangingParams->deviceMacAddr)];
	// Default size is set to 8, handle if its 2 bytes format
	size_t MAClen = (RangingParams->macAddrMode == 0) ?
			2 : sizeof(RangingParams->deviceMacAddr);
	formatMAC(RangingParams->deviceMacAddr,MAClen,MACaddr,sizeof(MACaddr),':');
	nLog("[CONFIG]",UWB_LOG_INFO_LEVEL,
			" Ranging Parameter: Device MAC addr: %s",MACaddr);
	nLog("[CONFIG]",UWB_LOG_INFO_LEVEL,
			" Ranging Parameter: MAC addr mode: %s",
			convertUwbMacMode(RangingParams->macAddrMode));
}
// ===== End print helpers =====

#endif // MQTT_FLAG
