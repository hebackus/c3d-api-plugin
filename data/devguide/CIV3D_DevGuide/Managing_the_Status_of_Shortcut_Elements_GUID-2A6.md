<!-- Developer's Guide > API Developer's Guide > Data Shortcuts > Managing the Status of Shortcut Elements -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-2A64D878-4AD4-4236-8A88-CAD89EAB9419.htm -->

# Managing the Status of Shortcut Elements

The DataShortcutManager API class replicates the functionality found in the Data Shortcut Manager dialog box using the following methods: 

  * **GetExportableItemCount()**. Returns the number of exportable objects that can be set as data shortcuts. 
  * **String GetItemAt(int index)**. Returns the object name at the index position in the list of items. 
  * **List <int> GetDependentItemsIndexList(int index)**. Returns the list of items that must be exported if an item at the index position is exported. This is likely the list of all parent/grandparent objects. For example, if a profile is selected to export, then its parent alignment would be in the list. 
  * **int GetParentItemIndex(int index)**. Returns the parent of the item at the index position. For example, if a profile is selected, then the parent would be the alignment. 
  * **List <int> GetDirectChildrenItemIndexList(int index)**. Returns the list of direct children to the item at the index position. 
  * **List <int> GetRecursiveChildrenItemsIndexList(int index)**. Returns the list of all descendants of the item at the index position. The complete descendent tree is then exposed in list form for convenience. 
  * **List <int> GetCurrentlySelectedItemsIndexList()**. Returns the subset of referenced objects from the list of all exportable objects in a data shortcut. 
  * **bool IsItemAtIndexAlreadyPublished(int index)**. Returns true if an object is already a data shortcut, and false if otherwise. 

Note: The DataShortcutManager class does not manage broken links, because this process requires searching and browsing folders to locate correct drawings and files. When a broken link is encountered, the API will throw an exception. When programming with the DataShortcutManager it is important to account for this. Show a message box or an error message to prompt that broken links should be repaired with the user-interface before running the plugin again. Once the links are repaired, the API methods should work properly again.
