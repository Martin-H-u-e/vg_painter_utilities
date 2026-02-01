# MH scripts
# Modules Import

import string
from substance_painter import textureset, layerstack, project, resource, logging, colormanagement


def mh_script_test():
    try:
        # 1. Get the Active Stack (The argument you were missing)
        # Found in vg_layerstack.py Line 36/41
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
