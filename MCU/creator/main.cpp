/*
 * Copyright 2016 <Admobilize>
 * MATRIX Labs  [http://creator.matrix.one]
 * This file is part of MATRIX Creator firmware for MCU
 * Author: Andrés Calderón [andres.calderon@admobilize.com]
 *
 * MATRIX Creator firmware for MCU is free software: you can redistribute
 * it and/or modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.

 * This program is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * General Public License for more details.

 * You should have received a copy of the GNU General Public License along
 * with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#include "ch.h"
#include "hal.h"
#include "board.h"
#include "wdt.h"


#include <math.h>
#include <string.h>
#include <mcuconf.h>

#include "./i2c.h"
#include "./sensors_data.h"
#include "./mpl3115a2.h"
#include "./lsm9ds1.h"
#include "./hts221.h"
#include "./veml6070.h"

#include "chprintf.h"

extern "C" {
#include "atmel_psram.h"
}

const uint32_t kFirmwareCreatorID = 0x10;
const uint32_t kFirmwareVersion = 0x171017; /* 0xYYMMDD */

/* Global objects */
creator::I2C i2c;  // TODO(andres.calderon@admobilize.com): avoid global objects

void psram_copy(uint8_t mem_offset, char *data, uint8_t len) {
  register char *psram = (char *)PSRAM_BASE_ADDRESS;

  for (int i = 0; i < len; i++) {
    psram[mem_offset + i] = data[i];
  }
}


/*
static WORKING_AREA(waEnvThread, 256);
static msg_t EnvThread(void *arg) {
  (void)arg;

  creator::MPL3115A2 mpl3115a2(&i2c);
  creator::HTS221 hts221(&i2c);
  creator::VEML6070 veml6070(&i2c);

  mpl3115a2.Begin();
  hts221.Begin();
  veml6070.Begin();

  PressureData press;
  HumidityData hum;
  UVData uv;
  MCUData mcu_info;

  mcu_info.ID = kFirmwareCreatorID;
  mcu_info.version = kFirmwareVersion;

  while (true) {
		
		palSetPad(IOPORT3, 17);
    chThdSleepMilliseconds(1);
    palClearPad(IOPORT3, 17);
		    
    hts221.GetData(hum.humidity, hum.temperature);

    press.altitude = mpl3115a2.GetAltitude();
    press.pressure = mpl3115a2.GetPressure();
    press.temperature = mpl3115a2.GetTemperature();

    uv.UV = veml6070.GetUV();

    psram_copy(mem_offset_mcu, (char *)&mcu_info, sizeof(mcu_info));
    psram_copy(mem_offset_press, (char *)&press, sizeof(press));
    psram_copy(mem_offset_humidity, (char *)&hum, sizeof(hum));
    psram_copy(mem_offset_uv, (char *)&uv, sizeof(uv));
  }
  return (0);
}*/

