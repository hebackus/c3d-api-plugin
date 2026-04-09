<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Survey in COM > Figures > Figures and Autodesk Civil 3D -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-037A2CC7-67C9-40B9-B69C-1FCADFCAA56F.htm -->

# Figures and Autodesk Civil 3D

A figure can influence Autodesk Civil 3D objects such as parcels and TIN surfaces. If the AeccSurveyFigure.IsLotLine property is set to True, then parcel segments are created for each figure line and arc when the figure is added to the drawing. If any set of parcel segments creates closed figures, then a parcel is formed. You can assign the parcel segments to a particular site by setting the AeccSurveyFigure.Site property - otherwise, a new site named “Survey Site” is created automatically. The figure still remains in the survey database, and deleting the figure removes all associated parcel segments from the drawing. 

A figure can also form a breakline that defines how surfaces are triangulated. This is accomplished by setting the AeccSurveyFigure.IsBreakline property to True
