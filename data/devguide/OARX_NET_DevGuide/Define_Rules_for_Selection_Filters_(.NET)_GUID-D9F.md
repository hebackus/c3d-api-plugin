<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Work With Selection Sets (.NET) > Define Rules for Selection Filters (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-D9FB23AE-D853-4D00-A910-4F66FCC4607A.htm -->

# Define Rules for Selection Filters (.NET)

You can limit which objects are selected and added to a selection set by using a selection filter. A selection filter list can be used to filter selected objects by properties or type. For example, you might want to select only blue objects or objects on a certain layer. You can also combine selection criteria. For example, you can create a selection filter that limits selection to blue circles on the layer named Pattern. 

Note: Filtering recognizes values explicitly assigned to objects, not those inherited by the layer. For example, if an object’s linetype property is set to ByLayer and the layer it is assigned is set to the Hidden linetype; filtering for objects assigned the Hidden linetype will not select these objects since their linetype property is set to ByLayer.
