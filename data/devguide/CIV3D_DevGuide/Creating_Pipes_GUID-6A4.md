<!-- Developer's Guide > API Developer's Guide > Pipe Networks > Pipes > Creating Pipes -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-6A41C6B7-3640-4F47-8125-60117A5DD1DF.htm -->

# Creating Pipes

Pipe objects represent the conduits of the pipe network. Pipes are created using the pipe network’s methods for creating either straight or curved pipes, AddLinePipe() and AddCurvePipe(). Both methods require you to specify a particular part family (using the ObjectId of a family) and a particular part size filter object as well as the geometry of the pipe. 

This sample creates a straight pipe between two hard-coded points using the first pipe family and pipe size filter it can find in the part list:
    
    
    [CommandMethod("AddPipe")]
    public void AddPipe()
    {
        CivilDocument doc = CivilApplication.ActiveDocument;
        Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
        using (Transaction ts = Application.DocumentManager.MdiActiveDocument.
            Database.TransactionManager.StartTransaction())
        {
            ObjectIdCollection oIdCollection = doc.GetPipeNetworkIds();
            // Get the first network in the document
            ObjectId objId = oIdCollection[0];
            Network oNetwork = ts.GetObject(objId, OpenMode.ForWrite) as Network;
            ed.WriteMessage("Pipe Network: {0}\n", oNetwork.Name);
            // Go through the list of part types and select the first pipe found
            ObjectId pid = oNetwork.PartsListId;
            PartsList pl = ts.GetObject(pid, OpenMode.ForWrite) as PartsList;
            ObjectId oid = pl["Concrete Pipe"];
            PartFamily pfa = ts.GetObject(oid, OpenMode.ForWrite) as PartFamily;
            ObjectId psize = pfa[0];
            LineSegment3d line = new LineSegment3d(new Point3d(30, 9, 0), new Point3d(33, 7, 0));
            ObjectIdCollection col = oNetwork.GetPipeIds();
            ObjectId oidNewPipe = ObjectId.Null;
            oNetwork.AddLinePipe(oid, psize, line, ref oidNewPipe, false);
            Pipe oNewPipe = ts.GetObject(oidNewPipe, OpenMode.ForRead) as Pipe;                
            ed.WriteMessage("Pipe created: {0}\n", oNewPipe.DisplayName);
            ts.Commit();
        }
        
    }
