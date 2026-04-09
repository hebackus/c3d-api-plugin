<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > About .NET and the AutoCAD .NET API (.NET) > Sample Code (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-577EDC34-0A10-4D63-BED4-ECA4570355A3.htm -->

# Sample Code (.NET)

This guide and the _ObjectARX SDK_ together contain a large number of sample projects, subroutines, and functions that demonstrate the core concepts of the AutoCAD .NET API. 

You can also find sample projects that demonstrate some aspects of the AutoCAD .NET API on the Autodesk website at _<https://www.autodesk.com/developautocad>_. These sample projects show a wide range of functionality, from working with database objects to defining object overrides, managing sheet sets, and much more. 

The samples in this guide are shown in the C# programming language, but the AutoCAD .NET API can be used to create custom applications with other programming languages that support .NET. 

Note: While VB.NET is a supported programming language with the AutoCAD .NET API, it is recommended to learn and use C# as it is more prevalent in the industry. If you are currently using or want to use VB.NET or another .NET programming language, you can convert the C# code samples in this guide using an online code translator or AI agent. To find an online code translator, search on the phrase "C# to VB.NET translator" or the programming language into which you want to convert the C# code samples. 

Additionally, the sample code in this guide can be copied to the clipboard and pasted directly into an open code editor window within Microsoft Visual Studio, then built and loaded in AutoCAD. At the top of most code samples are the namespaces required for that particular sample. Add those that are needed to the top of the code module in your project. 

Note: The AutoCAD .NET samples in this guide contain limited error handling and disposal of objects to keep the concepts simple and easy to read. You should apply additional error handling and checking when using any sample code in your project. 

## Procedures

**To run the sample code from the Help files**

  1. In Microsoft Visual Studio, open a code editor window, add the proper namespaces and define a class if one does not already exist. 
  2. Copy the sample code from the Help file and paste the copied code into the defined class. 
  3. In Microsoft Visual Studio, click Build menu  Build <_Project_ >. 
  4. In AutoCAD, at the Command prompt, enter **netload**. 
  5. In the Choose .NET Assembly dialog box, select the built assembly file. Click Open. 
  6. At the Command prompt, enter the name of the command defined inside the CommandMethod attribute.
