<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > VBA/VB to C# or VB.NET Comparison (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-1FE982C2-EAFF-4737-A786-CD54053597D5.htm -->

# VBA/VB to C# or VB.NET Comparison (.NET)

While most programming languages differ from each other in their syntax and capabilities, there still some fundamental concepts and logic that they share. 

The following table compares VBA functions with the similar C# and VB.NET functions and operators. The ActiveX library is indicated by “AutoCAD.Application” and the .NET Managed library equivalents are indicated by “Autodesk.AutoCAD” and the C# or VB.NET equivalents are listed as a function or operator. 

Math Functions   
---  
ActiveX, VBA, or Visual Basic 6  |  .NET equivalent (same unless noted)   
\+ (addition operator)  |  \+ (addition operator)   
\- (subtraction operator)  |  \- (subtraction operator)   
* (multiplication operator)  |  * (multiplication operator)   
/ (division operator)  |  / (division operator)   
^ (exponentiation operator)  |  ^ (exponentiation operator)   
Abs function  |  System.Math.Abs function   
Atn function  |  System.Math.Atan function   
Cos function  |  System.Math.Cos function   
Exp function  |  System.Math.Exp function   
Log function  |  System.Math.Log function   
Max function  |  System.Math.Max function   
Min function  |  System.Math.Min function   
Mod function  | 

.NET
     System.Math.DivRem function 
C#
     % (operator) 
VB.NET
     Mod function   
Sin function  |  System.Math.Sin function   
Sqr function  |  System.Math.Sqrt function   
  
Conditional and Loop Statements   
---  
ActiveX, VBA, or Visual Basic 6  |  .NET equivalent (same unless noted)   
Do Until… Loop statement  | 

C#
     Use do... while statement 
VB.NET
     Do Until... Loop statement   
Do While… Loop statement  | 

C#
     do... while statement 
VB.NET
     Do While... Loop statement   
For Each...Next statement  | 

C#
     Foreach and For statements 
VB.NET
     For Each...Next statement   
If… Then… Else...End If statement  | 

C#
     if... else... statement 
VB.NET
     If… Then… Else...End If statement   
Select Case statement  | 

C#
     Switch statement 
VB.NET
     Select Case statement   
While… Wend statement  | 

C#
     while... statement 
VB.NET
     While... Wend statement   
  
Logic Statements   
---  
ActiveX, VBA, or Visual Basic 6  |  .NET equivalent (same unless noted)   
= (equal to comparison operator)  | 

C#
     == (equal to comparison operator) 
VB.NET
     = (equal to comparison operator)   
<> (not equal to comparison operator)  | 

C#
     != (not equal to comparison operator) 
VB.NET
     <> (not equal to comparison operator)   
< (less than comparison operator)  |  < (less than comparison operator)   
<= (less than or equal to comparison operator)  |  <= (less than or equal to comparison operator)   
> (greater than comparison operator)  |  > (greater than comparison operator)   
>= (greater than or equal to comparison operator)  |  >= (greater than or equal to comparison operator)   
And function  | 

C#
     && operator 
VB.NET
     And operator   
Eqv operator  | Not provided, use other bitwise comparison methods instead   
Imp operator  |  Not provided, use = comparison instead   
Is operator  | 

C#
     _object_ is _object_
VB.NET
     _object_ Is _object_  
IsArray function  | 

.NET
     _varName_.GetType().IsArray 
C#
     typeof(_arrayName_) == Array comparison 
VB.NET
     IsArray function  or  TypeOf _arrayName_ Is Array comparison   
IsNull function  | 

C#
     Use == null comparison 
VB.NET
     IsDBNull function   
Like operator  | 

.NET
     _stringVariable_.Contains function 
VB.NET
     Like operator   
Not operator  | 

C#
     != (not equal to comparison operator) 
VB.NET
     Not operator   
Or function  | 

C#
     || operator 
VB.NET
     Or function   
  
Data Conversion Functions   
---  
ActiveX, VBA, or Visual Basic 6  |  .NET equivalent (same unless noted)   
Asc function  | 

C#
     (int)’ _letter_ ’ 
VB.NET
     Asc function   
AutoCAD.Application.ActiveDocument.  Utility.AngleToReal method  |  Autodesk.AutoCAD.Runtime.Converter.  StringToAngle method   
AutoCAD.Application.ActiveDocument.  Utility.AngleToString method  |  Autodesk.AutoCAD.Runtime.Converter.  AngleToString method   
AutoCAD.Application.ActiveDocument.  Utility.RealToString method  |  Autodesk.AutoCAD.Runtime.Converter.  DistanceToString function   
CDbl Function  | 

