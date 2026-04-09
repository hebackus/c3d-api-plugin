<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Points in COM > Point Groups > Using Point Groups -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-D8F3C5DC-CD5F-447F-9BD4-19D181F675C2.htm -->

# Using Point Groups

Once a point group has been created, you can perform actions upon all the points in that group in a single operation. You can override point elevations, descriptions, styles, and label styles.
    
    
    ' Check to see if a particular point exists in the group.
    If (oPtGroup.ContainsPoint(oPoint1.Number) = False) Then
        Debug.Print oPoint1.Name & " is not in the point group."
    End If
     
    ' Set the elevation of all the points in the group to 100.
    oPtGroup.Elevation = 100
    oPtGroup.OverrideElevation = True
    

Point groups can also be used to define or modify a TIN surface. The AeccTinSurface.PointGroups property is a collection of point groups. When a point group is added to the collection, every point in the point group is added to the TIN surface. 
    
    
    ' oTinSurf is a valid object of type AeccTinSurface.
    ' oPointGroup is a valid object of type AeccPointGroup.
    oTinSurf.PointGroups.Add oPointGroup
