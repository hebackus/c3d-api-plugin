<!-- Developer's Guide > API Developer's Guide > Rail > Finding the Track Distance between Two Rails -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-749BD054-DCAA-4D73-AB87-2BC7A8A7C8EB.htm -->

# Finding the Track Distance between Two Rails

The API detailed below enables the determination of clearance between the left or right rails of distinct alignments. While dynamic clearance in railway engineering is subject to various factors like radius and speed, the API provides a valuable static measurement. This measurement is crucial for preliminary design and feasibility studies, allowing the assessment of space availability for infrastructure elements such as signals and ensuring adequate clearance between tracks. 

The following API gets the distance between 2 tracks based on centerline alignments. 

|  **Option 1** **PrimaryAlignmentToSecondaryRail**. A line perpendicular to the left/right track lines of the primary alignment. The line intersects with left or right track line of secondary alignment. The target station on the secondary alignment is the intersection point's projection station on the secondary alignment. Track distance is the minimum distance between two intersection points that the line intersects with left/right track lines of primary alignment and left/right track lines of secondary alignment.   
---|---  
**Option 2** **PrimaryRailToSecondaryAlignment**. First get the primary alignment's left/right track line points by the primary alignment's station and gauge width. The target station on the secondary alignment is a projection station of the primary alignment's left/right track line point on the secondary alignment. Track distance is the minimum distance between the primary alignment's left/right track line points and the intersection points of projection lines with the left/right track lines of the secondary alignment.   
**Option 3** **AlignmentToAlignmentMinusGauge**. A line perpendicular to the left/right track lines of the primary alignment. The line intersects with the left or right track's line of secondary alignment. The target station on the secondary alignment is the station where the line intersects with the secondary alignment. Track distance is the minimum distance between two intersection points of the line with the left/right track lines of primary alignment and left/right track lines of secondary alignment.
