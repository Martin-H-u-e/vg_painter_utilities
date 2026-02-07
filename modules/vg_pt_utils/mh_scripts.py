# MH scripts
# Modules Import

from platform import node
import string
from substance_painter import textureset, layerstack, project, resource, logging, colormanagement


"""
[Python] --- Raw Attributes of NodeType ---
[Python] AnchorPointEffect
[Python] ColorSelectionEffect
[Python] CompareMaskEffect
[Python] FillEffect

[Python] FillLayer

[Python] FilterEffect
[Python] GeneratorEffect

[Python] GroupLayer

[Python] InstanceLayer

[Python] LevelsEffect
[Python] PaintEffect

[Python] PaintLayer

[Python] name
[Python] value
"""


def mh_script_test():
    # toggle_layer_mask_selection():
    try:
        # 1. Get the current layer
        stack = textureset.get_active_stack()
        selection = layerstack.get_selected_nodes(stack)
        
        if not selection:
            print("No layer selected.")
            return

        current_layer = selection[0]

        # 2. Get current state (Now passing the required layer argument)
        current_type = layerstack.get_selection_type(current_layer)
        
        # 3. Define the correct Enums based on your discovery
        MODE_CONTENT = layerstack.SelectionType.Content
        MODE_MASK = layerstack.SelectionType.Mask 

        # 4. The Toggle Logic
        # Note: We must pass 'current_layer' to the setter as well
        if current_type == MODE_CONTENT:
            print(f"Switching {current_layer} to MASK...")
            layerstack.set_selection_type(current_layer, MODE_MASK)
        else:
            print(f"Switching {current_layer} to CONTENT...")
            layerstack.set_selection_type(current_layer, MODE_CONTENT)

    except Exception as e:
        print(f"Error: {e}")

def toggle_layer_mask_selection():
    """Toggles the selection between layer content and mask for the currently selected layer."""
    try:
        # 1. Get the current layer
        stack = textureset.get_active_stack()
        selection = layerstack.get_selected_nodes(stack)
        
        if not selection:
            print("No layer selected.")
            return

        current_layer = selection[0]

        # 2. Get current state (Now passing the required layer argument)
        current_type = layerstack.get_selection_type(current_layer)
        
        # 3. Define the correct Enums based on your discovery
        MODE_CONTENT = layerstack.SelectionType.Content
        MODE_MASK = layerstack.SelectionType.Mask 

        # 4. The Toggle Logic
        # Note: We must pass 'current_layer' to the setter as well
        if current_type == MODE_CONTENT:
            print(f"Switching {current_layer} to MASK...")
            layerstack.set_selection_type(current_layer, MODE_MASK)
        else:
            print(f"Switching {current_layer} to CONTENT...")
            layerstack.set_selection_type(current_layer, MODE_CONTENT)

    except Exception as e:
        print(f"Error: {e}")

