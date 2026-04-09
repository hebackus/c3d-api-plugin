<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Define Layouts and Plot (.NET) > Viewports (.NET) > Scale Pattern Linetypes in Paper Space (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-30161103-5E6B-453D-B1F5-2DBBBB03BDF0.htm -->

# Scale Pattern Linetypes in Paper Space (.NET)

In Paper space, you can scale any type of linetype in two ways. The scale can be based on the drawing units of the space in which the object was created (Model or Paper). The linetype scale also can be a uniform scale based on Paper space units. You can use the PSLTSCALE system variable to maintain the same linetype scaling for objects displayed at different scales in different viewports. It also affects the line display in 3D views. 

The following illustration shows the pattern linetype scaled uniformly in Paper space. Notice that the linetype in the two viewports have the same scale, even though each of the viewports have different scales. 

Use the SetSystemVariable method to set the value of the PSLTSCALE system variable.
