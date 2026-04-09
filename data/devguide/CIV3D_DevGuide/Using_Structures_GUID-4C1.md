<!-- Developer's Guide > API Developer's Guide > Pipe Networks > Structures > Using Structures -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-4C1463D4-079D-409D-AD49-2560782CB208.htm -->

# Using Structures

To make the new structure a meaningful part of a pipe network, it must be connected to pipes in the network using the Structure.ConnectToPipe() method or pipes must be connected to it using the Pipe.ConnectToStructure() method. After a structure has been connected to a network, you can determine the pipes connected to it by using the ConnectedPipe property, which is a read-only collection of network parts. There are also methods and properties for setting and determining all types of physical measurements for the structure and for accessing collections of user-defined properties for custom descriptions of the structure.
