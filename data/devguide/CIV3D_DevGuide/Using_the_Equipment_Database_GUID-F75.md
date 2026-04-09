<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Survey in COM > Root Objects > Using the Equipment Database -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-F75EEA62-28CF-4201-A6E3-BAA4E6470E3C.htm -->

# Using the Equipment Database

The equipment database contains a list of equipment used to gather surveying data. The information about each item of equipment is used in least squares and other computations. A collection of all equipment lists is contained in the AeccSurveyDocument.EquipmentDatabases property. Each equipment database is a collection of individual items of equipment. An equipment database is an object of type AeccSurveyEquipmentDatabase, and contains methods for searching the list of equipment and for copying lists from other databases.

Each item of equipment is represented by an AeccSurveyEquipment object, which contains properties describing aspects of the equipment, including the name and description, how the instrument measures angles, the unit types for angle and distance, Electronic Distance Meter settings, prism accuracy and offset, and the accuracy of the instrument.

This sample program displays selected information about each equipment item in the document’s database:
    
    
    Dim oEquipDatabases As AeccSurveyEquipmentDatabases
    Dim oEquipDatabase As AeccSurveyEquipmentDatabase
    Dim oEquipment As AeccSurveyEquipment
     
    Set oEquipDatabases = oSurveyDocument.EquipmentDatabases
    For Each oEquipDatabase In oEquipDatabases
       Debug.Print "Database: "; oEquipDatabase.Name
       Debug.Print
     
       For Each oEquipment In oEquipDatabase
       With oEquipment
          Debug.Print "----"
          Debug.Print "Item: "; .Name; "   Id: "; .Id
          Debug.Print " Description: "; .Description
          Debug.Print " Angle Type: "; .AngleType
          Debug.Print " Angle Unit: "; .AngleUnit
          Debug.Print " Azimuth Std: "; .AzimuthStandard
          Debug.Print " Wave Constant: "; .CarrierWaveConstant
          Debug.Print " Center Standard: "; .CenterStandard
          Debug.Print " Circle Standard: "; .CircleStandard
          Debug.Print " Coordinate Std: "; .CoordinateStandard
          Debug.Print " Distance Unit: "; .DistanceUnit
          Debug.Print " Edm Error: "; .EdmMmError; "mm"
          Debug.Print " Edm Error: "; .EdmPpmError; "ppm"
          Debug.Print " Edm Offset: "; .EdmOffset
          Debug.Print " Elevation Std: "; .ElevationStandard
          Debug.Print " H Collimation: "; .HorizontalCollimation
          Debug.Print " Is Prism Tilted: "; CStr(.IsTiltedPrism)
          Debug.Print " Measuring Device: "; .MeasuringDevice
          Debug.Print " Pointing Std: "; .PointingStandard
          Debug.Print " Prism Constant: "; .PrismConstant
          Debug.Print " Prism Offset: "; .PrismOffset
          Debug.Print " Prism Std: "; .PrismStandard
          Debug.Print " Revision: "; .Revision
          Debug.Print " Target Std: "; .TargetStandard
          Debug.Print " Theodolite Std: "; .TheodoliteStandard
          Debug.Print " Vertical Angle Type: "; .VerticalAngleType
          Debug.Print " V Collimation: "; .VerticalCollimation
          Debug.Print
       End With
       Next
    Next
