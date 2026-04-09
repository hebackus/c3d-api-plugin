<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Customize User Interface (CUI) Managed API (.NET) > Customization Sections (.NET) > Ribbon Elements (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-01548FB4-7DE1-4025-B4C6-5E33D3530E15.htm -->

# Ribbon Elements (.NET)

The ribbon provides a location for tools that are frequently accessed and relevant to the current workspace. 

It is organized in to tabs, which are like menus on a toolbar. Each tabs contains one or more panels of which contain items that perform different operations. 

Autodesk.Windows is the managed namespace which contains classes and enumerations associated with the ribbon. 

## Tabs

Tabs are the initial navigation interface within a ribbon. The RibbonTab class used to create tabs. 

There are two types: 

  * **ActiveTab** \- This represents a tab that is currently selected. 
  * **ActiveContextualTab** \- This represents a tab that is displayed only when a particular type of AutoCAD object, such as a hatch or a table, is included in the selection. 

## Panels

A panel contains all the tools associated with a tab. Classes with the prefix RibbonPanel control the various aspects of a panel, such as its visibility, its size, and its floating location. 

RibbonRow objects define rows within the panel where items are placed. These rows are added to a RibbonPanelSource object, which contains the panel definition for panels displayed in the ribbon. 

## Items

Items may be one of two things. They could be the individual tools contained within a panel—such as buttons (RibbonButton) or forms (RibbonForm); or they could a visual divider—such as a row panel (RibbonRowPanel) or a separator (RibbonSeparator). RibbonItem is the parent class for both these types. 

Within the items themselves exist other subclasses, such as RibbonDropDownButton, RibbonMenuButton, or RibbonToggleButton underneath RibbonButton. For more information on these subtypes, see the ObjectARX Managed Class Reference Guide. 

## Ribbon Creation Sample

The following is sample code that creates and populates a Ribbon object. The important information here is to follow the hierarchy of construction, e.g. an item must be added to a panel, which must be added to a tab. There are a number of customizable properties available to ribbons as well, such as title text, size, orientation, tooltips, and the image to be displayed. 

### C#
    
    
    // First, the button items are created:
    RibbonButton button1 = new RibbonButton;
    button1.Text = "Button1";
    
    RibbonButton button2 = new RibbonButton;
    button2.Text = "Button2";
    
    // These are then added to a row:
    RibbonRow row = new RibbonRow();
    row.RowItems.Add(button1);
    row.RowItems.Add(button2);
    
    // This row is added to a panel source, which is then added to a panel:
    RibbonPanelSource panelSource = new RibbonPanelSource();
    panelSource.Title = "Panel1";
    panelSource.Rows.Add(row);
    
    RibbonPanel panel = new RibbonPanel();
    panel.Source = panelSource;
    
    // Last, the panel is added to a tab, which is added to the ribbon:
    RibbonTab tab = new RibbonTab();
    tab.Title = "Tab1";
    tab.Panels.Add(panel);
    
    RibbonControl ribbon = new RibbonControl();
    ribbon.Tabs.Add(tab);

### VB.NET
    
    
    '' First, the button items are created:
    Dim button1 As RibbonButton = New RibbonButton()
    button1.Text = "Button1"
    
    Dim button2 As RibbonButton = New RibbonButton()
    button2.Text = "Button2"
    
    '' These are then added to a row:
    Dim row As RibbonRow = New RibbonRow()
    row.RowItems.Add(button1)
    row.RowItems.Add(button2)
    
    '' This row is added to a panel source, which is then added to a panel:
    Dim panelSource As RibbonPanelSource = New RibbonPanelSource()
    panelSource.Title = "Panel1"
    panelSource.Rows.Add(row)
    
    Dim panel As RibbonPanel = New RibbonPanel()
    panel.Source = panelSource
    
    '' Last, the panel is added to a tab, which is added to the ribbon:
    Dim tab As RibbonTab = New RibbonTab()
    tab.Title = "Tab1"
    tab.Panels.Add(panel)
    
    Dim ribbon As RibbonControl = New RibbonControl()
    ribbon.Tabs.Add(tab)
