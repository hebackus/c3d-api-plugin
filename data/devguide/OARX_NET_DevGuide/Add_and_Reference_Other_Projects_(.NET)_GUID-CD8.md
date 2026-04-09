<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Getting Started with Microsoft Visual Studio (.NET) > Edit an Existing Project or Solution (.NET) > Add and Reference Other Projects (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-CD88C04C-8016-4011-A484-5C73A144A546.htm -->

# Add and Reference Other Projects (.NET)

Adding and referencing projects allows you to share code across multiple projects. You can create centralized libraries of commonly used methods, functions and classes, and then reference the library when needed. Projects can be referenced in the following ways: 

  * Add the project to a solution and reference it to a project within the solution 
  * Reference a compiled assembly file to a project 

When you add a project to a solution, a new node for the project is displayed in the Solution Explorer. This node is titled the same as the project that was referenced. After a project is added, it must be referenced to the project using the Add Reference dialog box. 

If the project has been compiled into an assembly DLL file, you can reference the file to a project using the Add Reference dialog box. After a project or assembly DLL file is referenced to a project, you use the Imports or using declaration with the namespace or project name to utilize any of the exposed objects (classes or forms) in your project. 

## Procedures

**To reference another project**

  1. Add a New Project or Existing Project to the current solution. 
  2. Once the project has been added to the current solution, in the Solution Explorer, right-click the project that you want to add the project reference to and click Add Reference. 
  3. In the Add Reference dialog box, Projects tab, select the project you want to reference. Click OK. 

The selected project will appear under the References folder in the Solution Explorer. 

  4. In the Solution Explorer, double-click the code module that you want to use the publicly exposed functions, methods, or objects that are in the referenced project. 
  5. At the top of the code module, add an Imports or using declaration for the project or namespace in the project that contains the functions, methods, or objects you want to use. 

For example, if a namespace containing an exposed class in the referenced project is named AdskUtilities, you would add the following to the code module to indicate that you are going to use that namespace from the referenced project: 

### C#
         
         using AdskUtilities;

### VB.NET
         
         Imports AdskUtilities

  6. Use the namespace in the same way you would any other .NET or COM library referenced to your project.
