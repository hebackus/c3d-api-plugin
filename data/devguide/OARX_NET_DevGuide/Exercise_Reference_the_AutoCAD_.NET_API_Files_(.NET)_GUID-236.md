<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Getting Started with Microsoft Visual Studio (.NET) > Exercises: Create Your First Project (.NET) > Exercise: Reference the AutoCAD .NET API Files (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-2363CE7C-AC2B-4CAC-AE5D-F77B386132D7.htm -->

# Exercise: Reference the AutoCAD .NET API Files (.NET)

In this exercise, you will reference the .NET assemblies _AcCoreMgd.dll_ , _AcMgd.dll_ , and _AcDbMgd.dll_. After you reference the three files, you will adjust the properties of the referenced files so they are not copied to the build output folder. 

## To reference the AutoCAD .NET API Files

  1. In Microsoft Visual Studio, click View menu  Solution Explorer to display the Solution Explorer; if it is not already displayed. 
  2. In the Solution Explorer, right-click the Dependencies node and click Add Project Reference. 
  3. In the Reference Manager - _< project>_ dialog box, at the bottom of the dialog, click Browse. 
  4. In the Select the Files to Reference dialog box, browse to one of the following locations: 
     * _inc_ folder within the ObjectARX SDK that is supported for this release (recommended) 
     * Install folder of AutoCAD; default install location is _< drive>:\Program Files\Autodesk\AutoCAD <release>_
  5. Select the _AcCoreMgd.dll_ file, then press and hold Ctrl, and select the _AcDbMgd.dll_ and _AcMgd.dll_ files. Click Add. 
  6. Click OK. 
  7. In the Solution Explorer, click the triangle to the left of the Dependencies node to expand it. 
  8. Press and hold Ctrl, and select AcCoreMgd, AcDbMgd, and AcMdg from under the Dependencies node. 
  9. Right-click over one of the selected references and click Properties. 
  10. In the Properties window, click the Copy Local field and then select No from the drop-down list. 

Note: Setting Copy Local to No instructs Microsoft Visual Studio to not include the referenced DLLs in the build output for the project. If the referenced DLLs are copied to the build output folder, it might cause unexpected results when the assembly file is loaded into AutoCAD.
