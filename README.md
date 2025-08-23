# CommuniFarm (cf_rst)

A smart farming automation system that connects ESP32 devices running Rust firmware to Home Assistant through MQTT communication.

## 🏗️ System Architecture

CommuniFarm consists of three main components:

1. **ESP32 Rust Firmware** (`esp/`) - Runs on ESP32 devices to control sensors and actuators
2. **Home Assistant Custom Component** (`ha/custom_components/communifarm/`) - Integrates devices into Home Assistant
3. **MQTT Communication Layer** - Enables device discovery and state synchronization

## 🔌 ESP Rust Communications

### Current Implementation
The ESP firmware is currently in development with a basic structure:

- **Main Application** (`esp/src/main.rs`) - Entry point for the ESP32 application
- **Configuration Library** (`esp/cf-config/`) - Shared configuration types using Serde for serialization
- **Workspace Structure** - Organized as a Cargo workspace for modular development

### Dependencies
- `serde` - For configuration serialization/deserialization
- Rust 2021 edition

### Build & Flash Commands
```bash
# Build the ESP firmware
just cf-build

# Run the ESP firmware (for testing)
just cf-rst

# Flash to ESP32 device
just flash-esp
```

## 🏠 Home Assistant Integration

### Custom Component: communifarm

The `communifarm` custom component provides seamless integration between ESP32 devices and Home Assistant through MQTT.

#### Features
- **Automatic Device Discovery** - Devices announce themselves via MQTT discovery
- **Sensor Support** - Real-time sensor data integration
- **Switch Control** - Bidirectional control of actuators
- **MQTT-based Communication** - Reliable local communication

#### Component Structure
```
ha/custom_components/communifarm/
├── __init__.py          # Main integration setup and discovery
├── sensor.py            # Sensor entity implementation
├── switch.py            # Switch entity implementation
└── manifest.json        # Component metadata
```

#### Device Discovery
Devices publish discovery messages to `cf/discovery` topic with the following format:
```json
{
  "device_id": "unique_device_id",
  "components": [
    {
      "type": "sensor",
      "name": "Temperature Sensor",
      "state_topic": "cf/device_id/temperature",
      "unit": "°C"
    },
    {
      "type": "switch",
      "name": "Water Pump",
      "state_topic": "cf/device_id/pump/state",
      "command_topic": "cf/device_id/pump/command"
    }
  ]
}
```

#### MQTT Topics
- **Discovery**: `cf/discovery` - Device and component registration
- **Sensor States**: `cf/{device_id}/{sensor_name}` - Real-time sensor readings
- **Switch States**: `cf/{device_id}/{switch_name}/state` - Current switch status
- **Switch Commands**: `cf/{device_id}/{switch_name}/command` - Control commands (ON/OFF)

## 🚀 Development Setup

### Prerequisites
- Rust toolchain
- ESP32 development environment
- Home Assistant instance
- MQTT broker (e.g., Mosquitto)

### Quick Start
1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd cf_rst
   ```

2. **Build ESP firmware**
   ```bash
   just cf-build
   ```

3. **Start Home Assistant development container**
   ```bash
   just ha-dev
   ```

4. **Install the communifarm custom component**
   - Copy `ha/custom_components/communifarm/` to your Home Assistant `custom_components/` directory
   - Restart Home Assistant

### Development Commands
```bash
# Build ESP firmware
just cf-build

# Run ESP firmware locally
just cf-rst

# Flash to ESP32
just flash-esp

# Start Home Assistant dev container
just ha-dev
```

## 🔧 Configuration

### ESP Configuration
The ESP firmware uses the `cf-config` library for configuration management. Configuration types are defined in `esp/cf-config/src/lib.rs`.

### Home Assistant Configuration
The communifarm component automatically discovers devices via MQTT. No additional configuration is required in `configuration.yaml`.

## 📡 Communication Protocol

### Device Registration
1. ESP32 device connects to MQTT broker
2. Device publishes discovery message to `cf/discovery`
3. Home Assistant receives discovery and creates entities
4. Device begins publishing state updates

### Sensor Updates
- Sensors publish values to their respective state topics
- Home Assistant receives updates and updates entity states
- Real-time monitoring without polling

### Switch Control
- Home Assistant publishes commands to command topics
- ESP32 receives commands and controls hardware
- Device publishes state confirmation back to state topic

## 🚧 Current Status

### ✅ Implemented
- Basic ESP Rust project structure
- Home Assistant custom component framework
- MQTT-based device discovery
- Sensor and switch entity types
- Bidirectional communication protocol

### 🚧 In Development
- ESP32 hardware integration
- Sensor/actuator drivers
- Configuration management
- Error handling and logging

### 📋 Planned Features
- Multiple sensor types (temperature, humidity, soil moisture)
- Actuator control (pumps, lights, fans)
- Data logging and analytics
- Web-based configuration interface
- OTA (Over-The-Air) updates

## 🤝 Contributing

### Commit Convention
This project follows [Conventional Commits](https://www.conventionalcommits.org/) for semantic versioning. Use the following commit types:

- **feat**: New features (bumps minor version)
- **doc**: Documentation changes (bumps patch version)
- **ci**: CI/CD changes (bumps patch version)
- **bug**: Bug fixes (bumps patch version)
- **test**: Test additions/changes (bumps patch version)
- **data**: Data file changes (bumps patch version)
- **tf**: Terraform changes (bumps patch version)
- **mod**: Module changes (bumps patch version)
- **lib**: Library updates (bumps patch version)

### Commit Message Format
```
type(scope): description

[optional body]

[optional footer(s)]
```

Examples:
```
feat(esp): add temperature sensor support
doc(readme): update installation instructions
bug(mqtt): fix connection timeout issue
test(sensor): add unit tests for sensor module
```

### Development Workflow
1. Fork the repository
2. Create a feature branch
3. Implement your changes following the commit convention
4. Add tests if applicable
5. Submit a pull request

### Automated Versioning
The project uses GitHub Actions with semantic-release to automatically:
- Analyze commit messages
- Determine version bumps
- Generate changelogs
- Create GitHub releases
- Tag releases

## 📄 License

[Add your license information here]

## 🔗 Related Projects

- [Home Assistant](https://www.home-assistant.io/)
- [ESP-IDF](https://docs.espressif.com/projects/esp-idf/)
- [Rust Embedded](https://rust-embedded.github.io/)