.NET
     System.Convert.ToDouble function 
VB.NET
     CDbl function   
Chr function  | 

.NET
     System.Convert.ToChar 
VB.NET
     Chr function   
CInt Function  | 

.NET
     System.Convert.ToInt16, System.Convert.ToInt32, or System.Convert.ToInt64 function 
VB.NET
     CInt function   
Fix function  | 

.NET
     System.Convert.ToInt16, System.Convert.ToInt32, or System.Convert.ToInt64 function 
VB.NET
     Fix function   
Int function  | 

.NET
     System.Convert.ToInt16, System.Convert.ToInt32, or System.Convert.ToInt64 function 
VB.NET
     Int function   
Str function  | 

.NET
     System.Convert.ToString function 
VB.NET
     Str function   
StrConv function  | 

.NET
     System.Text.Encoding.Convert function 
VB.NET
     StrConv function   
  
Basic String Manipulation Functions   
---  
ActiveX, VBA, or Visual Basic 6  |  .NET equivalent (same unless noted)   
& operator (concatenate string)  | 

C#
     \+ operator 
VB.NET
     & or + operator   
Len function  | 

.NET
     _stringVariable_.Length property 
VB.NET
     Len function   
Mid function  | 

.NET
     _stringVariable_.Substring function 
VB.NET
     Mid function   
  
Get Input from the AutoCAD Command Prompt Functions   
---  
ActiveX, VBA, or Visual Basic 6  |  .NET equivalent (same unless noted)   
AutoCAD.Application.ActiveDocument.Utility.GetAngle method  |  Autodesk.AutoCAD.ApplicationServices.Application.DocumentManager.  MdiActiveDocument.Editor.GetAngle function   
AutoCAD.Application.ActiveDocument.Utility.GetCorner method  |  Autodesk.AutoCAD.ApplicationServices.Application.DocumentManager.  MdiActiveDocument.Editor.GetCorner function   
AutoCAD.Application.ActiveDocument.Utility.GetDistance method  |  Autodesk.AutoCAD.ApplicationServices.Application.DocumentManager.  MdiActiveDocument.Editor.GetDistance function   
AutoCAD.Application.ActiveDocument.Utility.GetEntity method  |  Autodesk.AutoCAD.ApplicationServices.Application.DocumentManager.  MdiActiveDocument.Editor.GetEntity function   
AutoCAD.Application.ActiveDocument.Utility.GetInteger method  |  Autodesk.AutoCAD.ApplicationServices.Application.DocumentManager.  MdiActiveDocument.Editor.GetInteger function   
AutoCAD.Application.ActiveDocument.Utility.GetKeyword method  |  Autodesk.AutoCAD.ApplicationServices.Application.DocumentManager.  MdiActiveDocument.Editor.GetKeyword function   
AutoCAD.Application.ActiveDocument.Utility.GetOrientation method  |  Autodesk.AutoCAD.ApplicationServices.Application.DocumentManager.  MdiActiveDocument.Editor.GetAngle function   
AutoCAD.Application.ActiveDocument.Utility.GetPoint method  |  Autodesk.AutoCAD.ApplicationServices.Application.DocumentManager.  MdiActiveDocument.Editor.GetPoint function   
AutoCAD.Application.ActiveDocument.Utility.GetReal method  |  Autodesk.AutoCAD.ApplicationServices.Application.DocumentManager.  MdiActiveDocument.Editor.GetDouble function   
AutoCAD.Application.ActiveDocument.Utility.GetString method  |  Autodesk.AutoCAD.ApplicationServices.Application.DocumentManager.  MdiActiveDocument.Editor.GetString function   
AutoCAD.Application.ActiveDocument.Utility.InitializeUserInput method  |  Autodesk.AutoCAD.EditorInput.PromptKeywordOptions function   
  
