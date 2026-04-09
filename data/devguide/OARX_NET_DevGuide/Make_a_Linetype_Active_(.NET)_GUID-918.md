<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Use Layers, Colors, and Linetypes (.NET) > Work With Linetypes (.NET) > Make a Linetype Active (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-91849E9C-7B67-471D-9925-B55D0B25ABB6.htm -->

# Make a Linetype Active (.NET)

To use a linetype, you must make it active. All newly created objects are drawn using the active linetype. There are two different methods for applying a linetype to an object: direct or inherited. You can directly assign a linetype to an object which overrides the linetype assigned to the layer the object is on. Otherwise, an object inherits the linetype of the layer it is on by having its Linetype or LinetypeId property set to represent the ByLayer linetype. 

Note: Xref-dependent linetypes cannot be made active. 

There are three linetypes that exist in each drawing: BYBLOCK, BYLAYER and CONTINUOUS. Each of these linetypes can be accessed from the Linetype table object or using methods from the SymbolUtilityServices object. The following methods allow you to obtain the object id for these default linetypes: 

  * **GetLinetypeByBlockId** \- Returns the object id for the BYBLOCK linetype. 
  * **GetLinetypeByLayerId** \- Returns the object id for the BYLAYER linetype. 
  * **GetLinetypeContinuousId** \- Returns the object id for the CONTINUOUS linetype.
