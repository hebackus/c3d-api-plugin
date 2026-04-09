<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Survey in COM > Figures > Adding Arcs to a Figure -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-0B5554E5-D1C3-4E6C-B139-1D0EBEFFA499.htm -->

# Adding Arcs to a Figure

Each arc added to a figure is drawn from the endpoint of the previous line or arc. AddArc adds a segment of a circle to the figure to the specified point location. The shape of the arc is defined by the Radius, Bulge, and CenterX and CenterY parameters. The Bulge parameter defines what fraction of a circle the arc comprises. If the Radius parameter is zero or negative the arc is curved in the clockwise direction, otherwise the arc is curved in the counter-clockwise direction. An optional parameter can specify a survey point to reference so that whenever it changes the arc endpoint will change as well.
    
    
    ' Create a clockwise arc comprising of roughly half a circle 
    ' that ends at survey point 3001.
    oFigure.AddArc 10, 1.7, 0, 0, oPoint1.Easting, _
      oPoint1.Northing, , 3001
