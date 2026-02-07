###############################################################################
# This script creates a menu to host different tools for Substance 3D Painter
# ___________________
# Copyright 2024 Vincent GAULT - Adobe
# All Rights Reserved.
###############################################################################

"""
This module creates a menu to host various tools for Substance Painter.
"""

__author__ = "Vincent GAULT - Adobe"

# Modules import
from PySide6 import QtWidgets, QtGui
from PySide6.QtGui import QKeySequence
import importlib

import substance_painter

from substance_painter import ui, logging, layerstack
from vg_pt_utils import vg_baking, vg_export, vg_layerstack, vg_project_info, mh_scripts

plugin_menus_widgets = []
"""Keeps track of added UI elements for cleanup."""

######## FILL LAYER FUNCTIONS ########

def new_fill_layer_base():
    """Create a new fill layer with Base Color activated."""
    layer_manager = vg_layerstack.LayerManager()
    layer_manager.add_layer(layer_type='fill', active_channels=["BaseColor"], layer_name="New fill layer")

def new_fill_layer_height():
    """Create a new fill layer with Height channel activated."""
    layer_manager = vg_layerstack.LayerManager()
    layer_manager.add_layer(layer_type='fill', active_channels=["Height"], layer_name="New fill layer")

def new_fill_layer_all():
    """Create a new fill layer with all channels activated."""
    layer_manager = vg_layerstack.LayerManager()
    layer_manager.add_layer(layer_type='fill', layer_name="New fill layer")
    

def new_fill_layer_empty():
    """Create a new fill layer with no channels activated."""
    layer_manager = vg_layerstack.LayerManager()
    layer_manager.add_layer(layer_type='fill', active_channels=[""], layer_name="New fill layer")


######## PAINT LAYER FUNCTIONS ########    

def new_paint_layer():
    """Create a new paint layer."""
    layer_manager = vg_layerstack.LayerManager()
    layer_manager.add_layer(layer_type='paint', layer_name="New Paint layer")

######## MASK FUNCTIONS ########

def add_mask():
    """Add a black mask to the selected layer."""
    layer_manager = vg_layerstack.LayerManager()
    mask_manager = vg_layerstack.MaskManager(layer_manager)
    mask_manager.add_mask()

def add_ao_mask():
    """Add a black mask with AO Generator."""
    layer_manager = vg_layerstack.LayerManager()
    mask_manager = vg_layerstack.MaskManager(layer_manager)
    mask_manager.add_black_mask_with_ao_generator()

def add_curvature_mask():
    """Add a black mask with Curvature Generator."""
    layer_manager = vg_layerstack.LayerManager()
    mask_manager = vg_layerstack.MaskManager(layer_manager)
    mask_manager.add_black_mask_with_curvature_generator()

def add_color_select_mask():
    """Add a black mask with Color Selection filter."""
    layer_manager = vg_layerstack.LayerManager()
    mask_manager = vg_layerstack.MaskManager(layer_manager)
    mask_manager.add_black_mask_with_color_select()

def add_mask_with_fill_effect():
    """Add a mask with a fill effect."""
    layer_manager = vg_layerstack.LayerManager()
    mask_manager = vg_layerstack.MaskManager(layer_manager)
    mask_manager.add_mask_with_fill()


################ GENERATE CONTENT FROM STACK #######################    

def create_layer_from_stack():
    """Generate a layer from the visible content in the stack."""
    vg_export.create_layer_from_stack()
    

def flatten_stack():
    """Flatten the stack by exporting and importing textures."""    
    vg_export.flatten_stack()


############## CREATE REFERENCE POINT LAYER ####################### 

def create_ref_point_layer():
    """Create a reference point layer."""
    stack_manager = vg_layerstack.LayerManager()
    stack_manager.generate_ref_point_layer()


########################### QUICK BAKE ########################### 

def launch_quick_bake():
    """Quickly bake mesh maps of the current texture set."""
    vg_baking.quick_bake()
    
########################### DEBUG PRINTS ######################### <<<<<<<<<<<<<<<<<<

def print_layerstack_attributes():
    """Print all attributes in layerstack module that don't start with __"""
    print("--- Available Attributes in Layerstack ---")
    for attribute in dir(layerstack):
        if not attribute.startswith("__"):
            print(attribute)
    

