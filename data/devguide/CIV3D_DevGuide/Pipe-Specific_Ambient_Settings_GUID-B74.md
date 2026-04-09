<!-- Developer's Guide > API Developer's Guide > Pipe Networks > Base Objects > Pipe-Specific Ambient Settings -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-B74A9D15-F36C-4156-80BE-E7D6BF1FA9E8.htm -->

# Pipe-Specific Ambient Settings

Ambient settings allow you to get and set the units and default property settings of pipe network objects as well as access the catalog of all pipe and structure parts held in the document. Ambient settings for a pipe document are obtained from the CivilDocument.Settings.GetSettings() method, which returns an object inherited from SettingsAmbient. 

Among the classes that inherit from SettingsAmbient are SettingsPipe, SettingsPipeNetwork, and SettingsStructure. Each of these has properties that describe the default units of measurement for interference, pipe, and structure objects. The PipeSettingsRoot.PipeNetworkSettings property contains the name of the default styles for pipe and structure objects as well as the default label placement, units, and naming conventions for pipe networks as a whole.
    
    
    public void ShowPipeRules()
    {
        CivilDocument doc = CivilApplication.ActiveDocument;
        Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
        SettingsPipeNetwork oSettingsPipeNetwork = doc.Settings.GetSettings<SettingsPipeNetwork>() as SettingsPipeNetwork;
        ed.WriteMessage("Using pipe rules: {0}\n", oSettingsPipeNetwork.Rules.Pipe.Value);
        //  Set the default units used for pipes in this document.
        oSettingsPipeNetwork.Angle.Unit.Value = Autodesk.Civil.AngleUnitType.Radian;
        oSettingsPipeNetwork.Coordinate.Unit.Value = Autodesk.Civil.LinearUnitType.Foot;
        oSettingsPipeNetwork.Distance.Unit.Value = Autodesk.Civil.LinearUnitType.Foot;
    }
