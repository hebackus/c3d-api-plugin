<!-- Developer's Guide > API Developer's Guide > Alignments > Basic Alignment Operations > Defining an Alignment Path Using Entities -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-EC4774B6-C7E9-453E-9382-2A3EE3B2A575.htm -->

# Defining an Alignment Path Using Entities

An alignment is made up of a series of _entities_ , which are individual lines, curves, and spirals that make up the path of an alignment. A collection of entities is held in the Alignment::Entities property, which is an AlignmentEntityCollection object. This collection has a wide array of methods for creating new entities. 

Here’s a short code snippet that illustrates one of the methods for adding a FixedCurve entitiy to an alignment’s Entities collection:
    
    
    Int32 previousEntityId = 0;
    Point3d startPoint = new Point3d(8800.7906, 13098.1946, 0.0000);
    Point3d middlePoint = new Point3d(8841.9624, 13108.6382, 0.0000);
    Point3d endPoint = new Point3d(8874.2664, 13089.3333, 0.0000);
    AlignmentArc retVal = myAlignment.Entities.AddFixedCurve(previousEntityId, startPoint, middlePoint, endPoint);
