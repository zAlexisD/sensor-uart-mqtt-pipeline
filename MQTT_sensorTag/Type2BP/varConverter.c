/*
 * varConverter.c
 *
 *  Created on: May 19, 2026
 *      Author: alexis.doan
 */
#include "MyApp.h"

//TODO: might include these helpers any time
#if MQTT_FLAG

// ========== Convert variable codes into meaningful data ==========
//TODO: hopefully didn't mess with the assigned codes
EXTERNC const char* convertUwbStatus(tUWBAPI_STATUS status){
	switch(status){
	case 0x00: return "SUCCESS";
	case 0x01: return "REJECTED";
	case 0x02: return "FAILED";
	case 0x03: return "NOT INITIALIZED";
	case 0x04: return "INVALID PARAMETERS";
	case 0x05: return "INVALID RANGE";
	case 0x11: return "SESSION DOES NOT EXIST";
	case 0x12: return "INVALID PHASE PARTICIPATION";
	case 0x13: return "SESSION ACTIVE";
	case 0x14: return "MAX SESSIONS EXCEEDED";
	case 0x15: return "SESSION NOT CONFIGURED";
	case 0x16: return "SESSIONS ONGOING";
	case 0x17: return "MULTICAST LIST FULL";
	case 0x1B: return "OK BUT NEGATIVE DISTANCE REPORTED";
	case 0x71: return "ESE RESET";
	case 0x30: return "DATA TRANSFER ERROR";
	case 0x31: return "NO CREDIT AVAILABLE";
	case 0x28: return "ERROR ROUND INDEX NOT ACTIVATED";
	case 0x29: return "ERROR NUMBER OF QCTIVE RANGING ROUNDS EXCEEDED";
	case 0x2A: return "ERROR ROUND INDEX NOT SET AS INITIATOR";
	//case 0x30: return "DLTDOA DEVICE ADDRESS NOT MATCHING IN REPLY TIMELIST";
	case 0xFA: return "BUFFER OVERFLOW";
	case 0xFB: return "PBF=1, CMD PKT SENT";
	case 0xFC: return "DEVICE WOKEN UP FRON HPD";
	case 0xFD: return "FAILED WITH TIMEOUT";
	case 0xFF: return "ESE ERROR";
	case 0x8B: return "RANGING SUSPENDED";
	case 0x0B: return "UNKNOWN";
	default: return "";
	}
}

// Also convert phHbci_Status_t
EXTERNC const char* convertHbci(phHbci_Status_t status){
	switch(status){
	case phHbci_Success: return "SUCCESS";
	case phHbci_Failure: return "FAILURE";
	default: return "";
	}
}

// And finally for UART
EXTERNC const char* convertUART(hal_uart_status_t status){
	switch(status){
	case kStatus_HAL_UartSuccess: return "Success";
	case kStatus_HAL_UartTxBusy: return "Transmitter Busy";
	case kStatus_HAL_UartRxBusy: return "Receiver Busy";
	case kStatus_HAL_UartTxIdle: return "HAL UART transmitter is idle";
	case kStatus_HAL_UartRxIdle: return "HAL UART receiver is idle";
	case kStatus_HAL_UartBaudrateNotSupport: return "Baud rate not supported in current clock source";
	case kStatus_HAL_UartProtocolError: return "Protocol error (Noise,Framing,Parity,etc)";
	case kStatus_HAL_UartError: return "HAL UART error";
	default: return "";
	}
}

EXTERNC const char* convertUwbDevRole(uint8_t deviceRole){
	switch(deviceRole){
	case 0: return "Responder";
	case 1: return "Initiator";
	case 2: return "UT Sync Anchor";
	case 3: return "UT Anchor";
	case 4: return "UT Tag";
	case 5: return "Advertiser";
	case 6: return "Observer";
	case 7: return "DlTDoA Anchor";
	case 8: return "DlTDoA Tag";
	default: return "";
	}
}

EXTERNC const char* convertUwbMultiMode(uint8_t nodeMode){
	switch(nodeMode){
	case 0x00: return "Single device to Single device (Unicast)";
	case 0x01: return "One to Many";
	case 0x02: return "Many to Many";
	case 0x03: return "Reserved";
	default: return "";
	}
}

EXTERNC const char* convertUwbMacMode(uint8_t MacMode){
	switch(MacMode){
	case 0: return "2 bytes";
	case 1: return "8 bytes MAC addr with 2 bytes in header";
	case 2: return "8 bytes in MAC addr and header";
	default: return "";
	}
}

EXTERNC const char* convertUwbDevType(uint8_t deviceType){
	switch(deviceType){
	case 0x00: return "Controlee";
	case 0x01: return "Controller";
	case 0x02: return "Advertiser";
	case 0x03: return "Observer";
	default: return "";
	}
}

EXTERNC const char* convertUwbSessionState(uint8_t sessionState){
	switch(sessionState){
	case UWBAPI_SESSION_INIT_SUCCESS: return "Session is Initialized";
	case UWBAPI_SESSION_DEINIT_SUCCESS: return "Session is De-initialized";
	case UWBAPI_SESSION_ACTIVATED: return "Session is Busy";
	case UWBAPI_SESSION_IDLE: return "Session is Idle";
	case UWBAPI_SESSION_ERROR: return "Session Not Found";
	default: return "";
	}
}


// ========== End conversion helpers ==========

#endif // MQTT_FLAG

