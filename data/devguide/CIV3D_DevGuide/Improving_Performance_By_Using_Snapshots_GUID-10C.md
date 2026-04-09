<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Surfaces in COM > Working with Surfaces > Improving Performance By Using Snapshots -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-10CC9D4C-2478-4007-80AE-993BDA122923.htm -->

# Improving Performance By Using Snapshots

A surface is made up of all the operations that modified the surface’s triangles. If you rebuild the surface, re-performing all these operations can be slow. Snapshots can improve performance by recording all the triangles in a surface. Subsequent rebuilds start from the data of the snapshot, thus saving time by not performing complicated calculations that have already been done once. Surfaces have CreateSnapshot, RebuildSnapshot, and RemoveSnapshot methods. Both CreateSnapshot and RebuildSnapshot will overwrite an existing snapshot.

Tip:

RebuildSnapshot will cause an error if the snapshot does not exist. CreateSnapshot and RebuildSnapshot can also cause errors if the surface is out-of-date.
