/*
 * CustomApp.h
 *
 *  Created on: Mar 17, 2026
 *      Author: alexis.doan
 */

#ifndef CUSTOM_PROJECT_CUSTOMAPP_H_
#define CUSTOM_PROJECT_CUSTOMAPP_H_

#include "UWBIOT_APP_BUILD.h"
#include "phUwbTypes.h"
#include <inttypes.h>
#include "phUwb_BuildConfig.h"
#include "UwbApi_Types.h"
#include "PrintUtility_Proprietary.h"

#include "board.h"
#include "board_utility.h"
#include "phNxpUciHal_fwd.h"
#include "uart.h"
#include "uwb_logging.h"

// Define APP Build Flags here to avoid uploading UWBIOT_APP_BUILD.h
//NOTE: in every file containing something of the form
/*
 * #ifndef UWBIOT_APP_BUILD__MQTT_CONTROLEE
 * #include "UWBIOT_APP_BUILD.h"
 * #endif
 */
// Replace "UWBIOT_APP_BUILD.h" by "MyApp.h"
// And remove the lines
/*
 * #ifdef UWBIOT_APP_BUILD__MQTT_CONTROLEE
 * #include "MyApp.h"
 */

#pragma once

/* Options for selection of the demos : START */
/* Uncomment **ONE**, and comment out **rest** of them. */

#define UWBIOT_APP_BUILD__MQTT_CONTROLEE
// #define UWBIOT_APP_BUILD__CUSTOM_RANGING_CONTROLLER
// #define UWBIOT_APP_BUILD__CUSTOM_RANGING_CONTROLEE
// #define UWBIOT_APP_BUILD__BLE_PERIPHERAL_CONTROLLER
// #define UWBIOT_APP_BUILD__BLE_CENTRAL_CONTROLEE

//////////////////////////////////////////////////////////////////////////////////////////////////////////////
#if defined(UWBIOT_APP_BUILD__CUSTOM_RANGING_CONTROLLER)|| defined(UWBIOT_APP_BUILD__CUSTOM_RANGING_CONTROLEE)

// Enable custom actions if this flag exists
#if defined(UWBIOT_APP_BUILD__CUSTOM_RANGING_CONTROLLER)
#define CUSTOM_FLAG_CONTROLLER 1
#endif

#if defined(UWBIOT_APP_BUILD__CUSTOM_RANGING_CONTROLEE)
#define CUSTOM_FLAG_CONTROLEE 1
#endif

// Constants declaration
extern const uint8_t ALERT[];
extern const uint32_t ALERT_LEN;


// Helpers
EXTERNC void printCustMsg(const phRangingData_t *pRangingData);
EXTERNC void genSendData(uint8_t *gData,uint32_t maxDataSize);
EXTERNC tUWBAPI_STATUS sendAlert(
		phUwbDataPkt_t sendData,
		uint32_t sessionHandle,
		const uint8_t *gkDstMacAddr,
		uint32_t dwSize,
		phUwbQueryDataSize_t queryDataSz,
		uint8_t *gData);

#endif //defined(UWBIOT_APP_BUILD__CUSTOM_RANGING_CONTROLLER)|| defined(UWBIOT_APP_BUILD__CUSTOM_RANGING_CONTROLEE)

// ================================================================================================================

#if defined(UWBIOT_APP_BUILD__MQTT_CONTROLEE)

#define MQTT_FLAG 1

// Helpers
EXTERNC const char* convertUwbStatus(tUWBAPI_STATUS status);
EXTERNC const char* convertHbci(phHbci_Status_t status);
EXTERNC const char* convertUART(hal_uart_status_t status);
EXTERNC const char* convertUwbDevRole(uint8_t deviceRole);
EXTERNC const char* convertUwbMultiMode(uint8_t nodeMode);
EXTERNC const char* convertUwbMacMode(uint8_t MacMode);
EXTERNC const char* convertUwbDevType(uint8_t deviceType);
EXTERNC const char* convertUwbSessionState(uint8_t sessionState);

EXTERNC void myPrintDevInfo(phUwbDevInfo_t *devInfo);
EXTERNC void printRangingParam(phRangingParams_t *RangingParams);

EXTERNC void formatMAC(const uint8_t *mac,size_t len,char *out,
		size_t outSize,char sep);

EXTERNC void getConfig(uint32_t sessionHandle);
EXTERNC void getStatus(void);
EXTERNC void getInfo(void);
EXTERNC void MQTT_TASK(void *arg);

#endif //UWBIOT_APP_BUILD__MQTT_CONTROLEE

#endif /* CUSTOMAPP_H_ */
