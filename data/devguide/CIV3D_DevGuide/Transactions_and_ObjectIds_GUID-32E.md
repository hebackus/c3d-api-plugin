<!-- Developer's Guide > API Developer's Guide > Getting Started > Migrating COM code to .NET > Transactions and ObjectIds -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-32EBE075-5D30-4762-A7D3-C1D202D5FB8F.htm -->

# Transactions and ObjectIds

In the .NET API, code that reads and writes to root Civil documents need to use an Autodesk.AutoCAD.DatabaseServices.TransactionManager object to start and commit transactions. It’s a best practice to manage a Transaction with a Using statement, which automatically disposes the Transaction at the end of the block; otherwise, the Transaction should be explicitly disposed of in the Finally section of a Try-Finally block. Here’s an example of a Transaction in a Using block: 
    
    
    using (Transaction trans=TransactionManager.StartTransaction())
    {
      //operation here
      trans.Commit();
    }
    

Note:

See the section "Use Transactions With the Transaction Manager (.NET)" in the AutoCAD .NET Developer’s Guide for more information about using the Transaction object to open and modify drawing database objects. 

In the .NET API, objects that you get from collections are, in most cases, type ObjectId, which have to be cast to their intended type using a Transaction object (returned by TransactionManager.StartTransaction()). Here’s an example: 
    
    
    m_AligmentStyleId = m_doc.Styles.AlignmentStyles.Item(sStyleName)
    oAlignmentStyle = m_trans.GetObject(m_AligmentStyleId, OpenMode.ForWrite) As AlignmentStyle
