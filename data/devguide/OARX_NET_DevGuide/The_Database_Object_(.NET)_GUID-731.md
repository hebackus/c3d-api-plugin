<!-- ObjectARX and Managed .NET > ObjectARX: Managed .NET Developer's Guide > Basics of the AutoCAD .NET API (.NET) > Understand the AutoCAD Object Hierarchy (.NET) > The Database Object (.NET) -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/OARX-DevGuide-Managed/files/GUID-7313ECA1-4875-4946-82E3-C06A4074F807.htm -->

# The Database Object (.NET)

The Database object contains all of the graphical and most of the non-graphical AutoCAD objects. Some of the objects contained in the database are entities, symbol tables, and named dictionaries. Entities in the database represent graphical objects within a drawing. Lines, circles, arcs, text, hatch, and polylines are examples of entities. A user can see an entity on the screen and can manipulate it. 

You access the Database object for the current document by the Document object’s Database member property. 
    
    
    Application.DocumentManager.MdiActiveDocument.Database

## Symbol Tables and Dictionaries

Symbol table and dictionary objects provide access to non-graphical objects (blocks, layers, linetypes, layouts, and so forth). Each drawing contains a set of nine fixed symbol tables, whereas the number of dictionaries in a drawing can vary based on the features and types of applications used in AutoCAD. New symbol tables cannot be added to a database. 

Examples of symbol tables are the layer table (_LayerTable_), which contains layer table records, and the block table (_BlockTable_), which contains block table records. All graphical entities (lines, circles, arcs, and so forth) are owned by a block table record. By default, every drawing contains predefined block table records for Model and Paper space. Each Paper space layout has its own block table record. 

A dictionary is a container object which can contain any AutoCAD object or an XRecord. Dictionaries are stored either in the database under the named object dictionary or as an extension dictionary of a table record or graphical entity. The named object dictionary is the master table for all of the dictionaries associated with a database. Unlike symbol tables, new dictionaries can be created and added to the named object dictionary. 

Note: Dictionary objects cannot contain drawing entities. 

## VBA/ActiveX Cross Reference

The Database object in the AutoCAD .NET API is similar to the Document object in the ActiveX Automation library. To access most of the properties that are available in the Document object of the ActiveX Automation library, you will need to work with the Document and Database objects of the AutoCAD .NET API.
