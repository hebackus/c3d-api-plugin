<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Points in COM > Point Groups > Creating Point Groups -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-72568C6A-2DC6-4CF2-9B1C-D4CD1454C77B.htm -->

# Creating Point Groups

A point group is a collection that contains a subset of the points in a document. A collection of all point groups is held in a document‘s AeccDocument.PointGroups property. Add a new point group by using the AeccDocument.PointGroups.Add method and specifying a unique identifying string name. A new empty point group is returned.
    
    
    ' Get the collection of all point groups from the document.
    Dim oPtGroups As AeccPointGroups
    Dim oPtGroup As AeccPointGroup
    Set oPtGroups = oAeccDocument.PointGroups
     
    ' Add our group to the collection of groups.
    Set oPtGroup = oPtGroups.Add("Sample point group")
