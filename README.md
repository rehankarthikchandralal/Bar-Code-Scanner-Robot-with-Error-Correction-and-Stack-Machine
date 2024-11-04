# LEGO Mindstorms EV3 Barcode Scanning Robot

**Project Overview**

This project involved building a LEGO Mindstorms EV3 robot capable of:

1. **Scanning Barcodes:** Precisely scanning individual barcodes on a sheet.
2. **Decoding Barcodes:** Using Hamming Code logic to decode the scanned data.
3. **Displaying and Speaking Results:** Audibly communicating the decoded information.
4. **Scrolling Through Barcode Sheet:** Mechanically navigating to different barcode positions.

**Technical Implementation**

* **Hardware:**
  - LEGO Mindstorms EV3 Core Set
  - Motors for movement and barcode scanning
  - Sensors for  barcode detection
* **Software:**
  -  Python with appropriate libraries
  - Hamming Code implementation
  - Stack Machine for instruction/operand execution
* **Version Control:** GitLab

**Workflow**

1. **Barcode Scanning:**
   - Robot precisely positions itself over a barcode using motor control.
   - Barcode sensor captures the image.
2. **Decoding:**
   - Captured image is processed to extract raw data.
   - Hamming Code is applied to correct errors and extract the original data.
3. **Result Processing:**
   - Decoded data is interpreted as a sequence of instructions or characters.
   - A stack machine executes these instructions or displays/speaks the characters.
4. **Scrolling:**
   - Motors are controlled to move the robot to the next barcode position.





