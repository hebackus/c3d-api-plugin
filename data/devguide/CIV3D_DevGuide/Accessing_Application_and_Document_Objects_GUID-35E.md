<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Root Objects and Common Concepts in COM > Root Objects > Accessing Application and Document Objects -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-35EF1185-4BBB-422A-A86F-529DF05E2AC5.htm -->

# Accessing Application and Document Objects

The root object in the Autodesk Civil 3D COM hierarchy is the AeccApplication object. It contains information about the main application window, base AutoCAD objects, and a collection of all open documents. AeccApplication is inherited from the AutoCAD object AcadApplication. See the AutoCAD ObjectARX documentation for information about all inherited methods and properties.

The AeccApplication object is accessed by first using the exposed ThisDrawing object, an AutoCAD object of type AcadDocument. Its AcadDocument.Application property returns the AutoCAD AcadApplication object. From this point, use COM Automation to get the desired Autodesk Civil 3DAeccApplication object. 

This example demonstrates the process of accessing the AeccApplication and AeccDocument objects:
    
    
    Dim oAcadApp As AcadApplication
    Set oAcadApp = ThisDrawing.Application
    ' Specify the COM name of the object we want to access.
    ' Note that this always accesses the most recent version
    ' of Autodesk Civil 3D installed.
    Const sCivilAppName = "AeccXUiLand.AeccApplication.6.0"
    Dim oCivilApp As AeccApplication
    Set oCivilApp = oAcadApp.GetInterfaceObject(sCivilAppName)
     
    ' Now we can use the AeccApplication object.
    ' Get the AeccDocument representing the currently
    ' active drawing.
    Dim oDocument As AeccDocument
    Set oDocument = oCivilApp.ActiveDocument
    ' Set the viewport of the current drawing so that all
    ' drawing elements are visible.
    oCivilApp.ZoomExtents
    

This sample gets the objects from Autodesk Civil 3D 2009\. To gain access to the libraries of an older version, use the version number of the desired libraries to the COM object name. For example, to make a program that works with Autodesk Civil 3D 2007, replace:
    
    
    Const sCivilAppName = "AeccXUiLand.AeccApplication.4.0"
    

with the following line of code:
    
    
    Const sCivilAppName = "AeccXUiLand.AeccApplication.6.0"
    

The application object contains references to all open documents in the AeccApplication.Documents collection and the AeccApplication.ActiveDocument property. AeccDocument is inherited from the AutoCAD object AcadDocument. See the AutoCAD ObjectARX documentation for information on all inherited methods and properties.
