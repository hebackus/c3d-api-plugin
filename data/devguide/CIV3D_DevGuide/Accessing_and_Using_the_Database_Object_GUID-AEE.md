<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Root Objects and Common Concepts in COM > Root Objects > Accessing and Using the Database Object -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-AEEBEDD9-A079-4363-AF62-15DAA87D5F6B.htm -->

# Accessing and Using the Database Object

Each document has an associated database object of type AeccDatabase that is accessed through the AeccDocument.Database property. The database object is inherited from the AutoCAD ObjectARX object AcadDatabase. The AeccDatabase object contains references to all the same Autodesk Civil 3D entities as the AeccDocument object. However, it is the only object that contains references to base AutoCAD entities. See the AutoCAD ObjectARX documentation for more information.
    
    
    ' Add a polyline to the drawing's collection of objects.
    Dim oPolyline As AcadPolyline
    Dim dPoints(0 To 8) As Double
    dPoints(0) = 1000: dPoints(1) = 1000: dPoints(2) = 0
    dPoints(3) = 1000: dPoints(4) = 4000: dPoints(5) = 0
    dPoints(6) = 4000: dPoints(7) = 4000: dPoints(8) = 0
    ' The database is where all such objects are stored.
    Set oPolyline = oDocument.Database.ModelSpace.AddPolyline(dPoints)
    oPolyline.Closed = True
    

The AeccDatabase object also has an AddEvent() method, that lets you send an event to the Event Viewer in the Autodesk Civil 3D user interface:
    
    
    Dim oAeccApp As AeccApplication
    Set oAeccApp = ThisDrawing.Application.GetInterfaceObject("AeccXUiLand.AeccApplication.6.0")
    oAeccApp.Init ThisDrawing.Application
    Dim oDatabase As AeccDatabase
    Set oDatabase = oAeccApp.ActiveDocument.Database
    oDatabase.AddEvent aeccEventMessageError, "PipeLengthRule", "Parameter Bad"
