<!-- Developer's Guide > API Developer's Guide > Root Objects and Common Concepts > Settings > Accessing Drawing, Feature, and Command Settings -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-9196EDF6-9BAF-44D9-A121-3E990E04B205.htm -->

# Accessing Drawing, Feature, and Command Settings

Settings apply at three levels in Autodesk Civil 3D: 

  1. Drawing level: there are drawing-wide settings, such as units and zone, abbreviations, etc. There are also ambient settings, which affect a variety of Autodesk Civil 3D behaviors. While these settings also apply drawing-wide, they can be overridden at the feature or command level. 
  2. Feature (object) level: ambient settings override drawing level ambient settings for that feature only. There are also feature-specific settings, such as default styles. 
  3. Command level: ambient settings can be set on a command-by-command basis. These settings override both drawing level and feature level settings. 

For more information on settings in general, see [About Settings](<https://beehive.autodesk.com/community/service/rest/cloudhelp/resource/cloudhelpchannel/guidcrossbook/?v=2026&p=CIV3D&l=ENU&accessmode=live&guid=GUID-329DAB7D-2497-45AE-985A-D58720439D8A>). 

A document’s settings are accessed through the properties of the SettingsRoot object, which is obtained from the Document.Settings property. This object contains the DrawingSettings property (type SettingsDrawing), which contains all the top-level ambient settings for the document. It also has the GetSettings() method, which gets feature and command settings. 

Drawing settings and general ambient settings are in the Autodesk.Civil.Settings namespace, while feature and command settings are in the namespace for the related feature. For example, alignment-related ambient and command settings are in the Autodesk.Civil.Land.Settings namespace. 

The following sample shows how to access the angle settings for alignments: 
    
    
    SettingsAlignment alignmentSettings = doc.Settings.GetSettings<SettingsAlignment>();
    Autodesk.Civil.Settings.SettingsAmbient.SettingsAngle angleSettings = alignmentSettings.Angle;
    ed.WriteMessage(@"Alignment settings:\n  Precision: {0}\n  Rounding: {1}  
    Unit: {2}\n  Drop Decimal: {3}\n  DropZeros: {4}\n ",
        angleSettings.Precision.Value, angleSettings.Rounding.Value, 
        angleSettings.Unit.Value, angleSettings.DropDecimalForWholeNumbers.Value, 
        angleSettings.DropLeadingZerosForDegrees.Value);  
    

The command settings apply to commands, and correspond to the settings in the Commands folder for each item in the Autodesk Civil 3DToolspace Settings Tab. Each command setting has a corresponding class named SettingsCmd _CommandName_. For example, the settings class corresponding to the `CreateAlignmentLayout` command is SettingsCmdCreateAlignmentLayout. As with other types of settings, you use the CivilDocument.Settings.GetSettings() method to access command settings objects in the document. 

The following snippet determines what the “Alignment Type Option” is for the `CreateAlignmentLayout` command: 
    
    
    SettingsCmdCreateAlignmentLayout alignLayoutCmdSettings = doc.Settings.GetSettings<SettingsCmdCreateAlignmentLayout>();         
    ed.WriteMessage(@"Alignment Layout Command settings: AlignmentType: {0}  ",
        alignLayoutCmdSettings.AlignmentTypeOption.AlignmentType.Value
       );
    

The result of this code returns the current command setting: 

Getting command settings
