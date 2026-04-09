<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > ResultBuffer Data Type (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-A43BA3F1-513E-42E5-A21F-633FAF97B5C9.htm -->

# ResultBuffer Data Type (.NET)

The ResultBuffer type is a class that mirrors the resbuf struct defined in the ObjectARX SDK. The resbuf struct provides a flexible container for AutoCAD-specific data. 

An Autodesk.AutoCAD.DatabaseServices.ResultBuffer class object is used in much the same way as a resbuf chain. You define a ResultBuffer and populate it with a sequence of data pairs. Each pair contains a data type description and a value. In the managed API, these data pairs are instances of the Autodesk.AutoCAD.DatabaseServices.TypedValue class. This utility class serves the same purpose as the restype and resval members of the resbuf struct. 

The TypedValue.TypeCode property is a 16-bit integer value that indicates the TypedValue.Value property's data type. Acceptable TypeCode values depend on the specific use of a ResultBuffer instance. For example, TypeCode values that are suitable for an xrecord definition are not necessarily appropriate for xdata. The Autodesk.AutoCAD.DatabaseServices.DxfCode enum defines codes that accurately describe the full range of possible ResultBuffer data types. 

The TypedValue.Value property maps to an instance of System.Object, and theoretically may contain any type of data. However, the Value data must conform to the type indicated by TypeCode to guarantee usable results. 

You can prepopulate a ResultBuffer by passing an array of TypedValue objects to its constructor, or you can construct an empty ResultBuffer and later call the ResultBuffer::Add() method to append new TypedValue objects. The following example shows a typical ResultBuffer constructor usage: 

## C#
    
    
    using (Xrecord rec = new Xrecord())
    {
        rec.Data = new ResultBuffer(
            new TypedValue(Convert.ToInt32(DxfCode.Text), "This is a test"),
            new TypedValue(Convert.ToInt32(DxfCode.Int8), 0),
            new TypedValue(Convert.ToInt32(DxfCode.Int16), 1),
            new TypedValue(Convert.ToInt32(DxfCode.Int32), 2),
            new TypedValue(Convert.ToInt32(DxfCode.HardPointerId), db.BlockTableId),
            new TypedValue(Convert.ToInt32(DxfCode.BinaryChunk), new byte[] {0, 1, 2, 3, 4}),
            new TypedValue(Convert.ToInt32(DxfCode.ArbitraryHandle), db.BlockTableId.Handle),
            new TypedValue(Convert.ToInt32(DxfCode.UcsOrg),
            new Point3d(0, 0, 0)));
    }

## VB.NET
    
    
    Using rec As New Xrecord()
        rec.Data = New ResultBuffer( _
            New TypedValue(CInt(DxfCode.Text), "This is a test"), _
            New TypedValue(CInt(DxfCode.Int8), 0), _
            New TypedValue(CInt(DxfCode.Int16), 1), _
            New TypedValue(CInt(DxfCode.Int32), 2), _
            New TypedValue(CInt(DxfCode.HardPointerId), db.BlockTableId), _
            New TypedValue(CInt(DxfCode.BinaryChunk), New Byte(){0, 1, 2, 3, 4}), _
            New TypedValue(CInt(DxfCode.ArbitraryHandle), db.BlockTableId.Handle), _
            New TypedValue(CInt(DxfCode.UcsOrg), New Point3d(0, 0, 0)))
    End Using
