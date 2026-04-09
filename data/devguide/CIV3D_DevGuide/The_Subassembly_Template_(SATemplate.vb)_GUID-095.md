<!-- Developer's Guide > API Developer's Guide > Creating Custom Subassemblies Using .NET > Structure of Subassembly Programs > The Subassembly Template (SATemplate.vb) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-09560952-D0A2-44EF-9B0E-C7DBE9E1F0AE.htm -->

# The Subassembly Template (SATemplate.vb)

All custom subassemblies are defined as classes that inherit from the SATemplate class. SATemplate provides four methods that you can override in your own class to provide functionality of your subassembly. They are described in the following table: 

Overridable Method | Purpose for Overriding   
---|---  
GetLogicalNamesImplement (input: CorridorState) | Define the list of target parameters that appear in the "Set All Logical Names" dialog box used when creating a corridor model.  
GetInputParametersImplement (input: CorridorState) | Define the list of input parameters, including their names, types, and default values.  
GetOutputParametersImplement (input: CorridorState) | Define the list of output parameters, including their names, types, and default values. If a parameter is to be used for both input and output, that property is specified in this method.  
DrawImplement (input: CorridorState) |  **Must be overridden.** Contains the code for accessing parameter values, adjusting the shape of the subassembly, and then adding the points, links, and shapes that make up your subassembly to an existing assembly.   
  
_SATemplate.vb_ is located in the _< Autodesk Civil 3D Install Directory>\Sample\Civil 3D API\C3DStockSubAssemblies_ directory.
