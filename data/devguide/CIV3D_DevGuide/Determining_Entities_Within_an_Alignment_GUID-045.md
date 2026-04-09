<!-- Developer's Guide > API Developer's Guide > Alignments > Basic Alignment Operations > Determining Entities Within an Alignment -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-04543DA8-A2D5-4E6E-A0D4-5B5C75DD0414.htm -->

# Determining Entities Within an Alignment

Each of the entities in the Alignment::Entities collection is a type derived from the Alignment::AlignmentEntity class. By checking the AlignmentEntity.EntityType property, you can determine the specific type of each entity and cast the reference to the correct type.

The following sample loops through all entities in an alignment, determines the type of entity, and prints one of its properties.
    
    
    [CommandMethod("EntityProperties")]
    public void EntityProperties()
    {
        doc = CivilApplication.ActiveDocument;
        Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
        using (Transaction ts = Application.DocumentManager.MdiActiveDocument.Database.TransactionManager.StartTransaction())
        {
            // Ask the user to select an alignment to get info about
            PromptEntityOptions opt = new PromptEntityOptions("\nSelect an Alignment");
            opt.SetRejectMessage("\nObject must be an alignment.");
            opt.AddAllowedClass(typeof(Alignment), false);
            ObjectId alignID = ed.GetEntity(opt).ObjectId;
            Alignment align = ts.GetObject(alignID, OpenMode.ForRead) as Alignment;
     
            int i = 0;
            // iterate through each Entity and check its type
            foreach (AlignmentEntity myAe in align.Entities){
                i++;
                String msg = "";
                switch (myAe.EntityType)
                {                            
                    case AlignmentEntityType.Arc:
                        AlignmentArc myArc = myAe as AlignmentArc;
                        msg = String.Format("Entity{0} is an Arc, length: {1}\n", i, myArc.Length);
                        break;
     
                    case AlignmentEntityType.Spiral:
                        AlignmentSpiral mySpiral = myAe as AlignmentSpiral;
                        msg = String.Format("Entity{0} is a Spiral, length: {1}\n", i, mySpiral.Length);
                        break;
                    // we could detect other entity types as well, such as 
                    // Tangent, SpiralCurve, SpiralSpiral, etc.
                    default:
                        msg = String.Format("Entity{0} is not a spiral or arc.\n", i);
                        break;
     
                }
                // write out the Entity information
                ed.WriteMessage(msg);
            }
        }
    }
    

Each entity has an identification number contained in its AlignmentEntity.EntityId property. Each entity knows the numbers of the entities before and after it in the alignment, and you can access specific entities by identification number through the AlignmentEntityCollection.EntityAtId() method.
