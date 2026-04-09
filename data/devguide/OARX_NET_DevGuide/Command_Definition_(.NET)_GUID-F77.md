<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Basics of the AutoCAD .NET API (.NET) > Define Commands and AutoLISP Functions (.NET) > Command Definition (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-F77E8FE0-8034-4704-93BD-F717608F8223.htm -->

# Command Definition (.NET)

When defining a command, you use the CommandMethod attribute. The CommandMethod attribute expects a string value to use as the global name of the command that is being defined. Along with a global command name, the CommandMethod attribute can accept the following values: 

  * **Command Flags** \- Defines the behavior of the command 
  * **Group Name** \- Command group name 
  * **Local Name** \- Local command name, usually language specific 
  * **Help Topic Name** \- Help topic name that should be displayed when F1 is pressed 
  * **Context Menu Type Flags** \- Defines the context menu behavior when the command is active 
  * **Help File Name** \- Help file that contains the help topic that should be displayed when the command is active and F1 is pressed 

The following table lists the available flags that can be used to define the behavior of a command. 

Enum Value | Description   
---|---  
ActionMacro | Command can be recorded as an action with the Action Recorder.   
Defun | Command can be invoked as a LISP function and can therefore use acedGetArgs() to receive arguments from LISP and can use the acedRetXxx() functions to return values to LISP. This flag can only be set by the Visual LISP engine.   
DocExclusiveLock | Document will be exclusively locked when command is invoked.   
DocReadLock | Document will be read locked when command is invoked.   
Interruptible | The command may be interrupted when prompting for user input.   
Modal | Command cannot be invoked while another command is active.   
NoActionRecording | Command cannot be recorded as action with the Action Recorder.   
NoBlockEditor | Command cannot be used from the Block Editor.   
NoHistory | Command is not added to the repeat-last-command history list.   
NoInferConstraint | Command cannot be used when inferring constraints.   
NoInternalLock | Document cannot be internally locked.   
NoMultiple | Command does not support the multiple behavior when prefixed with an astericks (*) as part of a command macro.   
NoNewStack | Command does not create a new item on the stack.   
NoOEM | Command cannot be accessed from AutoCAD OEM.   
NoPaperSpace | Command cannot be used from Paper space.   
NoPerspective | Command cannot be used when PERSPECTIVE is set to 1.   
NoTileMode | Command cannot be used when TILEMODE is set to 1.   
NoUndoMarker | Command does not support undo markers. This is intended for commands that do not modify the database, and therefore should not show up in the undo file.   
Redraw | When the pickfirst set or grip set are retrieved, they are not cleared.   
Session | Command is executed in the context of the application rather than the current document context.   
TempShowDynDimension | Command allows the display of dynamic dimensions temporarily when entities are selected.   
Transparent | Command can be used while another command is active.   
Undefined | Command can only be used via its Global Name.   
UsePickSet | When the pickfirst set is retrieved, it is cleared.   
  
## Instance and Static Command Methods

Command methods may be declared as either instance or static methods. Static command methods are declared with the static keyword in C#, or with the Shared keyword in VB .NET. Instance command methods are public class members that are not declared with the static or Shared keyword. 

For an instance command method, the method's enclosing type is instantiated separately for each open document. This means that each document gets a private copy of the command's instance data. Thus there is no danger of overwriting document-specific data when the user switches documents. If an instance method needs to share data globally, it can do so by declaring static or Shared member variables. 

For a static command method, the managed wrapper runtime module does not need to instantiate the enclosing type. A single copy of the method's data is used, regardless of the document context. Static commands normally do not use per-document data and do not require special consideration for MDI mode. 

Instance and static methods can be defined with command flags to accommodate special requirements. For example, an instance method may be declared with an attribute that sets the CommandFlags.Session flag. This means that the command runs in the application execution context, but also maintains per-document data. An AutoCAD example of such a command is the PROPERTIES command. 

Likewise, a static method may be declared without the CommandFlags.Session flag. This combination is useful for commands that run in the document context but do not need to maintain per-document data. 

## Syntax to Define a Command

The following demonstrates the creation of a CommandMethod attribute that defines a command named CheckForPickfirstSelection. The attribute also uses the command flag UsePickSet to indicate that the command is allowed to use the objects that are selected before the command is started. 

### C#
    
    
    [CommandMethod("CheckForPickfirstSelection", CommandFlags.UsePickSet)]
    public static void CheckForPickfirstSelection()
    {
     . . .
    }

### VB.NET
    
    
    <CommandMethod("CheckForPickfirstSelection", CommandFlags.UsePickSet)> _
    Public Sub CheckForPickfirstSelection()
     . . .
    End Sub

You can specify the use of more than one flag. 

### C#
    
    
    [CommandMethod("CheckForPickfirstSelection", CommandFlags.UsePickSet |
                                                 CommandFlags.NoBlockEditor)]
    public static void CheckForPickfirstSelection()
    {
     . . .
    }

### VB.NET
    
    
    <CommandMethod("CheckForPickfirstSelection", CommandFlags.UsePickSet + _
                                                 CommandFlags.NoBlockEditor)> _
    Public Sub CheckForPickfirstSelection()
     . . .
    End Sub
