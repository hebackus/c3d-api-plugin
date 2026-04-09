<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Define Layouts and Plot (.NET) > Layouts (.NET) > Layouts and Blocks (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-BEF5FDEE-925E-4E28-86E1-9B4A2CADD355.htm -->

# Layouts and Blocks (.NET)

The content of any layout is distributed among two different objects: a Layout and BlockTableRecord object. The Layout object contains the plot settings and the visual properties of the layout as it appears in the AutoCAD user interface. The BlockTableRecord object contains the geometry that is displayed on the layout such as annotation, floating viewports, and title blocks. The BlockTableRecord object also includes the Viewport object that controls the display of the drafting aids and layer properties used for the layout. 

Each Layout object is associated with one, and only one, BlockTableRecord object. To access the BlockTableRecord object associated with a given layout, use the BlockTableRecordId property. Conversely, each BlockTableRecord object is associated with one, and only one, Layout object. To access the Layout object associated with a given BlockTableRecord, use the LayoutId property for that block. The IsLayout property of a BlockTableRecord can be used to determine if it has an associated Layout object; TRUE is returned if the BlockTableRecord is associated with a Layout object.
