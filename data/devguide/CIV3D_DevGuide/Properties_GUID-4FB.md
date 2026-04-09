<!-- Developer's Guide > API Developer's Guide > Getting Started > Migrating COM code to .NET > Properties -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-4FB2FACB-6AB2-4BFC-945C-4A4DA2B7CD02.htm -->

# Properties

In the COM API, properties are usually simple built-in types, such as double, or types such as BSTR that map to built-in VBA types such as String. In the .NET API, most properties are one of the Property* classes that implement the IProperty interface. For these properties, you get or set the Value of the property. For example, this code in COM:
    
    
    oLabelStyleLineComponent.Visibility = True
    

Becomes this in .NET:
    
    
    oLabelStyleLineComponent.General.Visible.Value = true;
    

Note:

There are a few other changes here: the Visibility property is renamed Visible, which has moved to a sub-property of LabelStyleLineComponent called General.
