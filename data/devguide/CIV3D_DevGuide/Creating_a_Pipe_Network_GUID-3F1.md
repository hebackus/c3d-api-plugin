<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Pipe Networks in COM > Base Objects > Creating a Pipe Network -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-3F133FCD-76DF-4979-AFE9-A45865026BE2.htm -->

# Creating a Pipe Network

A pipe network is a set of interconnected or related parts. The collection of all pipe networks is held in the AeccPipeDocument.PipeNetworks property. A pipe network, an object of type AeccPipeNetwork, contains the collection of pipes and the collection of structures which make up the network. AeccPipeNetwork also contains the method AeccPipeNetwork.FindShortestNetworkPath for determining the path between two network parts. 

The AeccPipeNetwork.ReferenceAlignment is used by pipe and structure label properties. For example, you can create a label that shows the station and offset from the alignment. The AeccPipeNetwork.ReferenceSurface is used primarily for Pipe Rules. For example, you can have a rule that places the structure rim at a specified elevation from the surface. Labels may also refer to the ReferenceSurface property.
    
    
    ' Get the collection of all networks.
    Dim oPipeNetworks as AeccPipeNetworks
    Set oPipeNetworks = oPipeDocument.PipeNetworks
     
    ' Create a new pipe network
    Set oPipeNetwork = oPipeNetworks.Add("Network Name")
