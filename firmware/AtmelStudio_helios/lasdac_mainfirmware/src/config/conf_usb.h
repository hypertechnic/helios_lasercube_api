/**
 * \file
 *
 * \brief USB configuration file
 *
 * Copyright (c) 2011-2015 Atmel Corporation. All rights reserved.
 *
 * \asf_license_start
 *
 * \page License
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 * 1. Redistributions of source code must retain the above copyright notice,
 *    this list of conditions and the following disclaimer.
 *
 * 2. Redistributions in binary form must reproduce the above copyright notice,
 *    this list of conditions and the following disclaimer in the documentation
 *    and/or other materials provided with the distribution.
 *
 * 3. The name of Atmel may not be used to endorse or promote products derived
 *    from this software without specific prior written permission.
 *
 * 4. This software may only be redistributed and used in connection with an
 *    Atmel microcontroller product.
 *
 * THIS SOFTWARE IS PROVIDED BY ATMEL "AS IS" AND ANY EXPRESS OR IMPLIED
 * WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT ARE
 * EXPRESSLY AND SPECIFICALLY DISCLAIMED. IN NO EVENT SHALL ATMEL BE LIABLE FOR
 * ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
 * OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
 * STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
 * ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 *
 * \asf_license_stop
 *
 */
/*
 * Support and FAQ: visit <a href="http://www.atmel.com/design-support/">Atmel Support</a>
 */

#ifndef _CONF_USB_H_
#define _CONF_USB_H_

#include "compiler.h"

/**
 * USB Device Configuration
 * @{
 */

//! Device definition (mandatory)
#define  USB_DEVICE_VENDOR_ID             0x1209
#define  USB_DEVICE_PRODUCT_ID            0xE500	//PID/VID from http://pid.codes
#define  USB_DEVICE_MAJOR_VERSION         2
#define  USB_DEVICE_MINOR_VERSION         0
#define  USB_DEVICE_POWER                 150	//Max consumption on VBUS line (mA)
#define  USB_DEVICE_ATTR                  (USB_CONFIG_ATTR_BUS_POWERED)


//! USB Device string definitions (Optional)
 #define  USB_DEVICE_MANUFACTURE_NAME      "Gitle Mikkelsen"
 #define  USB_DEVICE_PRODUCT_NAME          "Helios Laser DAC"
 //#define  USB_DEVICE_SERIAL_NAME           "00001"

//sleep manager
//#define UDD_NO_SLEEP_MGR

/**
 * Device speeds support
 * Low speed not supported by this vendor class
 * @{
 */
////! To authorize the High speed
//#if (UC3A3||UC3A4)
//#define  USB_DEVICE_HS_SUPPORT
//#endif
//@}


/**
 * USB Device Callbacks definitions (Optional)
 * @{
 */
// #define  UDC_VBUS_EVENT(b_vbus_high)      user_callback_vbus_action(b_vbus_high)
// extern void user_callback_vbus_action(bool b_vbus_high);
// #define  UDC_SOF_EVENT()                  user_callback_sof_action()
// extern void user_callback_sof_action(void);
// #define  UDC_SUSPEND_EVENT()              user_callback_suspend_action()
// extern void user_callback_suspend_action(void);
// #define  UDC_RESUME_EVENT()               user_callback_resume_action()
// extern void user_callback_resume_action(void);
//! Mandatory when USB_DEVICE_ATTR authorizes remote wakeup feature
// #define  UDC_REMOTEWAKEUP_ENABLE()        user_callback_remotewakeup_enable()
// extern void user_callback_remotewakeup_enable(void);
// #define  UDC_REMOTEWAKEUP_DISABLE()       user_callback_remotewakeup_disable()
// extern void user_callback_remotewakeup_disable(void);
//! When a extra string descriptor must be supported
//! other than manufacturer, product and serial string
//#define  UDC_GET_EXTRA_STRING()	TODO this
//@}

//@}


/**
 * USB Interface Configuration
 * @{
 */

/**
 * Configuration of vendor interface
 * @{
 */
//! Interface callback definition
//#define UDI_VENDOR_ENABLE_EXT()          true
//#define UDI_VENDOR_DISABLE_EXT()
#define UDI_VENDOR_ENABLE_EXT() callback_vendor_enable()
extern int callback_vendor_enable(void);
#define UDI_VENDOR_DISABLE_EXT() callback_vendor_disable()
extern void callback_vendor_disable(void);

#define UDI_VENDOR_SETUP_OUT_RECEIVED()  false
#define UDI_VENDOR_SETUP_IN_RECEIVED()   false

#define UDC_GET_EXTRA_STRING() msft_string_handle()
extern bool msft_string_handle(void);
#define USB_DEVICE_SPECIFIC_REQUEST() usb_device_specific_request()
extern bool usb_device_specific_request(void);
/* *
 * #define  UDI_VENDOR_SETUP_OUT_RECEIVED()  my_vendor_setup_out_received()
 * extern bool my_vendor_setup_out_received(void);
 * #define  UDI_VENDOR_SETUP_IN_RECEIVED()   my_vendor_setup_in_received()
 * extern bool my_vendor_setup_in_received(void);
 */

//! endpoints size for full speed
#define  UDI_VENDOR_EPS_SIZE_INT_FS		32
#define  UDI_VENDOR_EPS_SIZE_BULK_FS	64
#define  UDI_VENDOR_EPS_SIZE_ISO_FS		1

//for high speed (not used)
#define  UDI_VENDOR_EPS_SIZE_INT_HS		32
#define  UDI_VENDOR_EPS_SIZE_BULK_HS	512
#define  UDI_VENDOR_EPS_SIZE_ISO_HS		1

#define USB_VERSION USB_V2

//@}

//@}

/**
 * USB Device Driver Configuration
 * @{
 */
//@}

//! The includes of classes and other headers must be done
//! at the end of this file to avoid compile error
#include "udi_vendor_conf.h"

#endif // _CONF_USB_H_
