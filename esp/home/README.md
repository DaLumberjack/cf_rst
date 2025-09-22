# CommuniFarm ESPHome Device Setup

This directory contains the ESPHome configuration for CommuniFarm devices that can be auto-discovered by Home Assistant.

## Features

- 🌐 **Auto-discovery**: Devices automatically appear in Home Assistant
- 📱 **Captive Portal**: Easy WiFi setup through web interface
- 🔧 **Configurable**: Choose which sensors and switches to enable
- 🌱 **Smart Farming**: Support for DHT22, BME280, water flow, air quality sensors
- 💧 **Irrigation Control**: Water pump and flow monitoring
- 🌡️ **Environmental Control**: Temperature, humidity, and air quality monitoring

## Quick Start

### 1. Prerequisites

- ESP32 development board
- ESPHome installed (`pip install esphome`)
- Home Assistant running on your network

### 2. Initial Setup

1. **Clone and navigate to the setup directory:**
   ```bash
   cd esp/home
   ```

2. **Run the setup generator:**
   ```bash
   python setup_generator.py
   ```

3. **Follow the interactive menu to select sensors and switches:**
   - Choose which sensors to enable (DHT22, BME280, water flow, air quality)
   - Choose which switches to enable (water pump, fan, grow light, heater)
   - Generate the configuration

### 3. Configure Secrets

1. **Copy the secrets template:**
   ```bash
   cp secrets.yaml secrets_local.yaml
   ```

2. **Edit `secrets_local.yaml` with your actual values:**
   ```yaml
   wifi_ssid: "YourWiFiNetwork"
   wifi_password: "YourWiFiPassword"
   api_encryption_key: "your-32-character-base64-key"
   ota_password: "your-ota-password"
   ```

3. **Generate an API encryption key:**
   ```bash
   openssl rand -base64 32
   ```

### 4. Flash the Device

1. **Connect your ESP32 via USB**

2. **Flash the device:**
   ```bash
   esphome run main.yaml
   ```

3. **On first boot:**
   - The device will create a WiFi hotspot named "CommuniFarm Setup"
   - Connect to this network (password: setup123456)
   - Open a web browser and go to `http://192.168.4.1`
   - Enter your WiFi credentials
   - The device will restart and connect to your network

### 5. Add to Home Assistant

1. **Open Home Assistant**
2. **Go to Settings > Devices & Services**
3. **Click "Add Integration"**
4. **Search for "ESPHome"**
5. **Enter the device IP address or let it auto-discover**
6. **Enter the API encryption key when prompted**
7. **The device will appear in your devices list**

## Available Sensors

### DHT22 Temperature & Humidity
- **Pin**: GPIO4
- **Features**: Temperature and humidity monitoring
- **Update Interval**: 30 seconds

### BME280 Environmental Sensor
- **I2C Address**: 0x76
- **Features**: Temperature, humidity, and pressure
- **Pins**: SDA=GPIO21, SCL=GPIO22
- **Update Interval**: 30 seconds

### Water Flow Sensor
- **Pin**: GPIO5
- **Features**: Pulse counter for water flow measurement
- **Unit**: L/min
- **Update Interval**: 10 seconds

### Air Quality Sensor (MQ135)
- **Pin**: GPIO34
- **Features**: Air quality and gas detection
- **Unit**: ppm
- **Update Interval**: 30 seconds

## Available Switches

### Water Pump
- **Pin**: GPIO2
- **Features**: Control water pump for irrigation
- **Restore Mode**: Always OFF

### Fan
- **Pin**: GPIO3
- **Features**: Control ventilation fan
- **Restore Mode**: Always OFF

### Grow Light
- **Pin**: GPIO4
- **Features**: Control LED grow lights
- **Restore Mode**: Always OFF

### Heater
- **Pin**: GPIO5
- **Features**: Control heating element
- **Restore Mode**: Always OFF

## Configuration Files

- `main.yaml` - Generated ESPHome configuration
- `setup_config.yaml` - Available sensors and switches configuration
- `setup_generator.py` - Interactive setup script
- `secrets.yaml` - Template for secrets (copy to secrets_local.yaml)
- `README.md` - This documentation

## Troubleshooting

### Device Not Appearing in Home Assistant
1. Check that the device is connected to WiFi
2. Verify the API encryption key is correct
3. Ensure Home Assistant and the device are on the same network
4. Check the ESPHome logs for errors

### WiFi Connection Issues
1. Reset the device to enter setup mode
2. Connect to "CommuniFarm Setup" network
3. Use the web interface to reconfigure WiFi
4. Check WiFi credentials are correct

### Sensor Reading Issues
1. Verify sensor connections
2. Check GPIO pin assignments
3. Review sensor-specific documentation
4. Check power supply to sensors

## Advanced Configuration

### Custom Pin Assignments
Edit `setup_config.yaml` to change GPIO pin assignments:

```yaml
gpio_pins:
  dht_pin: "GPIO4"
  flow_pin: "GPIO5"
  air_quality_pin: "GPIO34"
  i2c_sda: "GPIO21"
  i2c_scl: "GPIO22"
```

### Adding New Sensors
1. Add sensor definition to `setup_config.yaml`
2. Update `setup_generator.py` to handle the new sensor
3. Regenerate the configuration

### MQTT Integration
The configuration includes optional MQTT support. To enable:
1. Set up an MQTT broker
2. Add MQTT credentials to `secrets_local.yaml`
3. Uncomment MQTT configuration in the generated `main.yaml`

## Support

For issues and questions:
- Check the ESPHome documentation
- Review Home Assistant ESPHome integration docs
- Open an issue in the project repository
