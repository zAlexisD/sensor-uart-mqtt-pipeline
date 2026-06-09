/*
 * MyApp.c
 *
 *  Created on: Mar 23, 2026
 *      Author: alexis.doan
 */
#include "UWBIOT_APP_BUILD.h"
#include "MyApp.h"
#include "phNxpLogApis_App.h"

// Ensure to take in count only if the right mode is activated
#if CUSTOM_FLAG

// Function to enable LEDs according to distance
EXTERNC void rangeLEDs(const phRangingData_t *pRangingData)
{
	if (pRangingData != NULL) {
#if UWBFTR_TWR // support only for DSTWR
		if (pRangingData->ranging_measure_type == MEASUREMENT_TYPE_TWOWAY) {
			for (uint8_t i = 0; i < pRangingData->no_of_measurements; i++) {
				if(pRangingData->ranging_meas.range_meas_twr[i].distance >= 60){
					// Green LED
					TurnOffLeds();
					Led2On();
				} if(pRangingData->ranging_meas.range_meas_twr[i].distance < 30){
					// Toggle red LED
					TurnOffLeds();
					Led1Toggle();
				} if((pRangingData->ranging_meas.range_meas_twr[i].distance >= 30) && (pRangingData->ranging_meas.range_meas_twr[i].distance < 60)){
					// Orange LED
					TurnOffLeds();
					Led1On();
					Led2On();
				}
			}
		}
#endif //UWBFTR_TWR
	} else {
		NXPLOG_APP_D("pRangingData is NULL");
	}
}

// Function to enable red LED if alert message received
EXTERNC void alertRcv(const phUwbRcvDataPkt_t *pRcvDataPkt)
{
    if (pRcvDataPkt != NULL) {
    	// byte array for "ALERT"
    	uint8_t condition[] = {0x41, 0x4c, 0x45, 0x52, 0x54};

        // LED logic for a determined condition
        if (memcmp(condition,pRcvDataPkt->data,sizeof(condition)) ){
        	Led1On();
        } else{
        	TurnOffLeds();
        }
    }
    else {
        NXPLOG_APP_D("pRcvDataPkt is NULL");
    }
}

#endif // CUSTOM_FLAG