def help_insert_color_selection_effect():
    """Print help for layerstack.insert_color_selection_effect"""
    try:
        # Use the discovered name
        # We rely on the API to act on the 'current context' if no args are mandatory
        # OR we try to pass the arguments revealed by the "TypeError Trick" above.
        
        # HYPOTHESIS: It needs the layer/mask to insert INTO.
        # Let's try to get the current selection first (if the API supports it)
        
        # This is a brute force dump to find the syntax:
        help(layerstack.insert_color_selection_effect) 
        
    except Exception as e:
        print(e)

def help_layerstack_attributes_A():
    attributes_to_check = [
        "insert_color_selection_effect",
        "InsertPosition",
        "NodeStack",
        "get_selection_type",
        "get_selection_type",
        "instantiate",
        "levels",
        "GeometryMaskType",
        "ScaleMode",
    ]
    for attr in attributes_to_check:
        try:
            print(f"Help for layerstack.{attr}:")
            help(getattr(layerstack, attr))
            print("\n")
        except AttributeError:
            print(f"Attribute {attr} not found in layerstack.")

def print_nodetype_attributes():
    """Print all attributes of the layerstack.NodeType Enum."""

    print("--- Available NodeType Attributes ---")
    # Iterate over the Enum members
    for name, member in layerstack.NodeType.__members__.items():
        print(f"{name}: {member.value}")

    # Fallback: Print raw dir() if it's not a standard python Enum
    print("\n--- Raw Attributes ---")
    for attr in dir(layerstack.NodeType):
        if not attr.startswith("__"):
            print(attr)

def print_NodeType_attributes():
    """Print all attributes of the layerstack.NodeType."""
    print("--- Available NodeType Attributes ---")
    for attr in dir(layerstack.NodeType):
        if not attr.startswith("__"):
            print(attr)
            # [Python] AttributeError: type object '_substance_painter.layerstack.NodeType' has no attribute 'PaintLayerNode'. Did you mean: 'PaintLayer'?

def run_mh_script_test():
    """Run the MH script test for inserting color selection effect"""
    mh_scripts.mh_script_test()
    

def run_mh_black_mask_color_select():
    """Run MH black mask with color select using MaskManager_mh"""
    layer_manager = vg_layerstack.LayerManager()
    mask_manager_mh = mh_scripts.MaskManager_mh(layer_manager)
    mask_manager_mh.mh_add_black_mask_with_color_select()

def run_mh_add_paint_mask_effect():
    """Run MH add paint mask effect using MaskManager_mh"""
    layer_manager = vg_layerstack.LayerManager()
    mask_manager_mh = mh_scripts.MaskManager_mh(layer_manager)
    mask_manager_mh.mh_add_paint_mask_effect()

def run_test_has_mask_attribute():
    layer_manager = vg_layerstack.LayerManager()
    mask_manager_mh = mh_scripts.MaskManager_mh(layer_manager)
    mask_manager_mh.test_has_mask_attribute()

def run_insert_paint_layer_mask_dynamic():
    layer_manager = vg_layerstack.LayerManager()
    mask_manager_mh = mh_scripts.MaskManager_mh(layer_manager)
    mask_manager_mh.insert_mask_effect_dynamic(effectType="Paint")

def run_insert_fill_layer_mask_dynamic():
    layer_manager = vg_layerstack.LayerManager()
    mask_manager_mh = mh_scripts.MaskManager_mh(layer_manager)
    mask_manager_mh.insert_mask_effect_dynamic(effectType="Fill")

def run_insert_levels_layer_mask_dynamic():
    layer_manager = vg_layerstack.LayerManager()
    mask_manager_mh = mh_scripts.MaskManager_mh(layer_manager)
    mask_manager_mh.insert_mask_effect_dynamic(effectType="Levels")

def run_insert_color_selection_layer_mask_dynamic():
    layer_manager = vg_layerstack.LayerManager()
    mask_manager_mh = mh_scripts.MaskManager_mh(layer_manager)
    mask_manager_mh.insert_mask_effect_dynamic(effectType="Color Selection")



