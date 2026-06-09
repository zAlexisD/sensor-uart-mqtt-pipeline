/*
#include <MyApp.h>
 * app_controlee.c
 *
 *  Created on: Mar 17, 2026
 *      Author: alexis.doan
 */
#include "UWBIOT_APP_BUILD.h"
#include "uwb_types.h"
#include "phNxpLogApis_App.h"
#include "MyApp.h"
#include "phOsalUwb.h"
#include "UwbApi.h"

// Ensure to take in count only if the right mode is activated
#if CUSTOM_FLAG_CONTROLEE

// Constants definition
const uint8_t ALERT[] = {0x41, 0x4c, 0x45, 0x52, 0x54};	//ALERT in hexadecimal
const uint32_t ALERT_LEN = sizeof(ALERT);

// Test function to display custom messages in controlee's log
EXTERNC void printCustMsg(const phRangingData_t *pRangingData)
{
	if (pRangingData != NULL) {
#if UWBFTR_TWR // support only for DSTWR
	if (pRangingData->ranging_measure_type == MEASUREMENT_TYPE_TWOWAY) {
		for (uint8_t i = 0; i < pRangingData->no_of_measurements; i++) {
			if(pRangingData->ranging_meas.range_meas_twr[i].distance <= 30){
				NXPLOG_APP_I("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA");
			} if(pRangingData->ranging_meas.range_meas_twr[i].distance > 60){
				NXPLOG_APP_I("OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO");
			} if((pRangingData->ranging_meas.range_meas_twr[i].distance <= 60) && (pRangingData->ranging_meas.range_meas_twr[i].distance > 30)){
				NXPLOG_APP_I("IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII");
			}
		}
	}
#endif //UWBFTR_TWR
	} else {
		NXPLOG_APP_D("pRangingData is NULL");
	}
}

// Function to generate custom send data
EXTERNC void genSendData(uint8_t *gData,uint32_t maxDataSize){

	if(ALERT_LEN <= maxDataSize){
		for (uint16_t i = 0; i < ALERT_LEN; i++) {
			gData[i] = ALERT[i];
		}
	} else {
		// WIP : Might need to handle fragmentation ???
		NXPLOG_APP_E("Custom message is too big");
	}
}

// Function to send data in alert case
EXTERNC tUWBAPI_STATUS sendAlert(
		phUwbDataPkt_t sendData,
		uint32_t sessionHandle,
		const uint8_t *gkDstMacAddr,
		uint32_t dwSize,
		phUwbQueryDataSize_t queryDataSz,
		uint8_t *gData){

	tUWBAPI_STATUS status;

	// Generate send data
	genSendData(gData,queryDataSz.dataSize);

	// Sending settings
    sendData.sessionHandle = sessionHandle;
    phOsalUwb_MemCopy(&sendData.mac_address, &gkDstMacAddr, dwSize);
    sendData.sequence_number = 0;
    sendData.data_size       = ALERT_LEN;
    sendData.data            = gData;
    status                   = UwbApi_SendData(&sendData);

    return status;
}


#endif //CUTOM_FLAG_CONTROLEE
