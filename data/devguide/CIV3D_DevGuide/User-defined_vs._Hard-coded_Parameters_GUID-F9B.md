<!-- Developer's Guide > API Developer's Guide > Creating Custom Subassemblies Using .NET > Designing Custom Subassemblies > User-defined vs. Hard-coded Parameters -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-F9BBAFC8-91AC-4C80-A394-A5C8317B946B.htm -->

# User-defined vs. Hard-coded Parameters

Determine which of the geometric dimensions, behavior, and methodology will be hard-coded into the subassembly, and which will be controlled by user-defined input parameters.

One approach is to specify that a majority of items can be controlled by user input. This can add time and complexity to using the subassembly. Another approach is to make it so that it cannot be adapted to different situations. Generally, widths, depths, and slopes should be variable, not fixed. A compromise is to include a larger number of inputs, but provide default values usable in most design situations.

A good example of where to use hard-coded dimensions is with structural components, such as barriers and curb-and-gutter shapes. If there are five commonly-used variations of the same basic shape with different dimensions, it may be better to provide five separate subassemblies with hard-coded dimensions rather than making the user define the dimensions on a single subassembly. For example, users may be comfortable selecting from separate subassemblies for curb types A-E, which have predefined, hard-coded dimensions. You can always provide a generic subassembly with variable dimensions for scenarios where the common ones do not apply.
