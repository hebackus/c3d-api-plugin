<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Corridors in COM > Assemblies and Subassemblies > Getting Applied Subassembly Information -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-9A15FF8A-D5B7-41A0-8C76-E9DB661C0780.htm -->

# Getting Applied Subassembly Information

An applied subassembly consists of a series of calculated shapes, links, and points, represented by objects of type AeccCalculatedShape, AeccCalculatedLink, and AeccCalculatedPoint respectivly. 
    
    
    Dim S, O, E As Double
    With oAppliedSubassembly
        S = .OriginStationOffsetElevationToBaseline(0)
        O = .OriginStationOffsetElevationToBaseline(1)
        E = .OriginStationOffsetElevationToBaseline(2)
    End With
    Debug.Print "Station to baseline   : " & S
    Debug.Print "Offset to baseline    : " & O
    Debug.Print "Elevation to baseline : " & E
    

Applied subassemblies also contain a reference to the archetype subassembly (of type AeccSubassembly) in the subassembly database. 
    
    
    ' Get information about the subassembly template.
    Dim oSubassembly As AeccSubassembly
    Set oSubassembly = oAppliedSubassembly.SubassemblyDbEntity
    Debug.Print "Subassembly name: " & oSubassembly.Name
