<!-- Developer's Guide > API Developer's Guide > Points > Point Groups -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-F5C897B7-07D9-47F3-B411-43CE9FEDA050.htm -->

# Point Groups

A point group is a collection that defines a subset of the points in a document. Points may be grouped for a number of reasons, such as points that share common characteristics or are used to perform a common task (for example, define a surface). A collection of all point groups in a drawing is held in a document‘s CivilDocument.PointGroups property. Add a new point group by using the CivilDocument.PointGroups.Add() method and specifying a unique identifying string name. The ObjectId for a new, empty point group is returned. 
    
    
    // _civildoc is the active CivilDocument instance.
    ObjectId pointGroupId = _civildoc.PointGroups.Add("Example Point Group");
    PointGroup pointGroup = pointGroupId.GetObject(OpenMode.ForRead) as PointGroup;
