# Smart Attendance & Visitor Management System

An automated Raspberry Pi-based attendance and visitor management system using face recognition, computer vision, and local database storage.

## Features

* Face registration
* Automatic face recognition
* Automated attendance marking
* Duplicate attendance prevention
* Unknown face detection
* Digital visitor IN / OUT tracking
* Admin dashboard
* SQLite database
* CSV report export
* Date and time tracking
* GPIO LED and buzzer support
* Optional relay / door-lock integration
* Raspberry Pi optimized operation
* Local-first data processing

## Hardware Used

* Raspberry Pi
* USB Webcam
* GPIO Pins
* LED Indicators
* Buzzer
* Optional Relay / Door Lock
* Power Supply
* Display / Monitor

## Software Used

* Python
* OpenCV
* LBPH Face Recognition
* SQLite
* Tkinter
* GPIO
* CSV / Pandas
* Raspberry Pi OS / Linux

## Operation

### Face Registration

The administrator enters the user's information and registers their face using the USB webcam.

Multiple face images are captured and stored in the dataset. The recognition model is then trained and saved as `trainer.yml`.

Example flow:

`User Registration → Face Capture → Dataset → Model Training → trainer.yml`

### Attendance

The webcam continuously captures frames and detects faces.

The system compares detected faces with the trained LBPH model.

If a registered user is recognized, the system checks whether attendance has already been marked for the current date.

* Recognized + not marked → Attendance recorded
* Recognized + already marked → No duplicate entry
* Unknown face → No attendance recorded

### Visitor Management

Visitors can be digitally registered with:

* Name
* Phone number
* Purpose
* Host
* Date
* Entry time

When the visitor leaves, their exit time is recorded and their status changes from `IN` to `OUT`.

Example:

`Visitor Entry → Status: IN → Visitor Exit → Status: OUT`

## Image / Data Storage

User information, attendance records, and visitor records are stored locally using SQLite.

Attendance reports and visitor reports can be exported as CSV files for Excel, analysis, auditing, or archival.

## Database

The system uses SQLite with separate records for:

* Users
* Attendance
* Visitors
* Admins

Attendance is linked to registered users to maintain organized historical records.

## GPIO Support

GPIO can be used for hardware feedback and optional access control.

### Recognized User

`Face Recognized → GPIO Output → Green LED → Optional Door Relay`

### Unknown User

`Unknown Face → GPIO Output → Red LED + Buzzer`

A physical button can also be used as a GPIO input for visitor exit or other hardware controls.

## Raspberry Pi Optimization

The system is designed to operate reliably on low-cost Raspberry Pi hardware.

Optimization techniques include:

* Lower camera resolution
* Frame resizing
* Efficient OpenCV detection
* Limited recognition frequency
* Lightweight SQLite database
* Lightweight Tkinter interface
* Modular Python architecture
* Local data processing

## Project Workflow

### Registration

`Register User → Capture Images → Train Model → Update Recognition Model`

### Attendance

`Open Camera → Detect Faces → Recognize Users → Check Records → Mark Attendance`

### Visitor Management

`Register Visitor → Record Entry → Track Visitor → Record Exit`

## Advantages

* Low cost
* Automated attendance
* Contactless operation
* Local data storage
* Easy reporting
* Digital visitor tracking
* Modular architecture
* Expandable hardware
* Raspberry Pi friendly

## Applications

* Colleges
* Schools
* Offices
* Laboratories
* Libraries
* Training centers
* Small businesses
* Restricted-access areas

## Future Improvements

Potential future upgrades:

* Cloud synchronization
* Mobile application
* Email / SMS notifications
* Multi-camera support
* Advanced face recognition models
* Liveness detection
* RFID and fingerprint integration
* Real-time analytics
* Remote monitoring
* Encrypted credentials

## Conclusion

The Smart Attendance & Visitor Management System combines computer vision, face recognition, database management, automation, and Raspberry Pi hardware to create an affordable and scalable solution for attendance and visitor monitoring.

## Author

**Mithil J.**

Computer Science / AI & ML
