<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Pipe Networks in COM > Pipes > Using Pipes -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-EFAC2C87-CC52-4672-AE2B-E8EC9C758798.htm -->

# Using Pipes

To make a new pipe a meaningful part of a pipe network, it must be connected to structures or other pipes using the AeccPipe.ConnectToStructure or AeccPipe.ConnectToPipe methods, or structures must be connected to it using the AeccStructure.ConnectToPipe method. Connecting pipes together directly creates a new virtual AeccStructure object to serve as the joint. If a pipe end is connected to a structure, it must be disconnected before attempting to connect it to a different structure. After a pipe has been connected to a network, you can determine the structures at either end by using the StartStructure and EndStructure properties or by using the Connections property, which is a read-only collection of network parts. There are methods and properties for setting and determining the flow direction, getting all types of physical measurements, and for accessing collections of user-defined properties for custom descriptions of the pipe.
    
    
    ' Given a pipe and a structure, join the second endpoint
    ' of the pipe to the structure.
    oPipe.ConnectToStructure aeccPipeEnd, oStructure
     
    ' Set the flow direction for the pipe.
    oPipe.FlowDirectionMethod = aeccPipeFlowDirectionMethodBySlope
     
    ' Add a custom property to the pipe and assign a value.
    Call oPipe.ParamsLong.Add("Custom", 9.2)
    Debug.Print "Custom prop:"; oPipe.ParamsLong.Value("Custom")
