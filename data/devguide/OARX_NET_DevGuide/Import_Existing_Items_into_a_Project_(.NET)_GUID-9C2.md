<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Getting Started with Microsoft Visual Studio (.NET) > Edit an Existing Project or Solution (.NET) > Import Existing Items into a Project (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-9C205780-8091-4AFE-9480-5BD69711B806.htm -->

# Import Existing Items into a Project (.NET)

Importing allows you to add an existing item to your project that might already exist in another project. Importing existing code or class modules or forms makes it easy to reuse utility functions across many projects. 

When you import an item, a copy of the file or a link to the file you are importing is added to the project. When a copy of the item is created, the original file is left unaltered in its original place. Linked files provide access to the original file, which is great for reusing common code that might be shared between multiple projects. 

If you import an item with the same name as an existing item, you are prompted to replace the existing item in the project with the one being imported. 

The imported component is added to your project and appears in the Solution Explorer. To edit the properties of the item, select the item in the Solution Explorer and change its properties in the Properties window. 

## Procedures

**To import an existing item into a project**

  1. In Microsoft Visual Studio, Solution Explorer, right-click the project to which you want to add an existing item and click Add  Existing Item. 
  2. In the Add Existing Item - _< Project>_ dialog box, browse to and select the file that contains the item you want to add. 
  3. Click Add to create a copy of the selected file, or click the down arrow to the right of the Add button and click Add As Link to create a link to the file instead of creating a copy of the file.
