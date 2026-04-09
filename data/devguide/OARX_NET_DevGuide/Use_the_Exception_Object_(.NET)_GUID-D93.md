<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Develop Applications (.NET) > Handle Errors (.NET) > Trap Runtime Errors (.NET) > Use the Exception Object (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-D93FC79E-B78B-4D41-A16B-C7BFFB59FD1F.htm -->

# Use the Exception Object (.NET)

The Exception object is used to obtain information about the error trapped with the Catch clause of a Try statement. The Exception object used for the AutoCAD .NET API is based on the Exception object of the Microsoft® .NET. To determine the error that is trapped by the Catch clause, you can use the properties of the Exception object. Some of the member properties of the Exception object that you can get information about the error are: 

  * **ErrorStatus** \- Returns the Autodesk.AutoCAD.Runtime.ErrorStatus enum value assigned to the exception. 
  * **Message** \- Returns a text message that explains the exception. 
  * **Source** \- Returns the application or object that caused the exception. 
  * **StackTrace** \- Returns a string representation of the frames on the call stack when the exception occurred. 
  * **TargetSite** \- Returns the method that threw the exception.
