<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Alignments in COM > Basic Alignment Operations > Determining Entities Within an Alignment -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-3B57BD08-EDB3-4BDF-BC2B-94203B65D632.htm -->

# Determining Entities Within an Alignment

Each of the entities in the AeccAlignment.Entities collection is a type derived from the AeccAlignmentEntity. By checking the AeccAlignmentEntity.Type property, you can determine the specific type of each entity and cast the reference to the correct type.

The following sample loops through all entities in an alignment, determines the type of entity, and prints one of its properties.
    
    
    Debug.Print "Number of Entities: "; oAlignment.Entities.Count
     
    Dim i as Integer
    For i = 0 To oAlignment.Entities.Count - 1
        Select Case (oAlignment.Entities.Item(i).Type)
        Case aeccTangent
            Dim oTangent As AeccAlignmentTangent
            Set oTangent = oAlignment.Entities.Item(i)
            Debug.Print "Tangent length:" & oTangent.Length
        Case aeccArc
            Dim oArc As AeccAlignmentArc
            Set oArc = oAlignment.Entities.Item(i)
            Debug.Print "Arc radius:" & oArc.Radius
        Case aeccSpiral
            Dim oSpiral As AeccAlignmentSpiral
            Set oSpiral = oAlignment.Entities.Item(i)
            Debug.Print "Spiral A value:" & oSpiral.A
        Case aeccSpiralCurveSpiralGroup
            Dim oSCSGroup As AeccAlignmentSCSGroup
            Set oSCSGroup = oAlignment.Entities.Item(i)
            Debug.Print "Radius of curve in SCS group:" _
              & oSCSGroup.Arc.Radius
     
        ' And so on for AeccAlignmentSTSGroup,
        ' AeccAlignmentSTGroup, AeccAlignmentTSGroup
        ' AeccAlignmentSCGroup, and AeccAlignmentCSGroup types.
        End Select
    Next i
    

Each entity has an identification number contained in its AeccAlignmentEntity.Id property. Each entity knows the numbers of the entities before and after it in the alignment, and you can access specific entities by identification number through the AeccAlignmentEntities.EntityAtId method.
