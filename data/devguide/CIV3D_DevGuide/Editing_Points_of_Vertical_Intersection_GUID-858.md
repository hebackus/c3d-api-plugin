<!-- Developer's Guide > API Developer's Guide > Profiles > Profiles > Editing Points of Vertical Intersection -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-858970CB-26AD-4B6B-8209-FE61CCDEECA4.htm -->

# Editing Points of Vertical Intersection

The point where two adjacent tangents would cross (whether they actually cross or not) is called the “point of vertical intersection”, or “PVI.” This location can be useful for editing the geometry of a profile because this one point controls the slopes of both tangents and any curve connecting them. The collection of all PVIs in a profile is contained in the Profile.PVIs property. This collection lets you access, add, and remove PVIs from a profile, which can change the position and number of entities that make up the profile. Individual PVIs (type ProfilePVI) do not have a name or id, but are instead identified by a particular station and elevation. The collection methods ProfilePVICollection.GetPVIAt and ProfilePVICollection.RemoveAt either access or delete the PVI closest to the station and elevation parameters so you do not need the exact location of the PVI you want to modify.

This sample identifies the PVI closest to a specified point. It then adds a new PVI to the profile created in the [Creating a Profile Using Entities](<GUID-409176A7-99F7-462A-A2E0-30449957CAB6.htm>) topic and adjusts its elevation.
    
    
    [CommandMethod("EditPVI")]
    public void EditPVI()
    {
        doc = CivilApplication.ActiveDocument;
     
        Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
        using (Transaction ts = Application.DocumentManager.MdiActiveDocument.Database.TransactionManager.StartTransaction())
        {
            // get first profile of first alignment in document
            ObjectId alignID = doc.GetAlignmentIds()[0];
            Alignment oAlignment = ts.GetObject(alignID, OpenMode.ForRead) as Alignment;
            Profile oProfile = ts.GetObject(oAlignment.GetProfileIds()[0], OpenMode.ForRead) as Profile;
     
            // check to make sure we have a profile:
            if (oProfile == null)
            {
                ed.WriteMessage("Must have at least one alignment with one profile");
                return;
            }
            //  Find the PVI close to station 1000 elevation -70.
            ProfilePVI oProfilePVI = oProfile.PVIs.GetPVIAt(1000, -70);
            ed.WriteMessage("PVI closest to station 1000 is at station: {0}", oProfilePVI.Station);
            // Add another PVI and slightly adjust its elevation.
            oProfilePVI = oProfile.PVIs.AddPVI(607.4, -64.3);
            oProfilePVI.Elevation -= 2.0;
     
            ts.Commit();
        }
    }
