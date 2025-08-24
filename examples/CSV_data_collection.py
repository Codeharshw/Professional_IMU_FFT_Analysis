#!/usr/bin/env python3
"""
MPU9250 Data Collection Script

Collects accelerometer and gyroscope data from Arduino via serial port
and saves to CSV file with timestamps.

Requirements:
    pip install pyserial

Usage:
    python data_collection.py
    
Configure COM_PORT below for your system:
    Windows: 'COM3', 'COM4', etc.
    Linux/Mac: '/dev/ttyUSB0', '/dev/ttyACM0', etc.
"""

import serial
import csv
import time
import sys
import os

# === Configuration ===
COM_PORT = 'COM5'  # Change this to match your Arduino port
BAUD_RATE = 115200
CSV_FILE = 'calibrated_mpu9250_data.csv'
TIMEOUT = 1  # Serial timeout in seconds

def find_arduino_port():
    """
    Helper function to automatically detect Arduino port.
    You can uncomment this and modify main() to use auto-detection.
    """
    import serial.tools.list_ports
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if 'Arduino' in port.description or 'CH340' in port.description or 'USB' in port.description:
            return port.device
    return None

def validate_data_line(line):
    """Validate that the line contains 6 numeric values."""
    try:
        values = line.split(",")
        if len(values) != 6:
            return False
        # Try to convert to float to validate
        [float(val.strip()) for val in values]
        return True
    except ValueError:
        return False

def main():
    print(f"MPU9250 Data Collection")
    print(f"Output file: {CSV_FILE}")
    print(f"Attempting to connect to {COM_PORT} at {BAUD_RATE} baud...")
    
    # Check if output file already exists
    if os.path.exists(CSV_FILE):
        response = input(f"\n{CSV_FILE} already exists. Overwrite? (y/n): ")
        if response.lower() != 'y':
            print("Aborted.")
            sys.exit(1)
    
    # === Initialize Serial Connection ===
    try:
        ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=TIMEOUT)
        print(f"✓ Connected to {COM_PORT}")
    except serial.SerialException as e:
        print(f"✗ Failed to connect to {COM_PORT}: {e}")
        print("\nTry these steps:")
        print("1. Check that Arduino is connected")
        print("2. Verify the COM port in Device Manager (Windows) or ls /dev/tty* (Linux/Mac)")
        print("3. Close Arduino IDE if it's open")
        print("4. Update COM_PORT variable in this script")
        sys.exit(1)
    
    # Wait for Arduino to initialize
    print("Waiting for Arduino to initialize...")
    time.sleep(3)
    
    # === Start Data Collection ===
    start_time = time.time()
    data_count = 0
    
    try:
        with open(CSV_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            
            # Write CSV header
            writer.writerow(["timestamp", "ax", "ay", "az", "gx", "gy", "gz"])
            
            print("\n✓ Logging started. Data format: timestamp,ax,ay,az,gx,gy,gz")
            print("Press Ctrl+C to stop logging.\n")
            print("Time(s)  | Accel (ax,ay,az)        | Gyro (gx,gy,gz)")
            print("-" * 65)
            
            while True:
                try:
                    line = ser.readline().decode('utf-8').strip()
                    
                    if line and validate_data_line(line):
                        values = line.split(",")
                        timestamp = round(time.time() - start_time, 3)
                        
                        # Clean up values (remove whitespace)
                        clean_values = [val.strip() for val in values]
                        
                        # Write to CSV
                        writer.writerow([timestamp] + clean_values)
                        
                        # Print formatted output (every 10th sample to avoid spam)
                        data_count += 1
                        if data_count % 10 == 0:
                            print(f"{timestamp:6.1f}s  | "
                                  f"{clean_values[0]:>6},{clean_values[1]:>6},{clean_values[2]:>6} | "
                                  f"{clean_values[3]:>6},{clean_values[4]:>6},{clean_values[5]:>6}")
                        
                        # Flush every 50 samples to ensure data is saved
                        if data_count % 50 == 0:
                            file.flush()
                    
                    elif line and not line.startswith("ax"):  # Skip header echoes
                        # Print invalid lines for debugging
                        print(f"⚠ Invalid data: {line}")
                        
                except UnicodeDecodeError:
                    print("⚠ Unicode decode error - check baud rate")
                    continue
                except serial.SerialException as e:
                    print(f"✗ Serial error: {e}")
                    break
                    
    except KeyboardInterrupt:
        print(f"\n✓ Data logging stopped.")
        print(f"✓ Collected {data_count} data points")
        print(f"✓ Data saved to: {CSV_FILE}")
        
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("✓ Serial connection closed")

if __name__ == "__main__":
    main()
