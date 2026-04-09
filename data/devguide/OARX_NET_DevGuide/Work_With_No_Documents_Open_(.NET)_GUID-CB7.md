<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Control the AutoCAD Environment (.NET) > Create, Open, Save, and Close Drawings (.NET) > Work With No Documents Open (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-CB7D7DC2-C8C1-4EF9-A638-C4C6184BFC85.htm -->

# Work With No Documents Open (.NET)

AutoCAD always starts up with a new or existing document open. It is possible, however, to close all documents during the current session. 

If you close all the documents in the AutoCAD user interface, you will notice a few changes to the application window. The Quick Access toolbar and application menu offer limited options. These limited options are related to creating and opening drawings, displaying the Sheet Set Manager, and recovering drawings. If the menu bar is displayed, simplified File, View, Window, and Help menus are also displayed. You will also notice that there is no command line. 

When working in zero document state, you can do the following: 

  * You can create a new or open an existing document 
  * You can customize the zero document states of the application menu and menu bar 
  * You can shutdown AutoCAD 

To react to AutoCAD when it enters zero document state, you should use the DocumentDestroyed event. The DocumentDestroyed event is triggered when an open document is closed. The document count when the last document is closed will be 1. Use the Count property of the DocumentManager to determine the number of open documents at the time the DocumentDestroyed event is triggered. 

## Customize the application menu

This example code uses the DocumentDestroyed event to monitor when the last drawing is closed and when zero document state is entered. Once zero document state is entered, the Opening event is registered with the application menu. When the application menu is clicked, the Opening event is triggered. During the Opening event, a new menu item is added to the application menu. The new menu item displays a message box. 

Note: You must reference _AdWindows.dll_ to your project in order to use the following example code. _AdWindows.dll_ contains the namespace used to customize the application menu and can be found in the install folder of AutoCAD or part of the ObjectARX SDK. You will also need to reference WindowsBase which can be found on the AutoCAD .NET tab of the Add Reference dialog box. 

### C#
    
    
    using Autodesk.Windows;
    using Autodesk.AutoCAD.Runtime;
    using Autodesk.AutoCAD.ApplicationServices;
     
    // Create the command handler for the custom  application menu item
    public class MyCommandHandler : System.Windows.Input.ICommand
    {
        public bool CanExecute(object parameter)
        {
            return true;
        }
     
        public event EventHandler CanExecuteChanged;
     
        public void Execute(object parameter)
        {
            Application.ShowAlertDialog("MyMenuItem has been clicked");
        }
    }
     
    class Chapter4
    {
        //Global var for ZeroDocState
        ApplicationMenuItem acApMenuItem = null;
     
        [CommandMethod("AddZeroDocEvent")]
        public void AddZeroDocEvent()
        {
            // Get the DocumentCollection and register the DocumentDestroyed event
            DocumentCollection acDocMgr = Application.DocumentManager;
            acDocMgr.DocumentDestroyed += 
                new DocumentDestroyedEventHandler(docDestroyed);
        }
     
        public void docDestroyed(object obj, 
                                 DocumentDestroyedEventArgs acDocDesEvtArgs)
        {
            // Determine if the menu item already exists and the number of documents open
            if (Application.DocumentManager.Count == 1 && acApMenuItem == null)
            {
                // Add the event handler to watch for when the application menu is opened
                // AdWindows.dll must be referenced to the project
                ComponentManager.ApplicationMenu.Opening += 
                    new EventHandler<EventArgs>(ApplicationMenu_Opening);
            }
        }
     
        void ApplicationMenu_Opening(object sender, EventArgs e)
        {
            // Check to see if the custom menu item was added previously
            if (acApMenuItem == null)
            {
                // Get the application menu component
                ApplicationMenu acApMenu = ComponentManager.ApplicationMenu;
     
                // Create a new application menu item
                acApMenuItem = new ApplicationMenuItem();
                acApMenuItem.Text = "MyMenuItem";
                acApMenuItem.CommandHandler = new MyCommandHandler();
     
                // Append the new menu item
                acApMenu.MenuContent.Items.Add(acApMenuItem);
     
                // Remove the application menu Opening event handler
                ComponentManager.ApplicationMenu.Opening -= 
                    new EventHandler<EventArgs>(ApplicationMenu_Opening);
            }
        }
    }

### VB.NET
    
    
    Imports System.Windows.Input
     
    Imports Autodesk.Windows
    Imports Autodesk.AutoCAD.Runtime
    Imports Autodesk.AutoCAD.ApplicationServices
     
    '' Create the command handler for the custom application menu item
    Public Class MyCommandHandler
        Implements ICommand
     
        Event CanExecuteChanged(ByVal sender As Object, ByVal e As EventArgs) _
                                             Implements ICommand.CanExecuteChanged
     
        Function CanExecute(ByVal parameter As Object) As Boolean _
                                            Implements ICommand.CanExecute
            Return True
        End Function
     
        Sub Execute(ByVal parameter As Object) Implements ICommand.Execute
            Application.ShowAlertDialog("MyMenuItem has been clicked")
        End Sub
    End Class
     
    Public Class Chapter4
        ''Global var for ZeroDocState
        Dim acApMenuItem As ApplicationMenuItem = Nothing
     
        <CommandMethod("AddZeroDocEvent")> _
        Public Sub AddZeroDocEvent()
            '' Get the DocumentCollection and register the DocumentDestroyed event
            Dim acDocMgr As DocumentCollection = Application.DocumentManager
            AddHandler acDocMgr.DocumentDestroyed, AddressOf docDestroyed
        End Sub
     
        Public Sub docDestroyed(ByVal obj As Object, _
                                ByVal acDocDesEvtArgs As DocumentDestroyedEventArgs)
            '' Determine if the menu item already exists and the number of documents open
            If Application.DocumentManager.Count = 1 And IsNothing(acApMenuItem) Then
                '' Add the event handler to watch for when the application menu is opened
                '' AdWindows.dll must be referenced to the project
                AddHandler ComponentManager.ApplicationMenu.Opening, _
                           AddressOf ApplicationMenu_Opening
            End If
        End Sub
     
        Public Sub ApplicationMenu_Opening(ByVal sender As Object, _
                                           ByVal e As EventArgs)
            '' Check to see if the custom menu item was added previously
            If IsNothing(acApMenuItem) Then
                '' Get the application menu component
                Dim acApMenu As ApplicationMenu = ComponentManager.ApplicationMenu
     
                '' Create a new application menu item
                acApMenuItem = New ApplicationMenuItem()
                acApMenuItem.Text = "MyMenuItem"
                acApMenuItem.CommandHandler = New MyCommandHandler()
     
                '' Append the new menu item
                acApMenu.MenuContent.Items.Add(acApMenuItem)
     
                '' Remove the application menu Opening event handler
                RemoveHandler ComponentManager.ApplicationMenu.Opening, _
                              AddressOf ApplicationMenu_Opening
            End If
        End Sub
    End Class
