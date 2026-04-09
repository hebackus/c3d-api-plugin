<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Use Events (.NET) > Register and Unregister Events (.NET) > Handle Document Events (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-F432E285-8B94-4ACD-A186-89E1218DEC07.htm -->

# Handle Document Events (.NET)

Document object events are used to respond to the document window. When a document event is registered, it is only associated with the document object in which it is associated. So if an event needs to be registered with each document, you will want to use the DocumentCreated event of the DocumentCollection object to register events with each new or opened drawing. 

The following events are available for Document objects: 

BeginDocumentClose
    

Triggered just after a request is received to close a drawing. 

BeginDwgOpen
    

Triggered when a drawing is about to be opened. 

CloseAborted
    

Triggered when an attempt to close a drawing is aborted. 

CloseWillStart
    

Triggered after the BeginDocumentClose event and before closing the drawing begins. 

CommandCancelled
    

Triggered when a command is cancelled before it completes. 

CommandEnded
    

Triggered immediately after a command completes. 

CommandFailed
    

Triggered when a command fails to complete and is not cancelled. 

CommandWillStart
    

Triggered immediately after a command is issued, but before it completes. 

EndDwgOpen
    

Triggered when a drawing has been opened. 

ImpliedSelectionChanged
    

Triggered when the current pickfirst selection set changes. 

LayoutSwitched
    

Triggered after a layout has been set current. 

LayoutSwitching
    

Triggered after a layout is being set current. 

LispCancelled
    

Triggered when the evaluation of a LISP expression is canceled. 

LispEnded
    

Triggered upon completion of evaluating a LISP expression. 

LispWillStart
    

Triggered immediately after AutoCAD receives a request to evaluate a LISP expression. 

UnknownCommand
    

Triggered immediately when an unknown command is entered at the Command prompt. 

ViewChanged
    

Triggered after the view of a drawing has changed. 

## Enable a Document object event

The following example uses the BeginDocumentClose event to prompt the user if they want to continue closing the current drawing. A message box is displayed with the Yes and No buttons. Clicking No aborts the closing of the drawing by using the Veto method of the arguments that are returned by the event handler. 

### C#
    
    
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
     
    [CommandMethod("AddDocEvent")]
    public void AddDocEvent()
    {
      // Get the current document
      Document acDoc = Application.DocumentManager.MdiActiveDocument;
     
      acDoc.BeginDocumentClose += 
          new DocumentBeginCloseEventHandler(docBeginDocClose);
    }
     
    [CommandMethod("RemoveDocEvent")]
    public void RemoveDocEvent()
    {
      // Get the current document
      Document acDoc = Application.DocumentManager.MdiActiveDocument;
     
      acDoc.BeginDocumentClose -=
          new DocumentBeginCloseEventHandler(docBeginDocClose);
    }
     
    public void docBeginDocClose(object senderObj, 
                                 DocumentBeginCloseEventArgs docBegClsEvtArgs)
    {
      // Display a message box prompting to continue closing the document
      if (System.Windows.Forms.MessageBox.Show(
                           "The document is about to be closed." +
                           "\nDo you want to continue?",
                           "Close Document",
                           System.Windows.Forms.MessageBoxButtons.YesNo) ==
                           System.Windows.Forms.DialogResult.No)
      {
          docBegClsEvtArgs.Veto();
      }
    }

### VB.NET
    
    
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
     
    <CommandMethod("AddDocEvent")> _
    Public Sub AddDocEvent()
      '' Get the current document
      Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
     
      AddHandler acDoc.BeginDocumentClose, AddressOf docBeginDocClose
    End Sub
     
    <CommandMethod("RemoveDocEvent")> _
    Public Sub RemoveDocEvent()
      '' Get the current document
      Dim acDoc As Document = Application.DocumentManager.MdiActiveDocument
     
      RemoveHandler acDoc.BeginDocumentClose, AddressOf docBeginDocClose
    End Sub
     
    Public Sub docBeginDocClose(ByVal senderObj As Object, _
                                ByVal docBegClsEvtArgs As DocumentBeginCloseEventArgs)
     
      '' Display a message box prompting to continue closing the document
      If System.Windows.Forms.MessageBox.Show( _
                          "The document is about to be closed." & _
                          vbLf & "Do you want to continue?", _
                          "Close Document", _
                          System.Windows.Forms.MessageBoxButtons.YesNo) = _
                          System.Windows.Forms.DialogResult.No Then
          docBegClsEvtArgs.Veto()
      End If
    End If

### VBA/ActiveX Code Reference
    
    
    Private Sub AcadDocument_BeginDocClose(Cancel As Boolean)
        ' This procedure intercepts the Document BeginDocClose event.
     
        If MsgBox("The document is about to be closed." & _
                  vbLf & "Do you want to continue?", vbYesNo, _
                  "Close Document") = vbNo Then
     
               ' Veto the document close
               Cancel = True
        End If
    End Sub
