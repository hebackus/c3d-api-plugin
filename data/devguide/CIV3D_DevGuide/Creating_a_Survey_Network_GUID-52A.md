<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Survey in COM > Survey Network > Creating a Survey Network -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-52A3A7C1-D9BF-4C9E-9F85-A236EC37CF9D.htm -->

# Creating a Survey Network

Survey networks are created through the Create method of the AeccSurveyProject.Networks collection.
    
    
    Dim oSurveyNetwork As AeccSurveyNetwork
    Set oSurveyNetwork = oSurveyProject.Networks.Create("Net_01")
