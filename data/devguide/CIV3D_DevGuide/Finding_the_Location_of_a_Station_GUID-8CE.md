<!-- Developer's Guide > API Developer's Guide > Alignments > Stations > Finding the Location of a Station -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-8CEA16C1-D0F0-44A6-98B0-5120F2A69CB0.htm -->

# Finding the Location of a Station

You can find the point coordinates (northing and easting) of a station and offset on an alignment using the Alignment::PointLocation() method. The simplest version of the method takes a station and offset, and returns a northing and easting (as ref parameters). 

Another version of this method takes a station, offset, and tolerance, and returns a northing, easting, and bearing (as ref parameters). The tolerance determines on which alignment entity the point is returned. If the tolerance is greater than the desired station minus the station at the alignment entity transition, the point will be reported on that entity. For example, consider an alignment made up of a tangent (length 240) and curve (length 260). Looking for the location of station 400, with tolerance = 0, will find a point on the curve. However, a tolerance of 200 will cause the method to report a point on the tangent, because 400 - 240 < 200.
