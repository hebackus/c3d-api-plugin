<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Dimensions and Tolerances (.NET) > Create Leaders and Annotation (.NET) > Edit Leaders (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-21D1FF58-DC99-4D00-AA6B-896A650C5632.htm -->

# Edit Leaders (.NET)

Any modifications to leader annotation that change its position affect the position of the endpoint of the associated leader. Also, rotating the annotation causes the leader hook line (if any) to rotate. 

Resize a leader by scaling it. If you scale the leader, the annotation stays in the same position relative to the leader endpoint but is not scaled. In addition to scaling, you can also move, mirror, and rotate a leader. Use the TransformBy method to edit the leader. Modify the associated annotation using its member properties and methods
