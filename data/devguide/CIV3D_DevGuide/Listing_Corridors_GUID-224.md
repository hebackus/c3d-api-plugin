<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Corridors in COM > Corridors > Listing Corridors -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-22444764-677B-4627-9C77-D01A4635C17D.htm -->

# Listing Corridors

The collection of all corridors in a document are held in the AeccRoadwayDocument.Corridors property.

The following sample displays the name and the largest possible triangle side of every corridor in a document:
    
    
    Dim oCorridors As AeccCorridors
    Set oCorridors = oRoadwayDocument.Corridors
     
    Dim oCorridor As AeccCorridor
    For Each oCorridor In oCorridors
        Debug.Print "Corridor: " & oCorridor.Name
        Debug.Print oCorridor.MaximumTriangleSideLength 
    Next
