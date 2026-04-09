<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Survey in COM > Figures -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-EF400B43-EE72-4A50-A0D1-8DAA3F6180F3.htm -->

# Figures

Figures are a group of connected lines and arcs that have meaning within a survey. A figure can represent a fence, building, road, parcel, or similar object. Unlike a normal polyline, a vertex in a figure can reference a survey point. If a referenced survey point is moved, vertices in the figure are moved as well. The first line or arc added to the figure sets the location all other lines and arcs will be drawn from. Each line and arc added to a figure is in turn based on the endpoint of the previous element. The position of the last endpoint can be determined from the read-only properties AeccSurveyFigure.LastPointX and AeccSurveyFigure.LastPointY.
