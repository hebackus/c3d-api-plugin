<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Develop Applications (.NET) > Securing Managed .NET Applications (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-C3E22BC9-5703-4F7A-AFFA-D9FE9B39E1BA.htm -->

# Securing Managed .NET Applications (.NET)

Cybersecurity attacks are one of the leading causes of intellectual property (IP) and productivity loss. 

Autodesk has been making the investment in fortifying and securing AutoCAD-based products since the 2013 product releases through the introduction of these and other features: 

  * **Safe mode** \- Restricts the loading of custom applications 
  * **Trusted application locations and domains** \- Restricts the locations in which AutoCAD-based products can load custom applications 
  * **Support for and validation of digitally signed applications** \- Identifies the company who authored\published the custom application and whether the file was altered after it was published 
  * **Scan for vulnerable modules during development** \- Checks are made to verify the latest version of development libraries are being used prior to the product release 

In order to truly secure AutoCAD-based applications, all entry points must be protected and those include custom and third-party applications. There are a number of tasks you should perform to help secure the applications you write and distribute, and those tasks are: 

  * Use security related compiler flags 
    * /WARNASERROR – Enables the treatment of all warnings as errors which can help prevent the use of obsolete/deprecated members. 
  * Digitally sign all executable (DLL/EXE/JS/…) files 
  * Validate any input before it is used 
  * Use the HTTPS protocol for accessing information over the network 
  * When utilizing a third-party and open source library, make sure the latest version is being used by your application and that the library is being maintained 
  * Check for any memory leaks utilizing the tools built into Microsoft Visual Studio or a third-party utility, such as Micro Focus DevPartner for Visual C++ / BoundsChecker Suite and TeamBLUE PurifyPlus 
  * Test your applications to make sure they work properly with the default values of the following settings: 
    * LEGACYCODESEARCH = 0 - Controls whether searching for executable files includes the folder from which the program is started. 
    * SECURELOAD = 1 - Controls whether AutoCAD loads executable files based on whether they are in a trusted folder.
