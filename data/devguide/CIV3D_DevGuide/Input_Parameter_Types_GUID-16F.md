<!-- Developer's Guide > API Developer's Guide > Creating Custom Subassemblies Using .NET > Designing Custom Subassemblies > Input Parameter Types -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-16FCCF6D-D117-40F9-968F-7C73066EF72C.htm -->

# Input Parameter Types

The table below describes the various types of input parameters:

Input Parameter | Description  
---|---  
Widths | The cross-sectional horizontal distance between two points on the roadway assembly. Widths are generally given as positive numeric values, and extend in the direction of insertion (left or right) of the subassembly. Many components that require a width are likely candidates for using an alignment as an optional target parameter. The width is then calculated at each station to tie to the alignment, if one is given.  
Offsets | The cross-sectional horizontal distance from the corridor baseline to a point on the roadway assembly. The difference between an Offset and a Width is that Widths are measured from some point on the assembly, while Offsets are measured from the corridor baseline. Positive and negative values indicate positions right or left of the baseline. Components requiring an offset are also likely to use an alignment to allow a calculated offset.  
% Slopes | Lanes, shoulders, and other components usually have a slope defined as ratio of rise-to-run. There are two common conventions for how these are expressed. They can either be a unitless ratio (-0.05), or a percent value (-5). Both of these examples define a 5% slope downwards. The same convention should be used for all subassemblies in a catalog. In some cases, you may want the component to have a variable slope, tying to a profile. The profile name can be given as a target parameter.  
Ratio Slopes | Cut slopes, fill slopes, ditch side slopes, median slopes, and many other roadway components are commonly expressed as a run-to-rise ratio, such as 4 : 1. These may be signed or unsigned values, depending on circumstances. For example, a fill slope is always downward, so it may not be necessary to force the user to enter a value like “-4”.   
Point, Link, and Shape Codes | In most cases, point, link, and shape codes should be hard-coded to ensure that consistent codes are assigned across the entire assembly. The primary exception is with generic link subassemblies that allow users to add links to the assembly as needed. These might be used for paved or unpaved finish grade, structural components, pavement subsurfaces, and many other unanticipated components. In these scenarios, the end-user assigns point, link, and shape codes that coordinate with the overall assembly.
