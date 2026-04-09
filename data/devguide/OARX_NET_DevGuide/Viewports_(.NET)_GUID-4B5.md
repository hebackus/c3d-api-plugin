<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Define Layouts and Plot (.NET) > Viewports (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-4B512161-DBD4-43DA-BD89-AA2EA564F9F9.htm -->

# Viewports (.NET)

When working in Model space you draw geometry in tile viewports which are represented by ViewportTableRecord objects. You can display one or several different viewports at a time. If several tiled viewports are displayed, editing in one viewport affects all other viewports. However, you can set the magnification, viewpoint, grid, and snap settings individually for each viewport. 

In Paper space, you work in floating viewports which are represented by Viewport objects and can contain different views of your model. Floating viewports are treated as objects that you can move, resize, and shape to create a suitable layout. You also can draw objects, such as title blocks or annotations, directly in the Paper space view without affecting the model itself.
