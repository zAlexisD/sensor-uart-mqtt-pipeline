/*
 * MyApp.h
 *
 *  Created on: Mar 23, 2026
 *      Author: alexis.doan
 */

#ifndef MYAPP_H_
#define MYAPP_H_

#include "UWBIOT_APP_BUILD.h"
#include "UwbApi_Types.h"
#include "LED.h"

// Define APP Build Flags here to avoid uploading UWBIOT_APP_BUILD.h
//NOTE: in every file containing something of the form
/*
 * #ifndef UWBIOT_APP_BUILD__CUSTOM_STANDALONE
 * #include "UWBIOT_APP_BUILD.h"
 * #endif
 */
// Replace "UWBIOT_APP_BUILD.h" by "MyApp.h"
// And remove the lines
/*
 * #ifdef UWBIOT_APP_BUILD__CUSTOM_STANDALONE
 * #include "MyApp.h"
 */

#pragma once

/* Options for selection of the demos : START */
#define UWBIOT_APP_BUILD__CUSTOM_STANDALONE

#if defined(UWBIOT_APP_BUILD__CUSTOM_STANDALONE)

// Config defines
#define RANGING_APP_SESSION_ID 0x11223344
#define RANGING_APP_MULTI_NODE_MODE_MANY 1
#define RANGING_APP_NO_OF_ANCHORS_P2P 1

// Flag that enables custom functions to avoid conflicts
#define CUSTOM_FLAG 1

// Prototypes
EXTERNC void rangeLEDs(const phRangingData_t *pRangingData);
EXTERNC void alertRcv(const phUwbRcvDataPkt_t *pRcvDataPkt);

#endif // defined

#endif /* MYAPP_H_ */
