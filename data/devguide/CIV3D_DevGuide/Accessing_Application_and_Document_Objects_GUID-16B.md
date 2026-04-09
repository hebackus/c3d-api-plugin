<!-- Developer's Guide > API Developer's Guide > Root Objects and Common Concepts > Root Objects > Accessing Application and Document Objects -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-16B1A3F9-35F7-4703-B5FD-F2AC00E6AB57.htm -->

# Accessing Application and Document Objects

The root object in the Autodesk Civil 3D .NET hierarchy is the CivilApplication object. It contains a reference to the currently active document, and information about the running product. 

Note:

Unlike the COM API, CivilApplication does not inherit from the AutoCAD object Autodesk.AutoCAD.ApplicationServices.Application. Therefore, if you need access to application-level methods and properties (such as the collection of all open documents, information about the main window, etc.), you need to access through the AutoCAD Application object. See the ObjectARX Managed Class Reference in the ObjectARX SDK for information about this class.

The active CivilDocument object is accessed by importing the AutodeskCivil.ApplicationServices namespace, and getting the CivilApplication.ActiveDocument property. 

This example demonstrates the process of accessing the CivilApplication and CivilDocument objects:
    
    
    using Autodesk.Civil.ApplicationServices;
    namespace CivilSample {
        class CivilExample {
            CivilDocument doc = CivilApplication.ActiveDocument;
        }
    }
