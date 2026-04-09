<!-- Developer's Guide > API Developer's Guide > Surfaces > Working with Surfaces > Improving Performance by Using Snapshots -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-3B20192C-7845-4BC3-B08D-2B5A0FE23D31.htm -->

# Improving Performance by Using Snapshots

A surface is made up of all the operations that modifiy the surface’s triangles. If you rebuild the surface, re-performing all these operations can be slow. Snapshots can improve performance by recording the current state of all the triangles in a surface. Subsequent rebuilds start from the data of the snapshot, thus saving time by not performing complicated calculations that have already been done once. Surface objects have CreateSnapshot(), RebuildSnapshot(), and RemoveSnapshot() methods. Both CreateSnapshot() and RebuildSnapshot() will overwrite an existing snapshot. 

Note:

RebuildSnapshot() will cause an error if the snapshot does not exist. CreateSnapshot() and RebuildSnapshot() can also cause errors if the surface is out-of-date. You can check whether the Surface has a snapshot already with the Surface.HasSnapshot property. For example: 
    
    
    if (oSurface.HasSnapshot)
    {
        oSurface.RemoveSnapshot();
    }
    oSurface.CreateSnapshot();
    oSurface.RebuildSnapshot();
