<!-- Developer's Guide > API Developer's Guide > Pipe Networks > Pipes > Using Pipes -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-405C06DF-520E-4E74-9182-CAC4AE679F7C.htm -->

# Using Pipes

To make a new pipe a meaningful part of a pipe network, it must be connected to structures or other pipes using the Pipe.ConnectToStructure() or Pipe.ConnectToPipe() methods, or structures must be connected to it using the Structure.ConnectToPipe() method. Connecting pipes together directly creates a new virtual Structure object to serve as the joint. If a pipe end is connected to a structure, it must be disconnected before attempting to connect it to a different structure. After a pipe has been connected to a network, you can determine the structures at either end by using the StartStructureId and EndStructureId properties. There are methods and properties for setting and determining the flow direction, getting all types of physical measurements, and for accessing collections of user-defined properties for custom descriptions of the pipe.