class MaskManager_mh:

    def __init__(self, layer_manager):
        self.layer_manager = layer_manager

    def add_mask(self, mask_bkg_color=None):
        """Adds a mask to the currently selected layer with optional background color."""
        
        color_map = {
            'Black': layerstack.MaskBackground.Black,  
            'White': layerstack.MaskBackground.White  
        }

        if mask_bkg_color and mask_bkg_color not in color_map:
            logging.error("Invalid mask color. Choose 'Black' or 'White'.")
            return

        if self.layer_manager.current_stack:
            current_layer = layerstack.get_selected_nodes(self.layer_manager.current_stack)

            for selectedLayer in current_layer:
                if selectedLayer.has_mask():
                    if mask_bkg_color:
                        selectedLayer.remove_mask()
                        selectedLayer.add_mask(color_map[mask_bkg_color])
                    else:
                        current_mask_background = selectedLayer.get_mask_background()
                        new_mask_background = (layerstack.MaskBackground.White if current_mask_background == layerstack.MaskBackground.Black 
                                            else layerstack.MaskBackground.Black)
                        selectedLayer.remove_mask()
                        selectedLayer.add_mask(new_mask_background)
                else:
                    mask_to_add = color_map.get(mask_bkg_color, layerstack.MaskBackground.Black)
                    selectedLayer.add_mask(mask_to_add)


    def mh_add_black_mask_with_color_select(self):
        """Adds a black mask with a color selection layer to the currently selected layer.
        """

        stack = textureset.get_active_stack()
        current_layer = layerstack.get_selected_nodes(self.layer_manager.current_stack)
        self.add_mask()
        
        inside_mask = layerstack.InsertPosition.inside_node(current_layer[0], layerstack.NodeStack.Mask)
        my_color_selection_effect = layerstack.insert_color_selection_effect(inside_mask)
        layerstack.set_selected_nodes([my_color_selection_effect])


    def mh_add_paint_mask_effect_v0(self):
        """Adds a paint effect to the mask of the currently selected layer or its parent layer if an effect is selected. Adds a black mask if none exists.
        """
        selected_nodes = layerstack.get_selected_nodes(self.layer_manager.current_stack)
        if not selected_nodes:
            logging.error("No layer selected.")
            return
        
        selected_node = selected_nodes[0]
        
        if selected_node.has_mask():
            layer_node = selected_node
        else:
            # If selected is an effect (no mask), get the parent layer (effect -> mask -> layer)
            mask_node = selected_node.get_parent()
            layer_node = mask_node.get_parent()
        
        # Check if the layer has a mask; if not, add a black mask
        if not layer_node.has_mask():
            layer_node.add_mask(layerstack.MaskBackground.Black)
        
        inside_mask = layerstack.InsertPosition.inside_node(layer_node, layerstack.NodeStack.Mask)
        my_paint_effect = layerstack.insert_paint(inside_mask)
        layerstack.set_selected_nodes([my_paint_effect])


    def mh_add_paint_mask_effect(self):
        """Adds a paint effect to the mask of the currently selected layer or its parent layer if an effect is selected. Adds a black mask if none exists.
        """
        selected_layer = layerstack.get_selected_nodes(self.layer_manager.current_stack)
        if not selected_layer:
            logging.error("No layer selected.")
            return
        
        selected_node = selected_layer[0]

        try:
            if not selected_node.has_mask():
                # create mask and
                # insert inside mask
                self.add_mask(mask_bkg_color='Black')
                insert_position = layerstack.InsertPosition.inside_node(selected_layer[0], layerstack.NodeStack.Mask)
                my_paint_effect = layerstack.insert_paint(insert_position)
                layerstack.set_selected_nodes([my_paint_effect])
        except AttributeError:
            # decide if user has a layer or effect selected
            if selected_node.get_type() == layerstack.NodeType.PaintEffect:
                # insert above effect
                insert_position = layerstack.InsertPosition.above_node(selected_node)
                my_paint_effect = layerstack.insert_paint(insert_position)
                layerstack.set_selected_nodes([my_paint_effect])
            else:
                # insert inside mask
                insert_position = layerstack.InsertPosition.inside_node(selected_node, layerstack.NodeStack.Mask)
                my_paint_effect = layerstack.insert_paint(insert_position)
                layerstack.set_selected_nodes([my_paint_effect])


    def test_has_mask_attribute(self):
        """Test if the selected layer has the has_mask attribute available.
        Prints success message if AttributeError is caught when trying to access has_mask.
        """
        selected_layer = layerstack.get_selected_nodes(self.layer_manager.current_stack)
        if not selected_layer:
            logging.error("No layer selected.")
            return
        
        selected_node = selected_layer[0]
        
        try:
            selected_node.has_mask()
            print(f"{type(selected_node).__name__} has has_mask attribute.")
            print("Test Failed - has_mask attribute exists")
        except AttributeError as e:
            print(f"[Python] AttributeError: '{type(selected_node).__name__}' object has no attribute 'has_mask'")
            print("Test Successful - no mask found")

    def insert_mask_effect_dynamic(self, effectType):
        """
        Dynamically adds a paint effect to the mask.
        If no mask exists, it creates one with a black background and adds the paint effect inside it.
        If currently an effect is selected, it adds the paint effect above it.
        """

        def _find_properties_button():
            from PySide6.QtWidgets import QApplication, QPushButton, QWidget
            app = QApplication.instance()
            print("--- Scanning Properties Panel ---")
            
            # 1. Find the Properties Dock/Window
            # We search all widgets for one that seems to be the properties panel
            # usually by checking window titles or object names if available.
            
            candidates = []
            
            for widget in app.allWidgets():
                # We look for a button with the specific text "Pick color"
                # This text usually appears on the button inside the properties view
                if isinstance(widget, QWidget):
                    # Check text if it has it (PushButtons, ToolButtons, Labels)
                    text = ""
                    if hasattr(widget, "text"):
                        text = widget.text()
                    
                    if "Pick color" in text:
                        print(f"[FOUND] Widget: {widget} | Text: '{text}'")
                        candidates.append(widget)

            if not candidates:
                print("No 'Pick color' button found. (Make sure the Color Selection node is selected!)")
                return

            # 2. Try to verify which one is the real button
            print(f"\nFound {len(candidates)} candidate(s).")
            
            # We will try to click the first valid button found
            # (Usually there is only one visible)
            target_btn = candidates[0]
            
            print(f"Attempting to click: {target_btn}")
            # We use animateClick() here as it's safer for standard buttons than setChecked
            if hasattr(target_btn, "animateClick"):
                target_btn.animateClick()
                print(">> Click sent.")

        def _insert_and_select_paint_effect_inside_mask(slected_node, effectType, above_inside="inside"):
            if above_inside == "inside":
                insert_position = layerstack.InsertPosition.inside_node(slected_node, layerstack.NodeStack.Mask)
            if above_inside == "above":
                insert_position = layerstack.InsertPosition.above_node(slected_node)
            if effectType == "Paint":
                my_mask_effect = layerstack.insert_paint(insert_position)
            if effectType == "Fill":
                my_mask_effect = layerstack.insert_fill(insert_position)
                pure_white = colormanagement.Color(1.0, 1.0, 1.0)
                my_mask_effect.set_source(channeltype=None, source=pure_white)
            if effectType == "Color Selection":
                my_mask_effect = layerstack.insert_color_selection_effect(insert_position)
            if effectType == "Levels":
                my_mask_effect = layerstack.insert_levels_effect(insert_position)

            layerstack.set_selected_nodes([my_mask_effect])

        selected_layer = layerstack.get_selected_nodes(self.layer_manager.current_stack)
        if not selected_layer:
            logging.error("No layer selected.")
            return
        
        nodesTypes_able_to_have_masks = [
            layerstack.NodeType.PaintLayer,
            layerstack.NodeType.FillLayer,
            layerstack.NodeType.GroupLayer,
            layerstack.NodeType.InstanceLayer,
        ]

        #test check if selected node is in the list of types to add mask to
        if selected_layer[0].get_type() not in nodesTypes_able_to_have_masks:
            _insert_and_select_paint_effect_inside_mask(selected_layer[0], effectType=effectType, above_inside="above")
        else:
            try:
                # create mask and
                # insert inside mask
                selected_layer[0].add_mask(layerstack.MaskBackground.Black)
                _insert_and_select_paint_effect_inside_mask(selected_layer[0], effectType=effectType, above_inside="inside")
            # except if [Python] ValueError: This node already has a mask
            # only execute if this exact error is caught, otherwise print the error
            except ValueError as e:
                if str(e) == "This node already has a mask":
                    # swtich to mask and insert paint
                    toggle_layer_mask_selection()
                    _insert_and_select_paint_effect_inside_mask(selected_layer[0], effectType=effectType, above_inside="inside")

        if effectType == "Color Selection":
            _find_properties_button()