static WORKING_AREA(waIMUThread, 512);
static msg_t IMUThread(void *arg) {
  (void)arg;
  LSM9DS1 imu(&i2c, IMU_MODE_I2C, 0x6A, 0x1C);

  imu.begin();

 	IMUData data;

	IMUDebugData debugData;

	//Serial communication test
	char *float_pointer = (char *) &debugData;
	uint8_t len = sizeof(debugData);
	
	//Gyro offset 
	float gyrX_offset=0;
	float gyrY_offset=0;
	float gyrZ_offset=0;
	
	float pitch_acc=0;
	float roll_acc=0;
	
	float roll_an=0;
	float pitch_an=0;
	
	float samplingTime=20E-3;

	//chprintf((BaseChannel *)&SD1, "\n" );
	
	//Fix init offset
	int n=1000;
	for (int i=0;i<n;i++)
	{
		imu.readGyro();
		data.gyro_x = imu.calcGyro(imu.gx);
		data.gyro_y = imu.calcGyro(imu.gy);
		data.gyro_z = imu.calcGyro(imu.gz);
		
		gyrX_offset += data.gyro_x;
		gyrY_offset += data.gyro_y;
		gyrZ_offset += data.gyro_z;
	}
	gyrX_offset /= n;
	gyrY_offset /= n;
	gyrZ_offset /= n;
	
	
  while (true) {
    imu.readGyro();
    data.gyro_x = (imu.calcGyro(imu.gx) - gyrX_offset) * M_PI/180;
    data.gyro_y = (imu.calcGyro(imu.gy) - gyrY_offset) * M_PI/180;
    data.gyro_z = (imu.calcGyro(imu.gz) - gyrZ_offset) * M_PI/180;

    imu.readMag();
    data.mag_x = imu.calcMag(imu.mx);
    data.mag_y = imu.calcMag(imu.my);
    data.mag_z = imu.calcMag(imu.mz);

    imu.readAccel();
    data.accel_x = imu.calcAccel(imu.ax);
    data.accel_y = imu.calcAccel(imu.ay);
    data.accel_z = imu.calcAccel(imu.az);
    
    roll_acc = atan2(-1*(data.accel_x),sqrt(pow((data.accel_y),2) + pow((data.accel_z),2)))*180/M_PI;
    pitch_acc = atan2((data.accel_y),sqrt(pow((data.accel_x),2) + pow((data.accel_z),2)))*180/M_PI;
    
    pitch_an= data.pitch;
    roll_an= data.roll;
    
    data.pitch = 0.94 *(pitch_an+data.gyro_x*samplingTime) + 0.06 * pitch_acc;
    data.roll = 0.94 *(roll_an+data.gyro_y*samplingTime) + 0.06 * roll_acc;
    data.yaw = 0;    

//    data.yaw = atan2(data.mag_y, -data.mag_x) * 180.0 / M_PI;
//    data.roll = atan2(data.accel_y, data.accel_z) * 180.0 / M_PI;
//    data.pitch = atan2(-data.accel_x, sqrt(data.accel_y * data.accel_y + data.accel_z * data.accel_z)) * 180.0 / M_PI;

    psram_copy(mem_offset_imu, (char *)&data, sizeof(data));

		
		//////Send IMU data through serial communication/////////////
		//Fill debug data
//	debugData.gyro_x = data.gyro_x;
//    debugData.gyro_y = data.gyro_y;
//    debugData.gyro_z = data.gyro_z;

	debugData.accel_x = data.pitch;
	debugData.accel_y = data.roll;
	debugData.accel_z = data.yaw;
    
    debugData.gyro_x = data.gyro_x - gyrX_offset;
    debugData.gyro_y = data.gyro_y - gyrY_offset;
    debugData.gyro_z = data.gyro_z - gyrZ_offset;
    

		for ( int i=0; i<len;i++)
		{
			chprintf((BaseChannel *)&SD1, "%c",float_pointer[i]);
			//chprintf((BaseChannel *)&SD1, "\n\r" );
		} 
	  //chprintf((BaseChannel *)&SD1, "\n" );
		///////////////////////////////////////////////////////////

    chThdSleepMilliseconds(20);

    WDT_Restart( WDT ) ;
  }
  return (0);
}

static WORKING_AREA(waBlinkingThread, 64);
static msg_t BlinkingThread(void *arg) {

  (void)arg;


  while (true) {
    palSetPad(IOPORT3, 17);
    chThdSleepMilliseconds(50);
    palClearPad(IOPORT3, 17);
		chThdSleepMilliseconds(50);
		
  }
  return (0);
}

/*
 * Application entry point.
 */
int main(void) {

  halInit();
  chSysInit();
	/* Activates the serial driver 2 */ 
	sdStart(&SD1, NULL);  

  /* Configure EBI I/O for psram connection*/
  PIO_Configure(pinPsram, PIO_LISTSIZE(pinPsram));

  /* complete SMC configuration between PSRAM and SMC waveforms.*/
  BOARD_ConfigurePSRAM(SMC);

  i2c.Init();
  
  /* Creates the imu thread. */
  chThdCreateStatic(waIMUThread, sizeof(waIMUThread), HIGHPRIO, IMUThread,NULL);

  /* Creates the hum thread. */
  //chThdCreateStatic(waEnvThread, sizeof(waEnvThread), NORMALPRIO, EnvThread,NULL);

	/* Creates the blinking thread.*/
  chThdCreateStatic(waBlinkingThread, sizeof(waBlinkingThread), NORMALPRIO, BlinkingThread,NULL);
	

	
  return (0);
}