Basic AutoCAD Application and Drawing Functions   
---  
ActiveX, VBA, or Visual Basic 6  |  .NET equivalent (same unless noted)   
AutoCAD.Application.ActiveDocument.Utility.AngleFromXAxis method  |  Autodesk.AutoCAD.Geometry.Point2d(_point1_).GetVectorTo(_point2_).Angle property   
AutoCAD.Application.ListARX method  |  Autodesk.AutoCAD.Runtime.SystemObjects.DynamicLinker.GetLoadedModules function   
AutoCAD.Application.LoadARX method  |  Autodesk.AutoCAD.Runtime.SystemObjects.DynamicLinker.LoadModule function   
AutoCAD.Application.UnloadARX method  |  Autodesk.AutoCAD.Runtime.SystemObjects.DynamicLinker.UnloadModule function   
AutoCAD.Application.Documents.Close method  |  Autodesk.AutoCAD.ApplicationServices.Application.DocumentManager.  MdiActiveDocument.CloseAndDiscard function  or  Autodesk.AutoCAD.ApplicationServices.Application.DocumentManager.  MdiActiveDocument.CloseAndSave function   
AutoCAD.Application.ActiveDocument.SendCommand method  |  Autodesk.AutoCAD.ApplicationServices.Application.DocumentManager.  MdiActiveDocument.SendStringToExecute function   
AutoCAD.Application.ActiveDocument.Dictionaries.Add method  | 

C#
     _dictionaryObj_ = _transactionObj_.  GetObject(_workingDatabaseObj_.NamedObjectsDictionaryId, _openMode_) as Autodesk.AutoCAD.DatabaseServices.DBDictionary;  _dictionaryObj_.SetAt function 
VB.NET
     _dictionaryObj_ = _transactionObj_.  GetObject(_workingDatabaseObj_.NamedObjectsDictionaryId, _openMode_)  _dictionaryObj_.SetAt function   
AutoCAD.Application.ActiveDocument.Dictionaries.Item method  | 

C#
     _dictionaryObj_ = _transactionObj_.  GetObject(_workingDatabaseObj_. NamedObjectsDictionaryId, _openMode_) as Autodesk.AutoCAD.DatabaseServices.DBDictionary;  _dictionaryObj_.GetAt function 
VB.NET
     _dictionaryObj_ = _transactionObj_.  GetObject(_workingDatabaseObj_.NamedObjectsDictionaryId, _openMode_)  _dictionaryObj_.GetAt function   
AutoCAD.Application.ActiveDocument.ModelSpace property  | 

C#
     _blockTableObj_ = _transactionObj_.  GetObject(_workingDatabaseObj_.BlockTableId, _openMode_) as Autodesk.AutoCAD.DatabaseServices.BlockTable;  _blockTableRecordObj_ = _transactionObj_.  GetObject(_blockTableObj_[BlockTableRecord. ModelSpace], _openMode_) as Autodesk.AutoCAD.DatabaseServices.BlockTableRecord; 
VB.NET
     _blockTableObj_ = _transactionObj_.  GetObject(_workingDatabaseObj_.BlockTableId, _openMode_)  _blockTableRecordObj_ = _transactionObj_.  GetObject(_blockTableObj_(BlockTableRecord. ModelSpace), _openMode_)   
AutoCAD.Application.ActiveDocument.ModelSpace.Item method  | 

C#
     _blockTableObj_ = _transactionObj_.  GetObject(_workingDatabaseObj_.BlockTableId, _openMode_) as Autodesk.AutoCAD.DatabaseServices.BlockTable;  _blockTableRecordObj_ = _transactionObj_.  GetObject(_blockTableObj_[BlockTableRecord. ModelSpace], _openMode_) as Autodesk.AutoCAD.DatabaseServices.BlockTableRecord;  foreach(_objecId_ in _blockTableRecordObj_)  {  _objObject_ = _transactionObj_.GetObject(_objecId_);  } 
VB.NET
     _blockTableObj_ = _transactionObj_.  GetObject(_workingDatabaseObj_.BlockTableId, _openMode_)  _blockTableRecordObj_ = _transactionObj_.  GetObject(_blockTableObj_(BlockTableRecord. ModelSpace), _openMode_)  _dbObj_ = _blockTableRecordObj_(_index_)   
AutoCAD.Application.ActiveDocument.ModelSpace.Count property  | 

C#
     _blockTableObj_ = _transactionObj_.  GetObject(_workingDatabaseObj_.BlockTableId, _openMode_) as Autodesk.AutoCAD.DatabaseServices.BlockTable;  _blockTableRecordObj_ = _transactionObj_.  GetObject(_blockTableObj_[BlockTableRecord. ModelSpace], _openMode_) as Autodesk.AutoCAD.DatabaseServices.BlockTableRecord;  int cnt = 0;  foreach(_objectId_ in _blockTableRecordObj_)  {  cnt = cnt + 1;  } 
