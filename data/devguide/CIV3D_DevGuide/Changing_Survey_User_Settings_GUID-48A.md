<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Survey in COM > Root Objects > Changing Survey User Settings -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-48A2D065-A81B-47FD-8F61-7F498933ED3C.htm -->

# Changing Survey User Settings

The survey document also provides access to the survey user settings object. User settings are not specific to a particular document but are tied to a particular user, and all documents a user creates or loads will use the same settings. Survey user settings manage the visibility and appearance of prism sites, backsight lines, foresight lines, and baselines. Survey user settings also control how network and figure previews are shown, and under what conditions points, figures, and observations are automatically erased or exported. These settings also allow you to determine or set which figure prefix database, equipment database, or item of equipment is currently in use. The survey user settings object is retrieved through the AeccSurveyDocument.GetUserSettings method, which returns an AeccSurveyUserSettings object. To apply any changes made to the user settings, pass the modified AeccSurveyUserSettings object to the AeccSurveyDocument.UpdateUserSettings method.
    
    
    Dim oUserSettings  As AeccSurveyUserSettings
    Set oUserSettings = oSurveyDocument.GetUserSettings
     
    ' Modify and examine the current settings.
    With oUserSettings
        .ShowBaseline = True
        Dim oColor As New AcadAcCmColor
        oColor.SetRGB 255, 165, 0 ' bright orange
        Set .BaselineColor = oColor
        .EraseAllFigures = False
        Debug.Print "Default layer:"; .DefaultFigureLayer
    End with
     
    ' Save the changes to the user settings object.
    oSurveyDocument.UpdateUserSettings oUserSettings
