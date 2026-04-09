<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Pipe Networks in COM > Structures > Creating Structure Styles -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-1863D790-BF33-4072-9523-FF0D67DC2253.htm -->

# Creating Structure Styles

A structure style controls the visual appearance of structures in a document. All structure style objects are stored in the AeccPipeDocument.StructureStyles collection. Structure styles have four methods for controlling general appearance attributes and three properties for controlling display attributes that are specific to structures. The methods DisplayStylePlan|Profile|Section|Model and HatchStylePlan|Profile|Section all take a parameter describing the feature being modified and return a reference to the AeccDisplayStyle or AeccHatchDisplayStyle object controlling common display attributes such as line styles and color. The properties PlanOption, ProfileOption, and ModelOption set the display size of the structure and whether the structure is shown as a model of the physical object or only symbolically. A structure object is given a style by assigning the AeccStructure.Style property to a AeccStructureStyle object.

This sample creates a new structure style object, sets some of its properties, and assigns it to a structure object:
    
    
    ' Create a new structure style object.
    Dim oStructureStyle As AeccStructureStyle
    Set oStructureStyle = oPipeDocument.StructureStyles.Add("Structure Style 01")
     
    oStructureStyle.DisplayStylePlan(aeccDispCompStructure).color = 30
    oStructureStyle.PlanOption.MaskConnectedObjects = True
     
    ' Set a structure to use this style.
    Set oStructure.Style = oStructureStyle
