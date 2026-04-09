<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Develop Applications (.NET) > Handle Errors (.NET) > Define Application Error Types (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-90BC83EA-43D1-4006-A090-20BE4B8C3397.htm -->

# Define Application Error Types (.NET)

There are three different types of errors you can encounter in your applications: compile-time errors, runtime errors, and logic errors. 

  * Compile-time errors occur during the construction of your application. These errors consist mostly of syntax mistakes, and variable scope and data type problems. In .NET, these types of errors are caught by the development environment. When you enter an incorrect line of code, the line is underlined and the problem with the code line is displayed in a tooltip when the cursor is positioned over the underlined text. Compile-time errors must be corrected before the .NET assembly for the application can be built. 
  * Runtime errors are a little more difficult to find and correct. They occur during the execution of your code, and often involve information provided by the user or files that are expected to be present. For example, if your application requires the user to enter the name of a drawing and the user enters a name for a drawing that does not exist, a runtime error occurs. To handle runtime errors effectively, you must predict what kinds of problems could happen, trap them, and then write code to handle these situations. 
  * Logic errors are the most difficult to find and correct. Symptoms of logic errors include situations in which there are no compile-time errors and no runtime errors, but the outcome of your program is still incorrect. This is what programmers refer to as a defect or bug. A defect can be very easy or difficult to track down. 

Information on finding and correcting errors can be found in the documentation for your development environment. AutoCAD-specific errors fall into the runtime error category, so these types of errors are covered in this documentation.
