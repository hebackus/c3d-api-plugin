<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Create and Edit AutoCAD Entities (.NET) > Open and Close Objects (.NET) > Use Transactions With the Transaction Manager (.NET) > Dispose Objects (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-9DFB5767-F8D6-4A88-87D6-9676C0189369.htm -->

# Dispose Objects (.NET)

When creating new objects in .NET, you must properly free the objects from memory through the disposal process and garbage collection. You use the Dispose method or the Using statement to signal when an object is ready for garbage collection. The Using statement in most cases is the preferred method, as it makes the proper calls to close and dispose of the object when it is no longer needed. 

You need to dispose of an object under the following conditions: 

  * Always with a Transaction or DocumentLock object 
  * Always with newly created database objects, objects derived from DBObject, that are being added to a transaction 
  * Always with newly created database objects, objects derived from DBObject, that are not added to the database 
  * Do not have to with existing database objects, objects derived from DBObject, opened with a transaction object and the GetObject method 

## C#
    
    
    // Dispose an object with the using statement
    using (<dataType> <object>  = <value>)
        // Do something here
    }
     
    // Manually dispose of an object with the Dispose method
    <object>. Dispose ();

## VB.NET
    
    
    ' Dispose an object with the Using statement
    Using <object> As <dataType> = <value>
        ' Do something here
    End Using
     
    ' Manually dispose of an object with the Dispose method
    <object>.Dispose()
