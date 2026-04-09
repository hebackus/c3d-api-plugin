<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Develop Applications (.NET) > Handle Errors (.NET) > Trap Runtime Errors (.NET) > Using the VB.NET On Error Statements (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-6E5D85C0-5F00-40A7-920A-2CD4D77DF8AA.htm -->

# Using the VB.NET On Error Statements (.NET)

In VB.NET, runtime errors can be trapped with the Try or On Error statement. This statement literally sets a general trap in the application. When an error occurs, this statement automatically detours processing to your specially written error handler. The default error handling for the system is bypassed. 

The On Error statement has three forms: 

  * On Error Resume Next
  * On Error GoTo Label
  * On Error GoTo 0

Note: Both Try and On Error statements cannot be used in the same procedure. 

## On Error Resume Next statement

The On Error Resume Next statement is used when you want to ignore errors. This statement traps the error and instead of displaying an error message and terminating the program, execution is moved to the next line of code and continues processing. 

For example, if you wanted to create a procedure to iterate through Model space and change the color of each entity, you know that AutoCAD will throw an error if you try to color an entity on a locked layer. Instead of terminating the program, simply skip the entity on the locked layer and continue processing the remaining entities. The On Error Resume Next statement lets you do just that. 

## On Error GoTo Label statement

The On Error GoTo Label statement is used when you want to write an explicit error handler. This statement traps the error and instead of displaying an error message and terminating the program, it jumps to a specific location in your code. Your code can then respond to the error in whatever manner is appropriate for your application. For example, you could jump to the beginning of the program using 0 (zero), a line number, or a named label such as ErrNoFileFound. Named labels are defined by using the following syntax: 
    
    
    HandlerName:

## Use the Err object with trapped errors

The Exception object is used with Try statements, while the Err object is used to provide information on the type of error that has been trapped with the On Error statements. This object has several properties: Number, Description, Source, HelpFile, HelpContext, and LastDLLError. The properties of the Err object get filled in with the information for the most current error. The most important properties are the Number and Description properties. The Number property contains the unique error code associated with the error, and the Description property contains the error message that would normally be displayed. 

In your error handler you can compare the Number property of the error to an expected value. This will help you determine the nature of the error that was occurred. Once you know what kind of error you are dealing with, you can take the appropriate action.
