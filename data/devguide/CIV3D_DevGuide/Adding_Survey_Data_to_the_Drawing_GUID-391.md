<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Survey in COM > Survey Network > Adding Survey Data to the Drawing -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-3911AC0B-19B4-4C14-B33A-52891040B4BD.htm -->

# Adding Survey Data to the Drawing

Adding elements or modifying information in a survey network object changes the survey database but does not automatically change the drawing. After you are done adding points, directions, and other elements that have a graphical element, call the AeccSurveyNetwork.AddToDrawing method to create AutoCAD elements that correspond to the survey network data. This is equivalent to the Autodesk Civil 3D command “Insert Into Drawing”.
    
    
    oSurveyNetwork.AddToDrawing
