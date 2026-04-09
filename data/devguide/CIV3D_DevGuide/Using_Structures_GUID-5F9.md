<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Pipe Networks in COM > Structures > Using Structures -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-5F9A3217-CE7F-497D-93CE-2BA3D2D6E654.htm -->

# Using Structures

To make the new structure a meaningful part of a pipe network, it must be connected to pipes in the network using the AeccStructure.ConnectToPipe method or pipes must be connected to it using the AeccPipe.ConnectToStructure method. After a structure has been connected to a network, you can determine the pipes connected to it by using the Connections property, which is a read-only collection of network parts. There are also methods and properties for setting and determining all types of physical measurements for the structure and for accessing collections of user-defined properties for custom descriptions of the structure.
    
    
    ' Given a pipe and a structure, join the second endpoint
    ' of the pipe to the structure.
    oStructure.ConnectToPipe oPipeNew, aeccPipeEnd
     
    ' Determine flow directions from all pipes connected
    ' to a structure.
    Dim i As Integer
    For i = 0 To oStructure.ConnectedPipesCount - 1
       If (oStructure.IsConnectedPipeFlowingIn(i) = True) Then
          Debug.Print "Pipe "; i; " flows into structure"
       Else
          Debug.Print "Pipe "; i; " does not flow into structure"
       End If
    Next i
