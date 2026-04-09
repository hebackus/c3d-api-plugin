<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Use Layers, Colors, and Linetypes (.NET) > Work With Layers (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-97955B2B-F823-4787-86C7-97F7E701FD72.htm -->

# Work With Layers (.NET)

You are always drawing on a layer. It may be the default layer or a layer you create and name yourself. Each layer has an associated color and linetype among other properties. For example, you can create a layer on which you draw only centerlines and assign the color blue and the linetype CENTER to that layer. Then, whenever you want to draw centerlines you can switch to that layer and start drawing. 

All layers and linetypes are stored in separate symbol tables. Layers are kept within the LayerTable, and linetypes are kept within the LinetypeTable.
