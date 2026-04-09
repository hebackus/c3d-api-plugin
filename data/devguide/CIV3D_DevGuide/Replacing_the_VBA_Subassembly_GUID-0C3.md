<!-- Developer's Guide > API Developer's Guide > Converting VBA Subassemblies to .NET > Procedure > Replacing the VBA Subassembly -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-0C326A7E-8B90-48FD-846D-0E6BF6D3DBCE.htm -->

# Replacing the VBA Subassembly

Once the VBA custom subassembly has been ported to .NET and installed in a catalog file, drawings need to be updated to use the new code. Below is an example .NET macro that performs this task. This macro gets a subassembly by name (“VBASubassembly”). It then creates a new SubassemblyGenerator object, passing in the mode (“UseDotNet”), the dll in which the new subassembly is located, the name of the .NET subassembly. Finally it sets the subassembly GeometryGenerator parameter to the new SubassemblyGenerator. When the transaction is committed, the subassembly is replaced.
    
    
    [CommandMethod("ConvertVbaSA")]
    public void ConvertVbaSA()
    {
        using(Transaction trans = m_transactionManger.StartTransaction())
        {
        ObjectId saId = Autodesk.Civil.ApplicationServices.CivilApplication.ActiveDocument.SubassemblyCollection["VBASubassembly"];
        Subassembly sa = trans.GetObject(saId, OpenMode.ForWrite) as Subassembly;
        SubassemblyGenerator genData = new SubassemblyGenerator(SubassemblyGeometryGenerateMode.UseDotNet, "C3DStockSubassemblies.dll", "Subassembly.DotNetSubassembly");
        sa.GeometryGenerator = genData;
        trans.Commit();
        }
    }
