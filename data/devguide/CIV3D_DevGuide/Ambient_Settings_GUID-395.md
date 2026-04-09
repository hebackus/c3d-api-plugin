<!-- Developer's Guide > API Developer's Guide > Corridors > Root Objects > Ambient Settings -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-395FEF00-6D53-486C-AAA8-D2F0591B11BA.htm -->

# Ambient Settings

Ambient settings allow you to get and set the unit and default property settings of roadway objects. Ambient settings for a corridor are accessed with the SettingsCorridor object returned by CivilDocument.Settings.GetFeatureSettings() method. 

## Corridor Ambient Settings

The corridor ambient settings object allows you to set the default name formats and default styles for corridor-related objects. The name templates allow you to set how new corridors, corridor surfaces, profiles from feature lines, or alignments from feature lines are named. Each format can use elements from the following property fields: 

Valid property fields for SettingsCorridor.SettingsNameFormat.Corridor  
---  
<[Corridor First Assembly(CP)]>  
<[Corridor First Baseline(CP)]>  
<[Corridor First Profile(CP)]>  
<[Next Counter(CP)]>  
  
... for SettingsCorridor.SettingsNameFormat.CorridorSurface   
---  
<[Corridor Name(CP)]>  
<[Next Corridor Surface Counter(CP)]>  
  
...for SettingsCorridor.SettingsNameformat.ProfileFromFeatureLine   
---  
<[Next Counter(CP)]>  
  
... for SettingsCorridor.SettingsNameFormat.AlignmentFromFeatureLine   
---  
<[Corridor Baseline Name(CP)]>  
<[Corridor Feature Code(CP)]>  
<[Corridor Name(CP)]>  
<[Next Counter(CP)]>  
<[Profile Type]>  
  
This sample sets the corridor name format:
    
    
    // Get the Corridor ambient settings root object
    CivilDocument doc = CivilApplication.ActiveDocument;
    Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
    SettingsCorridor oCorridorSettings = doc.Settings.GetFeatureSettings<SettingsCorridor>() as SettingsCorridor;
    // Set the template so new corridors are named "Corridor"
    // followed by a unique number followed by the name of the
    // corridor's first assembly in parenthesis. 
    oCorridorSettings.NameFormat.Corridor.Value = "Corridor <[Next Counter(CP)]>(<[Corridor First Assembly(CP)]>)";
    

Default styles are set through the SettingsCorridor.StyleSettings property. The styles for corridor alignments, alignment labels, code sets, surfaces, feature lines, profiles, profile labels, and slope pattern are accessed through a series of string properties.

This sample sets the style of alignments in a corridor to the first alignment style in the document’s collection of styles:
    
    
    using (Transaction ts = Application.DocumentManager.MdiActiveDocument.
        Database.TransactionManager.StartTransaction())
    {
        // Get the name of the first alignment style in the collection.
        ObjectId alignId = doc.Styles.AlignmentStyles[0];
        Alignment oAlignment = ts.GetObject(alignId, OpenMode.ForRead) as Alignment;
        // Assign the name to alignment style property.
        oCorridorSettings.Styles.Alignment.Value = oAlignment.Name;
    }
    

## Assembly Ambient Settings

The assembly ambient settings object allows you to set the default name formats and default styles for assemblies. The name formats allow you to set how new assemblies, offset assemblies, and assembly groups are named. Each format can use elements from the following property fields: 

Valid property fields for SettingsAssembly.NameFormat.Assembly   
---  
<[Next Counter(CP)]>  
  
... for SettingsAssembly.NameFormat.Offset  
---  
<[Corridor Name(CP)]>  
  
...for SettingsAssembly.NameFormat.Group   
---  
<[Next Counter(CP)]>  
  
## Subassembly Ambient Settings

The subassembly ambient settings object allows you to set the default name formats and default styles for subassembly objects. The name formats allow you to set how subassemblies created from entities and subassemblies created from macros are named. Each format can use elements from the following property fields: 

... for SettingsSubassembly.SettingsNameFormat.CreateFromEntities   
---  
<[Macro Short Name(CP)]>  
<[Next Counter(CP)]>  
<[Subassembly Local Name(CP)]>  
<[Subassembly Side]>  
  
... for SettingsSubassembly.SettingsNameFormat.CreateFromMacro  
---  
<[Macro Short Name(CP)]>  
<[Next Counter(CP)]>  
<[Subassembly Local Name(CP)]>  
<[Subassembly Side]>  
  
Note:

The name of the default code style set cannot be set with the .NET API.
