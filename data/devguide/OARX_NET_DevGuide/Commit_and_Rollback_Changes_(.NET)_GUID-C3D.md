<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Open and Close Objects (.NET) > Use Transactions With the Transaction Manager (.NET) > Commit and Rollback Changes (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-C3DE4301-EAC3-4745-A434-9F28EE87AB73.htm -->

# Commit and Rollback Changes (.NET)

When using transactions, you are able to decide when changes to objects are saved to the drawing database. You use the Commit method to save the changes made to the objects opened within a transaction. If your program encounters an error you can rollback any changes made within a transaction with the Abort method. 

If Commit is not called before Dispose is called, all changes made within the transaction are rolled back. Whether Commit or Abort is called, you need to call Dispose to signal the end of the transaction. If the transaction object is started with the Using statement, you do not have to call Dispose. 

### C#
    
    
    // Commit the changes made within the transaction
    <transaction>.Commit();
     
    // Abort the transaction and rollback to the previous state
    <transaction>.Abort();

### VB.NET
    
    
    '' Commit the changes made within the transaction
    <transaction>.Commit()
     
    '' Abort the transaction and rollback to the previous state
    <transaction>.Abort()
