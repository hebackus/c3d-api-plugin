<!-- Developer's Guide > API Developer's Guide > Pipe Networks > Base Objects > Retrieving the Parts List -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-9552DAF0-8324-46E0-9FAA-FAE60B57651A.htm -->

# Retrieving the Parts List

CivilDocument.Styles.PartsListSet contains a read-only collection of all the lists of part types available in the document. Each list is an object of type PartList, a read-only collection of PartsList ObjectIds. A part family represents a broad category of parts, and is identified by a GUID (Globally Unique Identification) value. A part family can only contain parts from one domain - either pipes or structures but not both. Part families contain a read-only collection of part filters (PartSizeFilter), which are the particular sizes of parts. A part filter is defined by its PartSizeFilter.PartDataRecord property, a collection of fields describing various aspects of the part.

This sample prints the complete listing of all parts in a document.
    
    
    [CommandMethod("PrintParts")]
    public void PrintParts()
    {
        CivilDocument doc = CivilApplication.ActiveDocument;
        Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
        using (Transaction ts = Application.DocumentManager.MdiActiveDocument.
            Database.TransactionManager.StartTransaction())
        {
            // SettingsPipeNetwork oSettingsPipeNetwork = doc.Settings.GetSettings<SettingsPipeNetwork>() as SettingsPipeNetwork;
            PartsListCollection oPartListCollection = doc.Styles.PartsListSet;
            ed.WriteMessage("Number of parts lists in document: {0}\n", oPartListCollection.Count);
            foreach (ObjectId objId in oPartListCollection)
            {
                PartsList oPartsList = ts.GetObject(objId, OpenMode.ForWrite) as PartsList;
                ed.WriteMessage("PARTS LIST: {0}\n----------------\n", oPartsList.Name);
                // From the part list, looking at only those part families
                // that are pipes, print all the individual parts, plus
                // some information about each part.
                ObjectIdCollection pipeFamilyCollection = oPartsList.GetPartFamilyIdsByDomain(DomainType.Pipe);
                ed.WriteMessage("  Pipes\n  =====\n");
                foreach (ObjectId objIdPfa in pipeFamilyCollection)
                {
                    PartFamily oPartFamily = ts.GetObject(objIdPfa, OpenMode.ForWrite) as PartFamily;
                    if (oPartFamily.Domain == DomainType.Pipe)
                    {
                        ed.WriteMessage("  Family: {0}\n", oPartFamily.Name);
                        SizeFilterRecord oSizeFilterRecord = oPartFamily.PartSizeFilter;
                        SizeFilterField SweptShape = oSizeFilterRecord.GetParamByContextAndIndex(PartContextType.SweptShape, 0);
                        SizeFilterField MinCurveRadius = oSizeFilterRecord.GetParamByContextAndIndex(PartContextType.MinCurveRadius, 0);
                        //SizeFilterField StructPipeWallThickness;
                        SizeFilterField FlowAnalysisManning = oSizeFilterRecord.GetParamByContextAndIndex(PartContextType.FlowAnalysisManning, 0);
                        SizeFilterField m_Material = oSizeFilterRecord.GetParamByContextAndIndex(PartContextType.Material, 0);
                        // SizeFilterField PipeInnerDiameter = oSizeFilterRecord.GetParamByContextAndIndex(PartContextType.PipeInnerDiameter, 0);
                        ed.WriteMessage("  {0}: {1}, {2}: {3}, {4}: {5} {6}: {7}\n",
                            SweptShape.Description, SweptShape.Value,
                            MinCurveRadius.Description, MinCurveRadius.Value,
                            FlowAnalysisManning.Description, FlowAnalysisManning.Value,
                            m_Material.Description, m_Material.Value
                            );
                    }
                }
                // From the part list, looking at only those part families
                // that are structures, print all the individual parts.
                ed.WriteMessage("  Structures\n  =====\n");
                foreach (ObjectId objIdPfa in pipeFamilyCollection)
                {
                    PartFamily oPartFamily = ts.GetObject(objIdPfa, OpenMode.ForWrite) as PartFamily;
                    if (oPartFamily.Domain == DomainType.Structure)
                    {
                        ed.WriteMessage("  Family: {0}\n", oPartFamily.Name);
                    }
                }
            }
        }
    }