def print_enum_selection_type():
    print("--- SelectionType Options ---")
    for name, member in layerstack.SelectionType.__members__.items():
        print(f"layerstack.SelectionType.{name}")

    print("\n--- Function Signature ---")
    help(layerstack.set_selection_type)

def print_ui_modules():
    print("--- Root Modules ---")
    # Check if there is anything like 'display', 'view', 'viewport' in the main package
    for item in dir(substance_painter):
        if not item.startswith("__"):
            print(item)

    print("\n--- UI Module Attributes ---")
    # Check if the UI module has viewport controls
    for item in dir(ui):
        print(item)

def print_display_modules():
    import substance_painter.display as display

    print("--- Display Module Attributes ---")
    # List everything in the display module
    for item in dir(display):
        if not item.startswith("__"):
            print(item)

    # Also check if there are any specific Enums inside it
    if hasattr(display, 'ViewportSettings'): 
        print("\n--- ViewportSettings ---")
        print(dir(display.ViewportSettings))

def find_veiwport_mode_code():
    from PySide6.QtWidgets import QApplication

    # Get the main application
    app = QApplication.instance()

    print("--- Searching for Mask Actions ---")
    found_count = 0
    visited_actions = set()

    # Iterate over every widget in the UI
    for widget in app.allWidgets():
        for action in widget.actions():
            # Clean up the text (remove accelerator keys like "&File")
            name = action.text().replace("&", "")
            
            # We search for "Mask" but filter out common noise like "Add Mask"
            # We are looking for "Show", "View", "Toggle", or just "Mask" in a View menu context
            if "Mask" in name and action not in visited_actions:
                visited_actions.add(action)
                
                # Print potentially relevant actions
                # We filter out "Add" to reduce noise, focusing on View/Edit ops
                if "Add" not in name and "Remove" not in name:
                    print(f"Action: '{name}' | Parent: {type(widget).__name__} | Object: {action}")
                    found_count += 1

    print(f"\nTotal Candidates Found: {found_count}")
        

def search_for_channel_code():
    from PySide6.QtWidgets import QApplication

    app = QApplication.instance()
    print("--- Searching for Channel/Display Actions ---")

    found_count = 0
    visited_actions = set()

    for widget in app.allWidgets():
        for action in widget.actions():
            # Clean the name
            text = action.text().replace("&", "")
            
            # Filter for the user's specific guess + broad keyword
            if "Channel" in text or "Display" in text:
                if action not in visited_actions:
                    visited_actions.add(action)
                    print(f"Action: '{text}' | Object: {action}")
                    found_count += 1

    print(f"\nTotal Found: {found_count}")

def search_pick():
    from PySide6.QtWidgets import QApplication
    from PySide6.QtGui import QKeySequence

    app = QApplication.instance()
    print("--- Searching for 'Pick Material' Tool ---")

    found_count = 0
    visited_actions = set()

    # Iterate all widgets
    for widget in app.allWidgets():
        for action in widget.actions():
            # Clean the name
            text = action.text().replace("&", "")
            
            # Get shortcuts (returns a list of QKeySequence)
            shortcuts = action.shortcuts()
            has_p_shortcut = any(seq.toString() == "P" for seq in shortcuts)
            
            # Search criteria:
            # 1. Name contains "Pick" AND "Material"
            # 2. OR the shortcut is exactly "P"
            if ("Pick" in text and "Material" in text) or has_p_shortcut:
                
                if action not in visited_actions:
                    visited_actions.add(action)
                    
                    # Print details
                    shortcut_str = ", ".join([s.toString() for s in shortcuts])
                    print(f"FOUND: '{text}' | Shortcut: [{shortcut_str}]")
                    print(f"Object: {action}\n")
                    found_count += 1

    print(f"Total Candidates: {found_count}")

#################################################################

