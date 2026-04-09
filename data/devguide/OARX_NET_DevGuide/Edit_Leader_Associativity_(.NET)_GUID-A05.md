<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Dimensions and Tolerances (.NET) > Create Leaders and Annotation (.NET) > Edit Leader Associativity (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-A05C3784-4CCB-4F95-9D31-BAB45237A9B2.htm -->

# Edit Leader Associativity (.NET)

Except for the associativity relation between the leader and annotation, the leader and its annotation are entirely separate objects in your drawing. Editing of the leader does not affect the annotation, and editing of the annotation does not affect the leader. 

Although text annotation is created using the DIMCLRT, DIMTXT, and DIMTXSTY system variables to define its color, height, and style, it cannot be changed by these system variables because it is not a true dimension object. Text annotation must be edited the same way as any other MText object. 

Use the Evaluate method to evaluate the relation of the leader to its associated annotation. This method will update the leader geometry if necessary.
