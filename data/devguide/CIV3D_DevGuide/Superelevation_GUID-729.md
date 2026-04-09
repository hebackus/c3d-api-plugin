<!-- Developer's Guide > API Developer's Guide > Alignments > Stations > Superelevation -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-72983BFC-D754-4423-932B-7395526C20FE.htm -->

# Superelevation

Another setting that can be applied to certain stations of an alignment is the superelevation, used to adjust the angle of roadway section components for corridors based on the alignment. The inside and outside shoulders and road surfaces can be adjusted for both the left and right sides of the road. 

Note:

The Superelevation feature was substantially changed in Autodesk Civil 3D 2011, and the API has also changed. The Alignment::SuperelevationData property and Alignment::SuperElevationAtStation() method have been removed. Existing code should be updated to use the new API, and access superelevation via Alignment::SuperelevationCurves, Alignment::SuperelevationCriticalStations, and SuperelevationCriticalStationCollection::GetCriticalStationAt(). 

The superelevation data for an alignment is divided into discrete curves, called superelevation curves, and each superelevation curve contains transition regions where superelevation transitions from normal roadway to full superelevation and back (with separate regions for transition in, and transition out of superelvation). These regions are defined by “critical stations”, or stations where there is a transition in the roadway cross-section. The collection of superelevation curves for an alignment is accessed with the Alignment::SuperelevationCurves property, while all critical stations for all curves is accessed with the Alignment::SuperelevationCriticalStations property. The SuperelevationCurves collection is empty if superelevation curves have not been added to the alignment (either manually, or calculated by the Superelevation Wizard in the user interface). The SuperelevationCriticalStations collection contains default entites for the start and end stations of the Alignment if no superelevation data has been calculated for the curves. 

An individual SuperelevationCriticalStation can be accessed through the Alignment::SuperelevationCriticalStations::GetCriticalStationAt() method. 

In this code snippet, the collection of superelevation curves for an alignment is iterated, and information about each critical station in each curve is printed out. Note that you must specify the cross segment type to get either the slope or smoothing length, but you may not know which segment types are valid for the critical station. In this snippet, the code attempts to get all segment types, and silently catches the InvalidOperationException exception for invalid types. 
    
    
    [CommandMethod("GetSECurves")]
    public void GetSECurves()
    {
        doc = CivilApplication.ActiveDocument;
        Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
        using (Transaction ts = Application.DocumentManager.MdiActiveDocument.Database.TransactionManager.StartTransaction())
        {
            // get first alignment:
            ObjectId alignID = doc.GetAlignmentIds()[0];
            Alignment myAlignment = ts.GetObject(alignID, OpenMode.ForRead) as Alignment;
            if (myAlignment.SuperelevationCurves.Count < 1)
            {
                ed.WriteMessage("You must calculate superelevation data.\n");
                return;
            }
            foreach (SuperelevationCurve sec in myAlignment.SuperelevationCurves)
            {
                ed.WriteMessage("Name: {0}\n", sec.Name);
                ed.WriteMessage("  Start: {0} End: {1}\n", sec.StartStation, sec.EndStation);
                foreach (SuperelevationCriticalStation sest in sec.CriticalStations)
                {
                    ed.WriteMessage("   Critical station: {0} {1} {2}\n", sest.TransitionRegionType,
                        sest.Station, sest.StationType);
                    // try to get the slope:
                    foreach (int i in Enum.GetValues(typeof(SuperelevationCrossSegmentType)))
                    {
                        try
                        {
                            // if this succeeds, we know the segment type:                               
                            double slope = sest.GetSlope((SuperelevationCrossSegmentType)i, false);
                            ed.WriteMessage("   Slope: {0} Segment type: {1}\n",slope,Enum.GetName(typeof(SuperelevationCrossSegmentType),i));
                        }
                            // silently fail:
                        catch (InvalidOperationException e) { }
                    }
                }
            }
        }
    }
    

## Creating a User-Defined Superelevation Curve

You can use the SuperelevationCurveCollection::AddUserDefinedCurve method to create a user-defined superelevation curve. To define the curve, you specify the alignment sub-entities at the start and at the end of the curve. User-defined curves can include alignment lines. Make sure there are no existing superelevation curves between the start sub-entity and the end sub-entity that you specify. 

The following sample code creates a user-defined superelevation curve which consists of an alignment line and an alignment spiral, and the entities between them. 
    
    
    [CommandMethod("AddUserDefinedCurve")]
    public void AddUserDefinedCurve ()
    {
        doc = CivilApplication.ActiveDocument;
        Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
        using (Transaction ts = Application.DocumentManager.MdiActiveDocument.Database.TransactionManager.StartTransaction())
        {
            // get first alignment:
            ObjectId alignID = doc.GetAlignmentIds()[0];
            Alignment myAlignment = ts.GetObject(alignID, OpenMode.ForWrite) as Alignment;
            SuperelevationCurveCollection superelevationCurves = myAlignment.SuperelevationCurves;
            AlignmentEntityCollection alignmentEntities = myAlignment.Entities;
            AlignmentLine startEntity = alignmentEntities.EntityAtStation(100.00) as AlignmentLine;
            // get the alignment line as the start of user defined curve
            AlignmentSubEntityLine startSubEntity = startEntity[0] as AlignmentSubEntityLine;
            AlignmentSCS endEntity = alignmentEntities.EntityAtStation(670.00) as AlignmentSCS;
            // get the first sub-entity spiral as the end of user defined curve
            AlignmentSubEntitySpiral endSubEntity = endEntity[0] as AlignmentSubEntitySpiral;
            SuperelevationCurve superelevationCurve = superelevationCurves.AddUserDefinedCurve(startSubEntity, endSubEntity);
            ed.WriteMessage("Name: {0}\n", superelevationCurve.Name);
            ed.WriteMessage(" Start: {0} End: {1}\n", superelevationCurve.StartStation, superelevationCurve.EndStation);
        }
    }
