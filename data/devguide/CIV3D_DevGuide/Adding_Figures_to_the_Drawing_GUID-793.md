<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Survey in COM > Figures > Adding Figures to the Drawing -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-79341C08-5C06-40BD-9590-0C9D54DD6DB4.htm -->

# Adding Figures to the Drawing

Adding lines and arcs to a figure changes the survey database but does not automatically change the drawing. After you are done adding elements to the figure, call the AeccSurveyFigure.AddToDrawing method to create AutoCAD elements that correspond to the figure. This is equivalent to the Autodesk Civil 3D command “Insert Into Drawing”.
