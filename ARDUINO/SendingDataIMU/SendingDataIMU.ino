#include <SoftwareSerial.h>
#include "I2Cdev.h"
#include "MPU6050.h"
#if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
    #include "Wire.h"
#endif
#define OUTPUT_READABLE_ACCELGYRO


SoftwareSerial mySerial(10, 11); // RX, TX

struct IMU_data 
{
  float accx;
  float accy;
  float accz;
  float gyrx;
  float gyry;
  float gyrz;
} ;

//float exampleFloat=12.141422;
float exampleFloat=6.2828;
float data=0.0;
float data2=0.0;
int n=0;

int16_t ax, ay, az;
int16_t gx, gy, gz;
float axf, ayf, azf;
float gxf, gyf, gzf;
//sensitivity acceleration = 16384
//sensitivity gyroscope = 131
int SENS_ACCEL;
int SENS_GYRO;
int OFFSET_ACCELX;
int OFFSET_ACCELY;
int OFFSET_ACCELZ;
int OFFSET_GYROX;
int OFFSET_GYROY;
int OFFSET_GYROZ;


IMU_data imu_data;
MPU6050 accelgyro;

void setup() 
{
  // join I2C bus (I2Cdev library doesn't do this automatically)
  #if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
    Wire.begin();
  #elif I2CDEV_IMPLEMENTATION == I2CDEV_BUILTIN_FASTWIRE
    Fastwire::setup(400, true);
  #endif
  
  // Open serial communications and wait for port to open:
  Serial.begin(57600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  //sensitivity values programmed
  SENS_ACCEL=16384;
  SENS_GYRO=131;
  OFFSET_ACCELX=-470;
  OFFSET_ACCELY=-1063;
  OFFSET_ACCELZ=1573;
  OFFSET_GYROX=75;
  OFFSET_GYROY=36;
  OFFSET_GYROZ=71;
  
  // set the data rate for the SoftwareSerial port
  mySerial.begin(57600);

  // initialize device
  accelgyro.initialize();
}

void loop() 
{
    accelgyro.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);

    //required value=raw value / sensitivity
    axf=(float(ax)-OFFSET_ACCELX)/SENS_ACCEL;
    ayf=(float(ay)-OFFSET_ACCELY)/SENS_ACCEL;
    azf=(float(az)-OFFSET_ACCELZ)/SENS_ACCEL;
    
    gxf=(float(gx)-OFFSET_GYROX)/SENS_GYRO;
    gyf=(float(gy)-OFFSET_GYROY)/SENS_GYRO;
    gzf=(float(gz)-OFFSET_GYROZ)/SENS_GYRO;
     
    imu_data.accx = axf;
    imu_data.accy = ayf;
    imu_data.accz = azf;

    imu_data.gyrx = gxf;
    imu_data.gyry = gyf;
    imu_data.gyrz = gzf;
    
    /*
    imu_data.accx = 2*sin(8*3.1416*n/200)+1;
    imu_data.accy = 2*sin(4*3.1416*n/200) + exampleFloat;
    imu_data.accz = exampleFloat+4*sin(2*3.1416*n/200);

    imu_data.gyrx = 2*sin(8*3.1416*n/200)+1.6;
    imu_data.gyry = 2*sin(4*3.1416*n/200)+2;
    imu_data.gyrz = exampleFloat+4*sin(2*3.1416*n/200);
    */

    char *c_data = ( char* ) &imu_data;
    for( char c_Index = 0 ; c_Index < sizeof( IMU_data ) ; mySerial.write( c_data[ c_Index++ ] ) );
    for( char c_Index = 0 ; c_Index < sizeof( IMU_data ) ;Serial.print(c_data[ c_Index++ ] ) );
    
    n++;
  
   delay(30);
   
}
