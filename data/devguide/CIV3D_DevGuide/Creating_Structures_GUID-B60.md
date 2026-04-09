<!-- Developer's Guide > API Developer's Guide > Pipe Networks > Structures > Creating Structures -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-B6004894-1E68-4818-B549-3DAA09BB9B4A.htm -->

# Creating Structures

Structures represent physical objects such as manholes, catch basins, and headwalls. Logically, structures are used as connections between pipes at pipe endpoints. In cases where two pipes connect directly, an Structure object not representing any physical object is still created to serve as the joint. Any number of pipes can connect with a structure. Structures are represented by objects of type Structure, which are created by using the AddStructure() method of Network.

See the code sample in [Creating a Pipe Network](<GUID-99B14755-ACCD-47F9-9B49-4D3950ACC725.htm>) for an example of how to call this method.
