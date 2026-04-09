<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Survey in COM > Figures > Creating a Figure Object -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-A4BAD428-0175-4696-BA9B-10B86D43FF96.htm -->

# Creating a Figure Object

A collection of all figures in the survey database are stored in the AeccSurveyProject.Figures property. New figures are made using the collection’s Create method.
    
    
    Dim oFigure As AeccSurveyFigure
    Set oFigure = oSurveyProject.Figures.Create("Figure_01")
