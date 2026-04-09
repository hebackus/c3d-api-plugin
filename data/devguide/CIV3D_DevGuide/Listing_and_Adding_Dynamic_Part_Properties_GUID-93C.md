<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Pipe Networks in COM > Base Objects > Listing and Adding Dynamic Part Properties -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-93CD63BD-A7E9-4156-BE0E-32B6E38CF62D.htm -->

# Listing and Adding Dynamic Part Properties

Each type of pipe and structure has many unique attributes (such as size, geometry, design, and composition) that cannot be stored in the standard pipe and structure properties. To give each part appropriate attributes, pipe and structure objects have sets of dynamic properties. A single property is represented by an AeccPartDataField object. Data fields are held in collections of type AeccPartDataRecord. You can reach these collections through the PartDataRecord property of AeccPartSizeFilter, AeccPipe, and AeccStructure objects. Each data field contains an internal variable name, a text description of the value, a global context used to identify the field, data type, and the data value itself.

This sample enumerates all the data fields contained in a pipe object “oPipe” and displays information from each field.
    
    
    Dim oPartDataField As AeccPartDataField
     
    Debug.Print "All data fields for this pipe:"
    Debug.Print "======"
    For Each oPartDataField In oPipe.PartDataRecord
       Debug.Print "Context name: "; oPartDataField.ContextString
       Debug.Print "Description:  "; oPartDataField.Description
       Debug.Print "Internal name:"; oPartDataField.Name
       Debug.Print "Value:        "; oPartDataField.Tag
       Debug.Print "Type of value:"; oPartDataField.Type
       Debug.Print "------"
    Next
    

To create your own dynamic properties, you first create a custom parameter describing the type and name of the property. You do this by using the pipe network catalog definitions object AeccPipeNetworkCatDef, which you access through the ambient property AeccPipeSettingsRoot.PipeNetworkCatDef. The AeccPipeNetworkCatDef object creates new parameters using the AeccPipeNetworkCatDef.DeclareNewParameter method. DeclareNewParameter takes some strings describing the parameter data type: 

  * a global context (the identification string used to access the parameter type)
  * a context description
  * a parameter name (the internally used name of the parameter)
  * a parameter description (the public name of the parameter used by the user interface, such as in the Part Properties tab of the Pipe and Structure Properties dialog boxes).

Once a parameter has been created, it can be made into a property available for use in parts through the AeccPipeNetworkCatDef.DeclarePartProperty method. 

Note:

The parameter name cannot contain spaces or punctuation characters.

This sample demonstrates declaring a parameter and making a property based on that parameter available to any pipe objects:
    
    
    Dim oSettings As AeccPipeSettingsRoot
    Dim oPipeNetworkCatDef As AeccPipeNetworkCatDef
     
    Set oSettings = oPipeDocument.Settings
    Set oPipeNetworkCatDef = oSettings.PipeNetworkCatDef
    oPipeNetworkCatDef.DeclareNewParameter _
      "Global Context 01", _
      "Context Description", _
      "TParam", _
      "Test Parameter", _
      aeccDoubleGeneral, _
      aeccDouble, _
      "", _
      True, _
      False
     
    oPipeNetworkCatDef.DeclarePartProperty 
      "Global Context 01", aeccDomPipe, 10
    

You can now choose from among those properties available to the part’s domain and create a data field.
    
    
    ' Make a data field based on the "Global Context 01"
    ' property and add it to a pipe object "oPipe". Set
    ' the value of the data field to "6.5".
    Dim oPartDataField As AeccPartDataField
    Set oPartDataField = oPipe.PartDataRecord.Append
      ("Global Context 01", 0)
    oPartDataField.Tag = 6.5
