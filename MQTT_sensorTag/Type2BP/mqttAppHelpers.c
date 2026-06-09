/*
 * mqttHelpers.c
 *
 *  Created on: May 18, 2026
 *      Author: alexis.doan
 */
#include "UWBIOT_APP_BUILD.h"
#include "MyApp.h"

#include "uwb_types.h"
#include "phNxpLogApis_App.h"

#include "phOsalUwb.h"
#include "UwbApi.h"

#include "fsl_ctimer.h"
#include "fsl_clock.h"

#if MQTT_FLAG

//TODO: Should we handle the cases where functions does not return success?
// Or do we just ignore

// Convert byte stream in plotable object for nLog
EXTERNC void formatMAC(const uint8_t *mac,size_t len,char *out,
		size_t outSize,char sep){
	size_t pos = 0;
	for (size_t i = 0; i < len; i++) {
		int written = snprintf(out+pos,
				outSize-pos,
				"%02X%c",
                mac[i],
                (i < len-1) ? sep : '\0');
		if (written < 0 || (size_t)written >= outSize-pos) {
			// Output truncated or error
			break;
		}
		pos += written;
	}
}


// =============== Grouping same prefix data ===============
// Function grouping configurations data
EXTERNC void getConfig(uint32_t sessionHandle){
	// Pointers initialization
	phUwbDevInfo_t devInfo;
	phRangingParams_t RangingParams = {0};
	uint8_t sessionState;
	uint8_t DeviceState;
	// UWB Device Info
	if (UwbApi_GetDeviceInfo(&devInfo)==UWBAPI_STATUS_OK){
		myPrintDevInfo(&devInfo);
	}
	// UWB Ranging Parameters
	if (UwbApi_GetRangingParams(sessionHandle,&RangingParams)==UWBAPI_STATUS_OK){
		printRangingParam(&RangingParams);
	}
	if (UwbApi_GetSessionState(sessionHandle,&sessionState)==UWBAPI_STATUS_OK){
		nLog("[STATUS]",UWB_LOG_INFO_LEVEL," UWB Session state: %s",
				convertUwbSessionState(sessionState));
	}
	// UWB Device State
	if (UwbApi_GetUwbDevState(&DeviceState)==UWBAPI_STATUS_OK){
		//TODO: might need to convert into significant status name
		nLog("[STATUS]",UWB_LOG_INFO_LEVEL," Device State: %lu",DeviceState);
	}
}

// Function grouping status data
EXTERNC void getStatus(void){
	// Pointers initialization

	// HBCI status
	const char* phHbci_status = convertHbci(phHbci_GetStatus());
	nLog("[STATUS]",UWB_LOG_INFO_LEVEL," phHbci: %s",phHbci_status);
}

// Function grouping other measures
EXTERNC void getInfo(void){
	// Get timer timestamp
	uint32_t timestamp = CTIMER_GetTimerCountValue(CTIMER0);
	nLog("[INFO]",UWB_LOG_INFO_LEVEL," Timestamp: %"PRIu32"",timestamp);
	// ADC Temperature
	int32_t temp_int = BOARD_GetTemperature();
	nLog("[INFO]",UWB_LOG_INFO_LEVEL," ADC Temperature: %"PRId32"°C",temp_int);
	// Battery level
	uint8_t bat_lvl = BOARD_GetBatteryLevel();
	nLog("[INFO]",UWB_LOG_INFO_LEVEL," Battery Level: %lu",bat_lvl);

}
// =============== End grouping helpers ===============

// Helper to run MQTT Task
EXTERNC void MQTT_TASK(void *arg){
	ctimer_config_t timerConfig;
	CTIMER_GetDefaultConfig(&timerConfig);
	CTIMER_Init(CTIMER0, &timerConfig);
	CTIMER_StartTimer(CTIMER0);
	while(1){
		getInfo();
		getStatus();
		vTaskDelay(pdMS_TO_TICKS(1000)); // every 1 second
	}
}

#endif //MQTT_FLAG
