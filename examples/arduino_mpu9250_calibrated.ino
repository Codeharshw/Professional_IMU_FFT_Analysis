// Arduino Code for Acceleroeter_and_gyroscope_readings_CSVFile_Calibrated
/*
 * Basic MPU9250 data collection example
 * Based on common Arduino IMU reading patterns
 */
#include <Wire.h>
#include <MPU9250_asukiaaa.h>

MPU9250_asukiaaa mpu;

bool printedHeader = false;
bool calibrated = false;

float ax_offset = 0, ay_offset = 0, az_offset = 0;
float gx_offset = 0, gy_offset = 0, gz_offset = 0;

void setup() {
  Serial.begin(115200);
  Wire.begin();
  mpu.setWire(&Wire);
  mpu.beginAccel();
  mpu.beginGyro();
  delay(2000); // Wait for sensor to stabilize

  // === AUTO CALIBRATION ===
  int samples = 200;
  float ax_sum = 0, ay_sum = 0, az_sum = 0;
  float gx_sum = 0, gy_sum = 0, gz_sum = 0;

  for (int i = 0; i < samples; i++) {
    mpu.accelUpdate();
    mpu.gyroUpdate();

    ax_sum += mpu.accelX();
    ay_sum += mpu.accelY();
    az_sum += mpu.accelZ(); // includes gravity (~1g when still)

    gx_sum += mpu.gyroX();
    gy_sum += mpu.gyroY();
    gz_sum += mpu.gyroZ();

    delay(10); // sampling delay
  }

  // Calculate average offset
  ax_offset = ax_sum / samples;
  ay_offset = ay_sum / samples;
  az_offset = (az_sum / samples) - 1.0;  // Remove gravity too → makes az ~ 0 when still

  gx_offset = gx_sum / samples;
  gy_offset = gy_sum / samples;
  gz_offset = gz_sum / samples;

  calibrated = true;
}

void loop() {
  if (!calibrated) return;

  mpu.accelUpdate();
  mpu.gyroUpdate();

  // Apply offset correction
  float ax = mpu.accelX() - ax_offset;
  float ay = mpu.accelY() - ay_offset;
  float az = mpu.accelZ() - az_offset;

  float gx = mpu.gyroX() - gx_offset;
  float gy = mpu.gyroY() - gy_offset;
  float gz = mpu.gyroZ() - gz_offset;

  // Print CSV header once
  if (!printedHeader) {
    Serial.println("ax,ay,az,gx,gy,gz");
    printedHeader = true;
  }

  // Print calibrated data
  Serial.print(ax); Serial.print(",");
  Serial.print(ay); Serial.print(",");
  Serial.print(az); Serial.print(",");

  Serial.print(gx); Serial.print(",");
  Serial.print(gy); Serial.print(",");
  Serial.println(gz);

  delay(100); // ~10Hz
}
