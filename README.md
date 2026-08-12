# EOSAS - Embedded Optical Skin Analysis System

EOSAS is a prototype embedded system developed to explore the integration of computer vision, machine learning, and embedded hardware. The system captures images using an ESP32-CAM, processes them through a Python-based machine learning pipeline, and generates a hazard score through a custom dashboard interface.

## Overview

EOSAS captures skin images using an ESP32-CAM, processes them through a machine learning pipeline, and displays results through a custom Flask dashboard. A Particle Argon controls the user interface, including scan lighting, button controls, and hazard indication LEDs.

![EOSAS Architecture](images/EOSAS_Architecture.png)
*Figure 1. High-level EOSAS system architecture showing embedded hardware, communication, machine learning pipeline, and dashboard outputs.*

## 🎥 Demo Video

A demonstration of the current EOSAS prototype can be found in the `demo` folder:

➡️ **eosas_demo.mov**

If GitHub does not preview the video directly, download the file to view the full demonstration.

## Prototype Status

Current Features

- ESP32-CAM image capture
- Hazard scoring pipeline
- Dashboard interface
- LED status indicators
- Embedded control system

In Progress

- PCB fabrication and hardware validation
- Optical sensor integration and calibration
- Custom enclosure
- Improved model performance

## Custom PCB

EOSAS PCB v1.0 is a custom dual-MCU carrier board designed to replace the breadboard wiring used in the original prototype and consolidate the system electronics onto a dedicated PCB.

The board integrates:
- Particle Argon and ESP32-CAM
- USB-C power input and protection
- Optical sensing
- Controlled scan illumination
- Low / Medium / High hazard indicators
- Power and scan controls
- Programming, expansion, and debugging interfaces

**Status:** Design complete; fabrication and physical validation pending.

Full PCB design files, schematic, layout, and documentation are available in the [`PCB/`](PCB/) directory.

## Features

* ESP32-CAM image capture
* Machine learning image classification
* Flask-based AI server
* Real-time dashboard visualization
* Particle Argon hardware controller
* White illumination LEDs
* Hazard indication LEDs (Green / Yellow / Red)
* Wi-Fi setup portal
* SD card image logging
* Portable multi-network deployment

## Hardware

- ESP32-CAM with OV2640 camera
- Particle Argon
- EOSAS PCB v1.0
- TEMT6000 optical light sensor
- White scan illumination
- Low / Medium / High hazard LEDs
- Scan push button
- Power switch
- USB-C 5 V power input
- External illumination connector
- ESP32 programming header
- Expansion/debug header
- SD card storage
  
## Software

* Python
* Flask
* TensorFlow / Keras
* OpenCV
* C++
* Arduino Framework
* Particle Device OS

## System Workflow

1. User powers on EOSAS
2. Particle Argon initializes the hardware
3. ESP32-CAM connects to the configured network
4. EOSAS locates the inference server
5. User positions the target skin area
6. User presses the Scan button
7. Optical sensor measures illumination conditions
8. White scan lighting is activated
9. ESP32-CAM captures the image
10. Image is sent to the Python inference server
11. OpenCV preprocesses the image
12. TensorFlow generates the hazard prediction
13. Hazard score and confidence are calculated
14. Results are displayed on the dashboard
15. EOSAS updates the Low / Medium / High hazard indicator LED

## Engineering Challenges

During development, several challenges were encountered:

- Integrating embedded hardware with a machine learning workflow
- Managing image acquisition and transfer between devices
- Training and evaluating image classification models
- Designing a user interface for displaying results
- Coordinating communication between hardware and software subsystems

## Future Improvements

- Fabricate and validate EOSAS PCB v1.0
- Complete optical sensor calibration
- Build PCB-based custom enclosure
- Add battery-powered operation
- Improve hazard scoring
- Expand training data with EOSAS-captured images
- Improve condition-matching model
- Add automatic server discovery
- Improve wireless communication reliability

## Author

Mishael Agbali

Electrical Engineering Student
University of South Florida

LinkedIn:
https://www.linkedin.com/in/mishael-agbali/

GitHub:
https://github.com/XcapeCodes
