# MH scripts
# Modules Import

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
    try:
        # 1. Get the Active Stack (The argument you were missing)
        # Found in vg_layerstack.py Line 36/41f
        stack = textureset.get_active_stack()
        
        # 2. Get the selected layer using the stack
        selection = layerstack.get_selected_nodes(stack)
        
        if not selection:
            print("Error: No layer selected.")
        else:
            current_layer = selection[0]
            print(f"Targeting: {current_layer}")

            # 3. Create the Insertion Position
            # We use the factory method '.inside_node' found in vg_layerstack.py Line 235
            # We explicitly target the Mask stack.
            position = layerstack.InsertPosition.inside_node(current_layer, layerstack.NodeStack.Mask)
            
            # 4. Insert the Color Selection Effect
            my_color_selection_effect = layerstack.insert_color_selection_effect(position)
            
            print(f"SUCCESS! Created effect: {my_color_selection_effect}")

            layerstack.set_selected_nodes([my_color_selection_effect])

    except Exception as e:
        print(f"Script Error: {e}")


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

    