def create_menu():    
    """Create and populate the menu with actions."""
    # Get the main window
    main_window = ui.get_main_window()    

    # Create a new menu
    vg_utilities_menu = QtWidgets.QMenu("VG Utilities", main_window)
    ui.add_menu(vg_utilities_menu)
    plugin_menus_widgets.append(vg_utilities_menu)

    # Define actions, shortcuts, and separators
    actions_with_separators = [
        ("New Paint Layer", new_paint_layer, "Ctrl+P"),
        None,  # Separator
        ("New Fill Layer with Base Color", new_fill_layer_base, "Ctrl+F"),
        # ("New Fill Layer with Height", new_fill_layer_height, "Ctrl+Alt+F"),
        ("New Fill Layer with All Channels", new_fill_layer_all, "Ctrl+Shift+F"),
        ("New Fill Layer, no channel", new_fill_layer_empty, None),
        None,  # Separator
        ("Add Mask to Selected Layer", add_mask, "Ctrl+M"),
        ("Add Mask with Fill Effect", add_mask_with_fill_effect, "Shift+M"),
        ("Add Mask with AO Generator", add_ao_mask, "Ctrl+Shift+M"),
        ("Add Mask with Curvature Generator", add_curvature_mask, "Ctrl+Alt+M"),
        ("Add Mask with Color Selection", add_color_select_mask, "Alt+F"),
        None,  # Separator
        ("Create New Layer from Visible Stack", create_layer_from_stack, "Ctrl+Shift+G"),
        ("Flatten Stack", flatten_stack, None),
        None,  # Separator
        ("Create Reference Point Layer", create_ref_point_layer, "Ctrl+R"),
        None,  # Separator
        ("Print Layerstack Attributes", print_layerstack_attributes, None),
        ("Help Insert Color Selection Effect", help_insert_color_selection_effect, None),
        ("Print NodeType Attributes", print_nodetype_attributes, None),
        ("Run MH Script Test", run_mh_script_test, None),
        ("Run MH Black Mask Color Select", run_mh_black_mask_color_select, None),
        ("Run MH Add Paint Mask Effect", run_mh_add_paint_mask_effect, None),
        ("Run MH Test has_mask Attribute", run_test_has_mask_attribute, None),
        ("Run MH Help Layerstack Attributes A", help_layerstack_attributes_A, None),
        ("Run MH Insert Paint Layer Mask Dynamic", run_insert_paint_layer_mask_dynamic, "Ctrl+Alt+D"),
        ("Run MH Insert Fill Layer Mask Dynamic", run_insert_fill_layer_mask_dynamic, "Ctrl+Alt+F"),
        ("Run MH Insert Levels Layer Mask Dynamic", run_insert_levels_layer_mask_dynamic, "Ctrl+Alt+V"),
        ("Run MH Insert Color Selection Layer Mask Dynamic", run_insert_color_selection_layer_mask_dynamic, "Ctrl+Alt+C"),




        ("Print NodeType Attributes (raw)", print_NodeType_attributes, None),
        ("Print SelectionType Enum Options", print_enum_selection_type, None),
        ("Print UI Modules", print_ui_modules, None),
        ("Print Display Modules", print_display_modules, None),
        ("Find Viewport Mode Code", find_veiwport_mode_code, None),
        ("Search for Channel/Display Code", search_for_channel_code, None),
        ("Search for 'Pick Material' Tool", search_pick, None),

        None,  # Separator
        ("Quick Bake", launch_quick_bake, "Ctrl+B"),
    ]

    # Add actions and separators to the menu
    for item in actions_with_separators:
        if item is None:
            vg_utilities_menu.addSeparator()
        else:
            text, func, shortcut = item
            action = QtGui.QAction(text, vg_utilities_menu)
            action.triggered.connect(func)
            if shortcut:
                action.setShortcut(QKeySequence(shortcut))
            vg_utilities_menu.addAction(action)



def start_plugin():
    """Called when the plugin is started."""
    create_menu()
    logging.info("VG Menu Activated") 
    

def close_plugin():
    """Called when the plugin is stopped."""
    # Remove all added widgets from the UI.
    for widget in plugin_menus_widgets:
        ui.delete_ui_element(widget)
    plugin_menus_widgets.clear()
    logging.info("VG Menu deactivated")  

def reload_plugin():
    """Reload plugin modules."""
    importlib.reload(vg_layerstack)
    importlib.reload(vg_export)
    importlib.reload(vg_baking)
    importlib.reload(vg_project_info)
    importlib.reload(mh_scripts)

if __name__ == "__main__":
    importlib.reload(vg_layerstack)
    importlib.reload(vg_export)
    importlib.reload(vg_baking)
    importlib.reload(vg_project_info)
    importlib.reload(mh_scripts)

    start_plugin()
