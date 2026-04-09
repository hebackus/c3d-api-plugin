<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Root Objects and Common Concepts in COM > Ambient Settings > Changing General and Specific Settings -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-3436D5B0-F2C6-4BD9-A1CA-E4FFF443B41B.htm -->

# Changing General and Specific Settings

Ambient settings are default properties and styles that apply to the drawing as a whole or to objects when they are first created. The document’s settings are accessed through the properties of the AeccSettingsRoot object, which is obtained from the AeccDocument.Settings property. There are settings for objects and commands. The object properties define the settings for items in general, or of particular classes of items, such as alignments, gradings, parcels, points, profiles, profile views, sample lines, sections, section views, and surfaces. Although each of these objects are unique, they all share some common features:

Property Name | Description  
---|---  
StyleSettings | Specifies the default styles and label styles.  
LabelStyleDefaults | Specifies the common attributes for labels.  
NameTemplate | Specifies the standard pattern of names.  
AmbientSettings | Specifies which units of measurement are used and displayed.  
CreationSettings | Not on all objects. Optional. Specifies item-specific default values.  
  
The command settings apply to commands, and correspond to the settings in the Commands folder for each item in the Autodesk Civil 3DToolspace Settings Tab.

The following sample determines what angle units are used for all displays related to points:
    
    
    Dim oPointSettings as AeccSettingsPoint
    Set oPointSettings = oDocument.Settings.PointSettings
    Dim oAmbientSettings as AeccSettingsAmbient
    Set oAmbientSettings = oPointSettings.AmbientSettings
    Dim oAngleUnit as AeccAngleUnitType
    Set oAngleUnit = oAmbientSettings.AngleSettings.Unit.Value
     
    If (oAngleUnit = aeccAngleUnitDegree) Then
        ' Units are displayed in degrees
    ElseIf (oAngleUnit = aeccAngleUnitRadian) Then
        ' Units are displayed in radians
    Else
        ' Units are displayed in gradians
    End If
