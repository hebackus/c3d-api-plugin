<!-- Developer's Guide > API Developer's Guide > Points > Point Groups > Using Point Groups -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-D8B45B99-3C09-45D8-8409-4A7190B5B433.htm -->

# Using Point Groups

Once a point group has been created, you can perform actions upon all the points in that group in a single operation. You can override point elevations, descriptions, styles, and label styles. 
    
    
    // Check to see if a particular point exists in the PointGroup
    ObjectId pointId = promptForEntity("Select a point", typeof(CogoPoint));
    CogoPoint cogoPoint = pointId.GetObject(OpenMode.ForRead) as CogoPoint;
    
    if (pointGroup.ContainsPoint(cogoPoint.PointNumber){
        _editor.WriteMessage("Point {0} is part of PointGroup {1}",
            cogoPoint.PointName, pointGroup.Name);
    }
    
    // Set the elevation of all points in the PointGroup to 100
    pointGroup.ElevationOverride.FixedElevation=100;
    pointGroup.ElevationOverride.ActiveOverrideType = PointGroupOverrideType.FixedValue;
    pointGroup.IsElevationOverriden = true;

Point groups can also be used to define or modify a TIN surface. The TinSurface.PointGroupsDefinition property is a collection of point groups. When a point group is added to the collection, every point in the point group is added to the TIN surface.
