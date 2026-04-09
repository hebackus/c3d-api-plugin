<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Survey in COM > Root Objects > Adjusting Survey Project Settings -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-1B5A48E5-716A-438F-B5E4-FBB20B24CDF8.htm -->

# Adjusting Survey Project Settings

A survey project has a group of properties accessed through the survey project settings object. Survey project settings define what measurement units are used, what angle types are used, and the precision of each measurement. It records what kinds of adjustments are made to observations, and the types and accuracy of traverse analyses and angle balancing. It also has methods for converting between metric units and the units of the ambient settings, and between easting and northing and longitude and latitude. The project settings object is retrieved through the AeccSurveyProject.GetProjectSettings method, which returns an AeccSurveyProjectSettings object. To apply any changes made to the project settings, pass the modified AeccSurveyProjectSettings object to the AeccSurveyProject.UpdateProjectSettings method.
    
    
    Dim oProjectSettings As AeccSurveyProjectSettings
    Set oProjectSettings = oSurveyProject.GetProjectSettings()
     
    ' Modify and examine the current settings.
    With oProjectSettings
       .AngleType = aeccSurveyAngleTypeAzimuth
       Debug.Print "Sea level correction? :"; .SeaLevelCorrection
    End With
     
    ' Save the changes to the project settings object.
    oSurveyProject.UpdateProjectSettings oProjectSettings
