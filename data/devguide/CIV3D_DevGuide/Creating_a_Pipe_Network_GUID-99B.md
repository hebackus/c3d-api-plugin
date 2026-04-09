<!-- Developer's Guide > API Developer's Guide > Pipe Networks > Base Objects > Creating a Pipe Network -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-99B14755-ACCD-47F9-9B49-4D3950ACC725.htm -->

# Creating a Pipe Network

A pipe network is a set of interconnected or related parts. The collection of all pipe networks is returned by the CivilDocument.GetPipeNetworkIds() method. A pipe network, an object of type Network, contains the collection of pipes and the collection of structures which make up the network. Network also contains the method FindShortestNetworkPath() for determining the path between two network parts. 

The Network.ReferenceSurfaceId is used primarily for Pipe Rules. For example, you can have a rule that places the structure rim at a specified elevation from the surface. 
    
    
    Public Function CreatePipeNetwork() As Boolean
        Dim trans As Transaction = tm.StartTransaction()
        Dim oPipeNetworkIds As ObjectIdCollection
        Dim oNetworkId As ObjectId
        Dim oNetwork As Network
        oNetworkId = Network.Create(g_oDocument, NETWORK_NAME)
        ' get the network
        Try
            oNetwork = trans.GetObject(oNetworkId, OpenMode.ForWrite)
        Catch
            CreatePipeNetwork = False
            Exit Function
        End Try
        '
        'Add pipe and Structure
        ' Get the Networks collections
        oPipeNetworkIds = g_oDocument.GetPipeNetworkIds()
        If (oPipeNetworkIds Is Nothing) Then
            MsgBox("There is no PipeNetwork Collection." + Convert.ToChar(10))
            ed.WriteMessage("There is no PipeNetwork Collection." + Convert.ToChar(10))
            CreatePipeNetwork = False
            Exit Function
        End If
        Dim oPartsListId As ObjectId = g_oDocument.Styles.PartsListSet(PARTS_LIST_NAME) 'Standard PartsList
        Dim oPartsList As PartsList = trans.GetObject(oPartsListId, OpenMode.ForWrite)
        Dim oidPipe As ObjectId = oPartsList("Concrete Pipe SI")
        Dim opfPipe As PartFamily = trans.GetObject(oidPipe, OpenMode.ForWrite)
        Dim psizePipe As ObjectId = opfPipe(0)
        Dim line As LineSegment3d = New LineSegment3d(New Point3d(30, 9, 0), New Point3d(33, 7, 0))
        Dim oidNewPipe As ObjectId = ObjectId.Null
        oNetwork.AddLinePipe(oidPipe, psizePipe, line, oidNewPipe, True)
        Dim oidStructure As ObjectId = oPartsList("CMP Rectangular End Section SI")
        Dim opfStructure As PartFamily = trans.GetObject(oidStructure, OpenMode.ForWrite)
        Dim psizeStructure As ObjectId = opfStructure(0)
        Dim startPoint As Point3d = New Point3d(30, 9, 0)
        Dim endPoint As Point3d = New Point3d(33, 7, 0)
        Dim oidNewStructure As ObjectId = ObjectId.Null
        oNetwork.AddStructure(oidStructure, psizeStructure, startPoint, 0, oidNewStructure, True)
        oNetwork.AddStructure(oidStructure, psizeStructure, endPoint, 0, oidNewStructure, True)
        ed.WriteMessage("PipeNetwork created" + Convert.ToChar(10))
        trans.Commit()
        CreatePipeNetwork = True
    End Function ' CreatePipeNetwork
