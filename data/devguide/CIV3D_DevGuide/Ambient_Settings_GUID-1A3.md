<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Corridors in COM > Root Objects > Ambient Settings -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-1A34443C-58BF-4162-8606-FDE764A87945.htm -->

# Ambient Settings

Ambient settings allow you to get and set the unit and default property settings of roadway objects. Ambient settings for a corridor document are held in the AeccRoadwayDocument.Settings property, an object of type AeccRoadwaySettingsRoot. AeccRoadwaySettingsRoot inheirits all the properties of the AeccSettingsRoot class from which it is derived. 

The roadway-specific properies of AeccRoadwaySettingsRoot let you adjust the settings for corridors, assemblies, subassemblies, and quantity takeoffs: 

## Corridor Ambient Settings

The corridor ambient settings object allows you to set the default name templates and default styles for corridor-related objects. The name templates allow you to set how new corridors, corridor surfaces, profiles from feature lines, or alignments from feature lines are named. Each template can use elements from the following property fields: 

Valid property fields for AeccSettingsCorridor.NameTemplate   
---  
<[Corridor First Assembly(CP)]>  
<[Corridor First Baseline(CP)]>  
<[Corridor First Profile(CP)]>  
<[Next Counter(CP)]>  
  
... for AeccSettingsCorridor.CorridorSurfaceNameTemplate   
---  
<[Corridor Name(CP)]>  
<[Next Corridor Surface Counter(CP)]>  
  
...for AeccSettingsCorridor.ProfileFromFeatureLineNameTemplate   
---  
<[Next Counter(CP)]>  
  
... for AeccSettingsCorridor.AlignmentFromFeatureLineNameTemplate   
---  
<[Corridor Baseline Name(CP)]>  
<[Corridor Feature Code(CP)]>  
<[Corridor Name(CP)]>  
<[Next Counter(CP)]>  
<[Profile Type]>  
  
This sample sets the corridor name template:
    
    
    ' Get the ambient settings root object.
    Dim oRoadwaySettings  As AeccRoadwaySettingsRoot
    Set oRoadwaySettings = oRoadwayDocument.Settings
     
    ' Set the template so that new corridors are named "Corridor"
    ' followed by a unique number followed by the name of the
    ' corridor's first assembly in parenthesis. 
    oRoadwaySettings.CorridorSettings.NameTemplate = _
      "Corridor <[Next Counter(CP)]>(<[Corridor First Assembly(CP)]>)"
    

Default styles are set through the AeccSettingsCorridor.StyleSettings property. The styles for corridor alignments, alignment labels, code sets, surfaces, feature lines, profiles, profile labels, and slope pattern are accessed through a series of string properties.

This sample sets the style of alignments in a corridor to the first alignment style in the document’s collection of styles:
    
    
    ' Get a reference to the corridor settings object.
    Dim oSettingsCorridor As AeccSettingsCorridor
    Set oSettingsCorridor = oRoadwayDocument.Settings.CorridorSettings
     
    ' Get the name of the first alignment style in the collection.
    Dim sName As String
    sName = oRoadwayDocument.AlignmentStyles.Item(0).Name
     
    ' Assign the name to alignment style property.
    oSettingsCorridor.StyleSettings.AlignmentStyle.Value = sName
    

## Assembly Ambient Settings

The assembly ambient settings object allows you to set the default name templates and default styles for assemblies. The name templates allow you to set how new assemblies, offset assemblies, and assembly groups are named. Each template can use elements from the following property fields: 

Valid property fields for AeccSettingsAssembly.NameTemplate   
---  
<[Next Counter(CP)]>  
  
... for AeccSettingsAssembly.OffsetNameTemplate   
---  
<[Corridor Name(CP)]>  
  
...for AeccSettingsAssembly.GroupNameTemplate   
---  
<[Next Counter(CP)]>  
  
Default styles are set through the AeccSettingsCorridor.StyleSettings property. The styles for assemblies and code sets are accessed through string properties.

## Subassembly Ambient Settings

The subassembly ambient settings object allows you to set the default name templates and default styles for subassembly objects. The name templates allow you to set how subassemblies created from entities and subassemblies create from macros are named. Each template can use elements from the following property fields: 

... for AeccSettingsSubassembly.CreateFromEntitiesNameTemplate   
---  
<[Macro Short Name(CP)]>  
<[Next Counter(CP)]>  
<[Subassembly Local Name(CP)]>  
<[Subassembly Side]>  
  
... for AeccSettingsSubassembly.CreateFromMacroNameTemplate  
---  
<[Macro Short Name(CP)]>  
<[Next Counter(CP)]>  
<[Subassembly Local Name(CP)]>  
<[Subassembly Side]>  
  
The name of the default code style set is accessed through the AeccSettingsSubassembly.CodeSetStyle string property. 

Each of these settings properties also contain a standard AmbientSettings property of type AeccSettingsAmbient for setting the default units of measurement.