VB.NET
     _blockTableObj_ = _transactionObj_.  GetObject(_workingDatabaseObj_.BlockTableId, _openMode_)  _blockTableRecordObj_ = _transactionObj_.  GetObject(_blockTableObj_(BlockTableRecord. ModelSpace), _openMode_)  Dim _nCount_ As Integer = 0  For Each _objectId_ In _blockTableRecordObj_ _nCount_ = _nCount_ \+ 1  Next   
AutoCAD.Application.ActiveDocument.  ModelSpace.Add<entityname> method  | 

C#
     _blockTableObj_ = _transactionObj_.  GetObject(_workingDatabaseObj_.BlockTableId, _openMode_) as Autodesk.AutoCAD.DatabaseServices.BlockTable;  _blockTableRecordObj_ = _transactionObj_.  GetObject(_blockTableObj_[BlockTableRecord. ModelSpace], _openMode_) as Autodesk.AutoCAD.DatabaseServices.BlockTableRecord;  _blockTableRecordObj_.AppendEntity(_someEntity_);  _transactionObj_.AddNewlyCreatedDBObject(_someEntity_ , true); 
VB.NET
     _blockTableObj_ = _transactionObj_.  GetObject(_workingDatabaseObj_.BlockTableId, _openMode_)  _blockTableRecordObj_ = _transactionObj_.  GetObject(_blockTableObj_(BlockTableRecord. ModelSpace), _openMode_)  _blockTableRecordObj_.AppendEntity(_someEntity_)  _transactionObj_.AddNewlyCreatedDBObject(_someEntity_ , True)   
AutoCAD.Application.ActiveDocument.ActiveSpace property  | 

C#
     _blockTableRecordObj_ = _transactionObj_.  GetObject(_workingDatabaseObj_.CurrentSpaceId, _openMode_) as Autodesk.AutoCAD.DatabaseServices.BlockTableRecord; 
VB.NET
     _blockTableRecordObj_ = _transactionObj_.  GetObject(_workingDatabaseObj_.CurrentSpaceId, _openMode_)   
AutoCAD.Application.ActiveDocument.PaperSpace property  | 

C#
     _blockTableObj_ = _transactionObj_.  GetObject(_workingDatabaseObj_.  BlockTableId, _openMode_) as Autodesk.AutoCAD.DatabaseServices.BlockTable;  _blockTableRecordObj_ = _transactionObj_.  GetObject(_blockTableObj_[BlockTableRecord. PaperSpace], _openMode_) as Autodesk.AutoCAD.DatabaseServices.BlockTableRecord; 
VB.NET
     _blockTableObj_ = _transactionObj_.  GetObject(_workingDatabaseObj_.BlockTableId, _openMode_)  _blockTableRecordObj_ = _transactionObj_.GetObject(_blockTableObj_ (BlockTableRecord. PaperSpace), _openMode_)   
AutoCAD.Application.ActiveDocument.ActiveLayout property  | 

C#
     _layoutObj_ = _transactionObj_.  GetObject(_layoutManagerObj_.GetLayoutId(_layoutManagerObj_.CurrentLayout), _openMode_) as Autodesk.AutoCAD.DatabaseServices.Layout;  _blockTableRecordObj_ = _transactionObj_.  GetObject(_layoutObj_.BlockTableRecordId,_openMode_) as Autodesk. AutoCAD.DatabaseServices.BlockTableRecord; 
VB.NET
     _layoutObj_ = _transactionObj_.  GetObject(_layoutManagerObj_.GetLayoutId(_layoutManagerObj_.CurrentLayout), _openMode_)  _blockTableRecordObj_ = _transactionObj_.  GetObject(_layoutObj_.BlockTableRecordId, _openMode_)   
