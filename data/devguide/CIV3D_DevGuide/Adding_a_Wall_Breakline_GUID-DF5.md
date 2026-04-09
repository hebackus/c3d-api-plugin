<!-- Developer's Guide > API Developer's Guide > Surfaces > Working with TIN Surfaces > Adding a Wall Breakline -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-DF5AFE09-A9BE-4502-BFC6-B5B6B5776284.htm -->

# Adding a Wall Breakline

A wall breakline is used when the height of the surface on one side of the breakline is different than the other side. The AddWallBreaklines() method creates two breaklines, one for the top of the wall and one for the bottom. However, you cannot have a perfectly vertical wall in a TIN surface. The first breakline is placed along the path specified, and the second breakline is very slightly offset to one side and raised or lowered by a relative elevation. There are two versions of AddWallBreaklines(): one takes a WallBreaklineCreation structure that sets one elevation for all vertices in the breakline, while WallBreaklineCreationEx specifies an elevation for each individual vertex. The IsRightOffset property indicates in which direction the wall at each entity endpoint is offset. If set to true, the offset is to the right as you walk along the breakline from the start point to the end.
