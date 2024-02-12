# crease-line-detection
A machine vision Tkinter GUI application that allows the user to draw four vertical lines on a live video stream and record the distance between them; used as a performance metric in paper folding operations of a packaging company.

You need to have Tkinter, OpenCV and pyscreenshot installed into your Python environment before running this script.

Demo:

![screenshot](https://github.com/salman1851/crease-line-detection/assets/131760691/01964faf-c8af-4687-84ed-b1e7ec5f8a18)

By default, the application reads images from the webcam. You can replace it with the IP address of your camera.

Click on the 'Take Picture' button to freeze the frame. You can then mark the lines using the colored buttons on the left hand side of the canvas. The lines can be moved across the horizontal axis by clicking anywhere on the frozen image.

The frame can be rotated using the slider. Click on the "Rotate Image" button next to the slider to rotate a frozen image. 

When you click the "Process Picture" button, the difference between the first two lines and the last two lines will be calculated and added to the table. You can move to the next point by clicking the "Next Point" button. 

Click on the "Save all Points" button to export the table as a CSV file.
