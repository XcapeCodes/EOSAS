# EOSAS - Embedded Optical Skin Analysis System

EOSAS is a portable AI-powered skin analysis device that combines embedded systems, computer vision, and machine learning to analyze skin images and provide hazard assessments.



\# EOSAS - Embedded Optical Skin Analysis System



\## Dashboard



!\[Dashboard](Images/dashboard.png)



\## Hardware Prototype



!\[Hardware](Images/eosas\_hardware\_overview.jpg)



\## Embedded Controller



!\[Argon](Images/eosas\_argon\_closeup.jpg)



## Overview

EOSAS captures skin images using an ESP32-CAM, processes them through a machine learning pipeline, and displays results through a custom Flask dashboard. A Particle Argon controls the user interface, including scan lighting, button controls, and hazard indication LEDs.

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

* ESP32-CAM
* Particle Argon
* White LEDs
* Status LEDs
* Momentary Push Button
* SD Card Storage

## Software

* Python
* Flask
* TensorFlow / Keras
* OpenCV
* C++
* Arduino Framework
* Particle Device OS

## System Workflow

User Presses Button
→ Argon Activates Scan Lighting
→ ESP32-CAM Captures Image
→ Image Sent To Flask Server
→ AI Model Generates Prediction
→ Dashboard Updates
→ Hazard Result Displayed Through LEDs

## Future Improvements

* Photodiode integration
* Custom PCB
* Custom enclosure
* Battery-powered operation
* Improved hazard scoring
* Automatic server discovery

## Author

Mishael Agbali

Electrical Engineering Student
University of South Florida

