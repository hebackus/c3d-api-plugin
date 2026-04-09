<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Pipe Networks in COM > Base Objects > Pipe-Specific Ambient Settings -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-26F033E8-7FE2-4429-BD4C-146D070780E4.htm -->

# Pipe-Specific Ambient Settings

Ambient settings allow you to get and set the units and default property settings of pipe network objects as well as access the catalog of all pipe and structure parts held in the document. Ambient settings for a pipe document are held in the AeccPipeDocument.Settings property, an object of type AeccPipeSettingsRoot. AeccPipeSettingsRoot inherits all the properties of the AeccSettingsRoot class. 

Among the properties of AeccPipeSettingsRoot are InterferenceSettings, PipeSettings, and StructureSettings. Each of these properties consist of an AeccSettingsAmbient object, which describes the default units of measurement for interference, pipe, and structure objects. The AeccPipeSettingsRoot.PipeNetworkSettings property contains the name of the default styles for pipe and structure objects as well as the default label placement, units, and naming conventions for pipe networks as a whole.
    
    
    ' Get the default set of pipe rules used in this document.
    With oSettings.PipeNetworkSettings.RulesSettings
        Debug.Print "Using pipe rules:"; .PipeDefaultRules.Value
    End With
     
    ' Set the default units used for pipes in this document.
    With oSettings.PipeSettings.AmbientSettings
        .AngleSettings.Unit = aeccAngleUnitRadian
        .CoordinateSettings.Unit = aeccCoordinateUnitFoot
        .DistanceSettings.Unit = aeccCoordinateUnitFoot
    End With
    

The AeccPipeSettingsRoot object also has a PipeNetworkCommandsSettingsproperty, which contains properties that affect pipe network-related commands. Each sub-property contains an AmbientSettings property which describes the default units of measurement for interference, pipe, and structure objects, plus other properties specific to the command.
