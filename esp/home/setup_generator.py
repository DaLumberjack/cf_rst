#!/usr/bin/env python3
"""
CommuniFarm ESPHome Configuration Generator
This script generates ESPHome YAML configuration based on user selections
"""

import yaml
import os
import sys
from pathlib import Path

class CommuniFarmSetupGenerator:
    def __init__(self, config_file="setup_config.yaml"):
        self.config_file = config_file
        self.config = self.load_config()
        
    def load_config(self):
        """Load the setup configuration file"""
        try:
            with open(self.config_file, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            print(f"Error: {self.config_file} not found!")
            sys.exit(1)
        except yaml.YAMLError as e:
            print(f"Error parsing {self.config_file}: {e}")
            sys.exit(1)
    
    def display_menu(self):
        """Display the setup menu"""
        print("\n" + "="*60)
        print("🌱 CommuniFarm ESPHome Device Setup")
        print("="*60)
        print("\nSelect sensors to enable:")
        print("-" * 30)
        
        for i, (sensor_id, sensor) in enumerate(self.config['sensors'].items(), 1):
            status = "✓" if sensor['enabled'] else " "
            print(f"{i}. [{status}] {sensor['name']}")
            print(f"   {sensor['description']}")
            print()
        
        print("Select switches to enable:")
        print("-" * 30)
        
        for i, (switch_id, switch) in enumerate(self.config['switches'].items(), 1):
            status = "✓" if switch['enabled'] else " "
            print(f"{i+len(self.config['sensors'])}. [{status}] {switch['name']}")
            print(f"   {switch['description']}")
            print()
    
    def get_user_selections(self):
        """Get user selections for sensors and switches"""
        print("\nEnter the numbers of items you want to enable (comma-separated):")
        print("Example: 1,3,5,7")
        print("Press Enter to keep current selections, 'q' to quit")
        
        while True:
            try:
                user_input = input("\nYour selection: ").strip()
                
                if user_input.lower() == 'q':
                    print("Exiting...")
                    sys.exit(0)
                
                if not user_input:
                    # Keep current selections
                    break
                
                # Parse selections
                selections = [int(x.strip()) for x in user_input.split(',')]
                
                # Reset all to disabled first
                for sensor in self.config['sensors'].values():
                    sensor['enabled'] = False
                for switch in self.config['switches'].values():
                    switch['enabled'] = False
                
                # Enable selected items
                total_sensors = len(self.config['sensors'])
                for selection in selections:
                    if 1 <= selection <= total_sensors:
                        sensor_id = list(self.config['sensors'].keys())[selection - 1]
                        self.config['sensors'][sensor_id]['enabled'] = True
                    elif total_sensors < selection <= total_sensors + len(self.config['switches']):
                        switch_id = list(self.config['switches'].keys())[selection - total_sensors - 1]
                        self.config['switches'][switch_id]['enabled'] = True
                    else:
                        print(f"Invalid selection: {selection}")
                        continue
                
                break
                
            except ValueError:
                print("Invalid input. Please enter numbers separated by commas.")
            except KeyboardInterrupt:
                print("\nExiting...")
                sys.exit(0)
    
    def generate_esphome_config(self):
        """Generate the ESPHome YAML configuration"""
        config = self.config
        
        yaml_content = f"""esphome:
  name: {config['device_info']['name']}
  friendly_name: {config['device_info']['friendly_name']}
  platform: {config['device_info']['platform']}
  board: {config['device_info']['board']}
  framework:
    type: arduino

# Enable logging
logger:
  level: INFO

# Enable Home Assistant API for auto-discovery
api:
  encryption:
    key: !secret api_encryption_key

# Enable OTA updates
ota:
  password: !secret ota_password

# WiFi configuration with captive portal for setup
wifi:
  ssid: !secret wifi_ssid
  password: !secret wifi_password
  
  # Enable captive portal for initial setup
  ap:
    ssid: "{config['network']['captive_portal']['ssid']}"
    password: "{config['network']['captive_portal']['password']}"

# Enable web server for configuration
web_server:
  port: 80
  include_internal: true

# Enable captive portal for WiFi setup
captive_portal:

# Enable MDNS for easy discovery
mdns:
  services:"""

        # Add MDNS services
        for service in config['network']['mdns_services']:
            yaml_content += f"""
    - service: {service['service']}
      protocol: {service['protocol']}
      port: {service['port']}"""

        yaml_content += """

# Text sensor for device status
text_sensor:
  - platform: template
    name: "Device Status"
    id: device_status
    update_interval: 30s
    lambda: |-
      return "Online - " + id(wifi).get_ssid().c_str();

# Binary sensor for WiFi connection status
binary_sensor:
  - platform: status
    name: "WiFi Status"
    id: wifi_status

# Sensors
sensor:"""

        # Add enabled sensors
        for sensor_id, sensor in config['sensors'].items():
            if sensor['enabled']:
                if sensor_id == 'dht22':
                    yaml_content += f"""
  # DHT22 Temperature and Humidity
  - platform: dht
    pin: {sensor['pin']}
    temperature:
      name: "Temperature"
      id: temperature
      unit_of_measurement: "°C"
      accuracy_decimals: 1
    humidity:
      name: "Humidity"
      id: humidity
      unit_of_measurement: "%"
      accuracy_decimals: 1
    update_interval: {sensor['update_interval']}
    id: dht_sensor"""
                
                elif sensor_id == 'bme280':
                    yaml_content += f"""
  # BME280 Environmental Sensor
  - platform: bme280
    address: {sensor['address']}
    i2c_id: {sensor['i2c_bus']}
    temperature:
      name: "BME280 Temperature"
      id: bme280_temperature
      unit_of_measurement: "°C"
      accuracy_decimals: 1
    pressure:
      name: "BME280 Pressure"
      id: bme280_pressure
      unit_of_measurement: "hPa"
      accuracy_decimals: 1
    humidity:
      name: "BME280 Humidity"
      id: bme280_humidity
      unit_of_measurement: "%"
      accuracy_decimals: 1
    update_interval: {sensor['update_interval']}
    id: bme280_sensor"""
                
                elif sensor_id == 'water_flow':
                    yaml_content += f"""
  # Water Flow Sensor
  - platform: pulse_counter
    pin: {sensor['pin']}
    name: "Water Flow"
    id: water_flow
    unit_of_measurement: "{sensor['unit_of_measurement']}"
    accuracy_decimals: 2
    filters:
      - multiply: 0.001
    update_interval: {sensor['update_interval']}"""
                
                elif sensor_id == 'air_quality':
                    yaml_content += f"""
  # Air Quality Sensor (MQ135)
  - platform: adc
    pin: {sensor['pin']}
    name: "Air Quality"
    id: air_quality
    unit_of_measurement: "{sensor['unit_of_measurement']}"
    accuracy_decimals: 0
    update_interval: {sensor['update_interval']}
    filters:
      - median:
          window_size: 5
          send_every: 5"""

        yaml_content += """

# Switches
switch:"""

        # Add enabled switches
        for switch_id, switch in config['switches'].items():
            if switch['enabled']:
                yaml_content += f"""
  # {switch['name']}
  - platform: gpio
    pin: {switch['pin']}
    name: "{switch['name']}"
    id: {switch_id}
    restore_mode: {switch['restore_mode']}"""

        # Add I2C bus if BME280 is enabled
        if any(sensor['enabled'] for sensor in config['sensors'].values() if 'i2c_bus' in sensor):
            yaml_content += f"""

# I2C Bus for BME280
i2c:
  sda: {config['gpio_pins']['i2c_sda']}
  scl: {config['gpio_pins']['i2c_scl']}
  scan: true
  id: bus_a"""

        yaml_content += f"""

# GPIO Pins for sensors
gpio:"""

        # Add GPIO pins for enabled sensors
        if config['sensors']['dht22']['enabled']:
            yaml_content += f"""
  - pin: {config['gpio_pins']['dht_pin']}
    mode: INPUT_PULLUP
    id: dht_pin"""
        
        if config['sensors']['water_flow']['enabled']:
            yaml_content += f"""
  - pin: {config['gpio_pins']['flow_pin']}
    mode: INPUT_PULLUP
    id: flow_pin"""
        
        if config['sensors']['air_quality']['enabled']:
            yaml_content += f"""
  - pin: {config['gpio_pins']['air_quality_pin']}
    mode: INPUT
    id: air_quality_pin"""

        yaml_content += """

# Time for scheduling
time:
  - platform: sntp
    id: sntp_time
    servers:
      - pool.ntp.org
      - time.nist.gov

# Interval for periodic updates
interval:
  - interval: 30s
    then:
      - lambda: |-
          // Update device status
          id(device_status).publish_state("Online - " + id(wifi).get_ssid().c_str());

# MQTT for additional communication (optional)
mqtt:
  broker: !secret mqtt_broker
  username: !secret mqtt_username
  password: !secret mqtt_password
  discovery: true
  discovery_prefix: homeassistant"""

        return yaml_content
    
    def save_config(self, filename="main.yaml"):
        """Save the generated configuration to a file"""
        yaml_content = self.generate_esphome_config()
        
        with open(filename, 'w') as file:
            file.write(yaml_content)
        
        print(f"\n✅ Configuration saved to {filename}")
        print("📝 Don't forget to:")
        print("   1. Copy secrets.yaml and fill in your WiFi credentials")
        print("   2. Generate an API encryption key")
        print("   3. Set up OTA password")
        print("   4. Flash the device with ESPHome")
    
    def run(self):
        """Run the setup generator"""
        while True:
            self.display_menu()
            self.get_user_selections()
            
            print("\n" + "="*60)
            print("Generated Configuration Preview:")
            print("="*60)
            
            # Show a preview of what will be enabled
            enabled_sensors = [name for name, sensor in self.config['sensors'].items() if sensor['enabled']]
            enabled_switches = [name for name, switch in self.config['switches'].items() if switch['enabled']]
            
            if enabled_sensors:
                print("✅ Enabled Sensors:")
                for sensor in enabled_sensors:
                    print(f"   - {self.config['sensors'][sensor]['name']}")
            
            if enabled_switches:
                print("✅ Enabled Switches:")
                for switch in enabled_switches:
                    print(f"   - {self.config['switches'][switch]['name']}")
            
            if not enabled_sensors and not enabled_switches:
                print("⚠️  No sensors or switches enabled!")
            
            print("\nOptions:")
            print("1. Generate configuration (save to main.yaml)")
            print("2. Modify selections")
            print("3. Exit")
            
            choice = input("\nYour choice (1-3): ").strip()
            
            if choice == '1':
                self.save_config()
                break
            elif choice == '2':
                continue
            elif choice == '3':
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    generator = CommuniFarmSetupGenerator()
    generator.run()
