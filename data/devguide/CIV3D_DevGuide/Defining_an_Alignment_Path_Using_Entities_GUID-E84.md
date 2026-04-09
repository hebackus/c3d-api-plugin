<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Alignments in COM > Basic Alignment Operations > Defining an Alignment Path Using Entities -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-E84FB5AA-03C4-4D6B-82E0-42D5FD2A3E36.htm -->

# Defining an Alignment Path Using Entities

An alignment is made up of a series of _entities_ , which are individual lines, curves, and spirals that make up the path of an alignment. A collection of entities is held in the AeccAlignment.Entities collection. This collection has a wide array of methods for creating new entities. 

The following code sample demonstrates some of the entity creation methods:
    
    
    ' Define the points used to create the entities.
    Dim point1(0 To 2) As Double
    Dim point2(0 To 2) As Double
    Dim point3(0 To 2) As Double
    point1(0) = 200: point1(1) = 800: point1(2) = 0
    point2(0) = 600: point1(1) = 400: point1(2) = 0
    point3(0) = 1000: point1(1) = 800: point1(2) = 0
     
    ' Create a line segment entity that connects two points.
    Dim oAlignmentTangent As AeccAlignmentTangent
    Set oAlignmentTangent = oAlignment.Entities _
      .AddFixedLine1(point1, point2)
     
    ' Print the length of the line segment.
    Debug.Print oAlignmentTangent.Length
     
    ' Create a curve entity that connects the second endpoint 
    ' of the fixed line to another point. The radius of the
    ' curve depends on the direction of the fixed line and the
    ' location of the second endpoint.
    Dim oAlignmentArc As AeccAlignmentArc
    Set oAlignmentArc = oAlignment.Entities _
      .AddFloatingCurve6(oAlignmentTangent.id, point3)
     
    ' Print the angle of direction at the second endpoint.
    Debug.Print oAlignmentArc.EndDirection