AutoCAD.Application.ActiveDocument.PurgeAll method  |  HostApplicationServices.WorkingDatabase.Purge method   
AutoCAD.Application.GetVariable method  |  Autodesk.AutoCAD.ApplicationServices.Application.  GetSystemVariable function   
AutoCAD.Application.MenuBar property  |  Autodesk.AutoCAD.ApplicationServices.Application.  MenuBar property   
AutoCAD.Application.MenuGroup property  |  Autodesk.AutoCAD.ApplicationServices.Application.  MenuGroups property   
AutoCAD.Application.ActiveDocument.PickfirstSelectionSet property  |  Autodesk.AutoCAD.ApplicationServices.Application.  DocumentManager.MdiActiveDocument.Editor.SelectImplied function   
AutoCAD.Application.ActiveDocument.Utility.PolarPoint method  |  Not provided, use the Point2d and Point3d classes from the Geometry namespace to calculate a new point   
AutoCAD.Application.Preferences property  |  Autodesk.AutoCAD.ApplicationServices.Application.Preferences property   
AutoCAD.Application.ActiveDocument.  Utility.Prompt method  |  Autodesk.AutoCAD.ApplicationServices.Application.  DocumentManager.MdiActiveDocument.Editor.WriteMessage method   
AutoCAD.Application.Quit method  |  Autodesk.AutoCAD.ApplicationServices.Application.Quit method   
AutoCAD.Application.ActiveDocument.  SelectionSets.Add method  |  Not needed/provided   
AutoCAD.Application.ActiveDocument.  SelectionSets.SelectionSet.Item method  |  Autodesk.AutoCAD.EditorInput.SelectionSet.  _selectionSet_.Item(_object_) method   
AutoCAD.Application.ActiveDocument.  SelectionSets.SelectionSet.Delete method  |  Autodesk.AutoCAD.EditorInput.SelectionSet.  _selectionSet_.Item(_object_).Delete method   
AutoCAD.Application.ActiveDocument.  SelectionSets.SelectionSet.SelectOnScreen method  |  Autodesk.AutoCAD.ApplicationServices.Application.  DocumentManager.MdiActiveDocument.Editor.GetSelection method   
AutoCAD.Application.ActiveDocument.  SelectionSets.SelectionSet.Count property  |  Autodesk.AutoCAD.EditorInput.SelectionSet.  _selectionSet_.Count property   
AutoCAD.Application.ActiveDocument.  SelectionSets.SelectionSet.SelectAtPoint method  |  Autodesk.AutoCAD.ApplicationServices.Application.DocumentManager.  MdiActiveDocument.Editor.SelectCrossingWindow method   
AutoCAD.Application.SetVariable method  |  Autodesk.AutoCAD.ApplicationServices.Application.  SetSystemVariable method   
AutoCAD.Application.ActiveDocument.  Utility.TranslateCoordinates method  |  Not provided, use the Matrix3d class from the Geometry namespace to translate points between different coordinate systems   
AutoCAD.Application.Version property  |  Autodesk.AutoCAD.ApplicationServices.Application.Version property   
ThisDrawing  |  Autodesk.AutoCAD.ApplicationServices.Application.DocumentManager.  MdiActiveDocument property  and  HostApplicationServices.WorkingDatabase property   
  
Basic VBA and Visual Basic 6 Functions and Statements   
---  
ActiveX, VBA, or Visual Basic 6  |  .NET equivalent (same unless noted)   
AppActivate AutoCAD.Application.Caption function  | 

.NET
     Use the Win32 Calls ShowWindow and SetWindowPos 
VB.NET
     AppActivate Autodesk.AutoCAD.  ApplicationServices.Application.  MainWindow.Text   
Dir function  |  System.IO.Directory.Exists function   
Error object/method/properties  | 

.NET
     Try Catch statement with exception handling 
VB.NET
     Error object/method/properties   
Function and End Function keywords  | 

C#
     Define a procedure and use _return_ to return a value 
VB.NET
     Function and End Function keywords and use _Return_ to return a value   
Input function  | 

.NET
     _fileStream_.Read method 
VB.NET
     Input method   
LBound(_arrayName_) function  | 

.NET
     _arrayName_.GetLowerBound function 
VB.NET
     LBound(_arrayName_) function   
Line Input function  | 

.NET
     _fileStream_.Read method 
VB.NET
     LineInput method   
MsgBox function  |  MessageBox.Show method   
object(n) syntax  | 

C#
     object[n] syntax 
VB.NET
     object(n) syntax   
Open function  |  System.IO.File.Open function   
ReDim statement  | 

.NET
     _arrayName_.Resize 
VB.NET
     ReDim _arrayName_(_newSize_)   
Set statement  |  Not needed/provided   
Shell function  | 

.NET
     System.Diagnostics.Process.Start function 
VB.NET
     Shell function   
Sub and End Sub keywords  | 

C#
     Define a procedure 
VB.NET
     Sub and End Sub keywords   
TypeName function  | 

.NET
     _varName_.GetType().Name or  _varName_.GetType().FullName functions 
VB.NET
     TypeName function   
UBound(_arrayName_) function  | 

.NET
     _arrayName_.GetUpperBound function 
VB.NET
     UBound(_arrayName_) function
