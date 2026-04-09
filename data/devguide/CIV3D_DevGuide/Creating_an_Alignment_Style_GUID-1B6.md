<!-- Developer's Guide > API Developer's Guide > Alignments > Alignment Style > Creating an Alignment Style -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-1B662B5C-946B-4338-81E8-3E7AEFA0A653.htm -->

# Creating an Alignment Style

Styles govern many aspects of how alignments are drawn, including direction arrows and curves, spirals, and lines within an alignment. All alignment styles are contained in the CivilDocument.Styles.AlignmentStyles collection. Alignment styles must be added to this collection before being used by an alignment object. A style is normally assigned to an alignment when it is first created, but it can also be assigned to an existing alignment through the Alignment.StyleId property. 
    
    
    [CommandMethod("SetAlignStyle")]
    public void SetAlignStyle()
    {
        doc = CivilApplication.ActiveDocument;
        Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
        using (Transaction ts = Application.DocumentManager.MdiActiveDocument.Database.TransactionManager.StartTransaction())
        {
            // Ask the user to select an alignment 
            PromptEntityOptions opt = new PromptEntityOptions("\nSelect an Alignment");
            opt.SetRejectMessage("\nObject must be an alignment.\n");
            opt.AddAllowedClass(typeof(Alignment), false);
            ObjectId alignID = ed.GetEntity(opt).ObjectId;
            Alignment myAlignment = ts.GetObject(alignID, OpenMode.ForWrite) as Alignment;
            ObjectId styleID = doc.Styles.AlignmentStyles.Add("Sample alignment style");
            AlignmentStyle myAlignmentStyle = ts.GetObject(styleID, OpenMode.ForWrite) as AlignmentStyle;
            // don't show direction arrows                
            myAlignmentStyle.GetDisplayStyleModel(AlignmentDisplayStyleType.Arrow).Visible = false;
            myAlignmentStyle.GetDisplayStylePlan(AlignmentDisplayStyleType.Arrow).Visible = false;
            // show curves in violet
            myAlignmentStyle.GetDisplayStyleModel(AlignmentDisplayStyleType.Curve).Color = Color.FromColorIndex(ColorMethod.ByAci, 200);
            myAlignmentStyle.GetDisplayStylePlan(AlignmentDisplayStyleType.Curve).Color = Color.FromColorIndex(ColorMethod.ByAci, 200);
            // show straight sections in blue
            myAlignmentStyle.GetDisplayStyleModel(AlignmentDisplayStyleType.Line).Color = Color.FromColorIndex(ColorMethod.ByAci, 160);
            myAlignmentStyle.GetDisplayStylePlan(AlignmentDisplayStyleType.Line).Color = Color.FromColorIndex(ColorMethod.ByAci, 160);
            // assign style to an existing alignment
            myAlignment.StyleId = myAlignmentStyle.Id;
            ts.Commit();
        }
    }
