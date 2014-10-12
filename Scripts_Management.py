######################################################################    
# Author: IK3D -- Issanou Kamardine                                                 
# License: GPL v3                                                  
######################################################################


bl_info = {
    "name": "Scripts Management",
    "author": "IK3D",
    "version": (0, 2),
    "location": "Properties panel > Scene",
    "description": "Pin scripts as favourites",
    "category": "Favourites"}


import bpy
from bpy.types import Header, Menu, Panel
from bpy.app.translations import pgettext_iface as iface_
from bpy.app.translations import contexts as i18n_contexts
import fileinput
import sys
import requests 



#Operator Add Favourites
class cheminOperator(bpy.types.Operator):
    bl_idname = "wm.get_chemin"
    bl_label = "Gert addons path"
    chemin = bpy.props.StringProperty()
    
    def execute(self, context):
        if self.chemin == '':
            print("Hello world!")
        else:
            print("Hello world from %s!" % self.chemin)
            dynamic_path = self.chemin

            #var new categories and old
            oldcatReaded = ""
            oldcat =""
            indexe_ligne = 0

            
            #Open File script
            fichier = open(dynamic_path, "r+")

            #read script
            lingne = fichier.readline()

            if "FAVOURIT" not in lingne: 
                #Find actual categorie
                for ligne in fichier:
                    indexe_ligne +=1
                    if "category" in ligne:        
                        oldcatReaded = ligne
                        oldcat = oldcatReaded.replace("}", "")
                        oldcat = oldcatReaded.replace('\n', "")

                        
                        #check close or not in line
                        if "}" in ligne:
                            fermer = 1
                        else:
                            fermer = 0
                        break
                  

                #fonction replace categorie 
                def replace_cat(file_name, line_num, text):
                    lines = open(file_name, 'r').readlines()
                    lines[line_num] = text
                    out = open(file_name, 'w')
                    out.writelines(lines)
                    out.close()

                #Change categorie
                if fermer == False:
                    replace_cat(dynamic_path, indexe_ligne,'    "category": "Favourites",\n')
                else:
                    replace_cat(dynamic_path, indexe_ligne,'    "category": "Favourites"}\n')                    

                #save back up, save change
                with open(dynamic_path, "r+") as fichier:
                    first_line = fichier.readline()                
                    if first_line != ("FAVOURIT = "+"'" + oldcat + " '" + "\n" + "\n"):
                        lines = fichier.readlines()
                        fichier.seek(0)
                        fichier.write("FAVOURIT = "+"'" + oldcat + " '" + "\n" + "\n" )
                        fichier.write(first_line)
                        fichier.writelines(lines)

            fichier.close()
            
        return{'FINISHED'}
        
          


#var pike-up script path
dynamic_path = ""


#Operator remove from Favourites
class unchemOperator(bpy.types.Operator):
    bl_idname = "wm.un_chemin"
    bl_label = "Remove from favourit"
    chemin = bpy.props.StringProperty()
    
    def execute(self, context):
        if self.chemin == '':
            print("Hello world!")
        else:
            print("Hello world from %s!" % self.chemin)
            dynamic_path = self.chemin

            #Read file script
            fichier = open(dynamic_path, "r+")

            #option read
            lingne = fichier.readline()

            #fonction replace remove line
            def replace_efa(file_name, line_num, text):
                lines = open(file_name, 'r').readlines()
                lines[line_num] = text
                out = open(file_name, 'w')
                out.writelines(lines)
                out.close()

            #fonction replace restore categorie  
            def replace_cat(file_name, line_num, text):
                lines = open(file_name, 'r').readlines()
                lines[line_num] = text
                out = open(file_name, 'w')
                out.writelines(lines)
                out.close()

            indexe_ligne = 0
            #back up, restor categorie
            if "category" in lingne:                   
                    #remove bad caractaires
                    FAVOURITrezOld = lingne
                    FAVOURITA= FAVOURITrezOld.replace("FAVOURIT = ", "")
                    FAVOURITB= FAVOURITA.replace("'\n'", "")
                    FAVOURIT= FAVOURITB.replace("'", "")
                    
                    #remove back up line
                    replace_efa(dynamic_path,0,'')
                    
                    #remove empty line
                    if lingne == '\n'or '\n' + '\n':
                            replace_efa(dynamic_path,0,'')
                           
                    #Find categorie line
                    for ligne in fichier:
                            indexe_ligne +=1

                            if "category" in ligne:
                                    #check if line close
                                    if "}" or " }" or " } " or "}" or "} + '\n'" or " }+ '\n'" or " } + '\n'" in ligne:
                                        fermer = 1
                                    else:
                                        fermer = 0
                                    break

                    #Replase, or, and, close line
                    if fermer == 0:
                            replace_cat(dynamic_path, indexe_ligne-2, FAVOURIT+"}")
                    else:
                            replace_cat(dynamic_path, indexe_ligne-2, FAVOURIT)

            fichier.close()

            print ("Vous avez enlevé un Favorit !")
            
        return{'FINISHED'}
        

#Display Enabled scripts
class EnadonOperator(bpy.types.Operator):
    bl_idname = "wm.ena_adon"
    bl_label = "View Enabled add-on"
    
    
    def execute(self, context):
        bpy.data.window_managers["WinMan"].addon_support = {'OFFICIAL', 'COMMUNITY', 'TESTING'}
        bpy.data.window_managers["WinMan"].addon_filter = 'Enabled'
        return {'FINISHED'}


#Display all scripts
class AlladonOperator(bpy.types.Operator):
    bl_idname = "wm.all_adon"
    bl_label = "View all add-on"
    
    
    def execute(self, context):
        bpy.data.window_managers["WinMan"].addon_support = {'OFFICIAL', 'COMMUNITY', 'TESTING'}
        bpy.data.window_managers["WinMan"].addon_filter = 'All'
        return {'FINISHED'}


class CheckeurdOperator(bpy.types.Operator):
    bl_idname = "wm.check_fav"
    bl_label = "check add-on"

    def execute(self, context):
        bpy.data.window_managers["WinMan"].addon_support = {'OFFICIAL', 'COMMUNITY', 'TESTING'}
        bpy.data.window_managers["WinMan"].addon_filter = 'Favourites'
        return {'FINISHED'}


class userOperator(bpy.types.Operator):
    bl_idname = "wm.user_adon"
    bl_label = "View user add-on"

    def execute(self, context):
        bpy.data.window_managers["WinMan"].addon_support = {'OFFICIAL', 'COMMUNITY', 'TESTING'}
        bpy.data.window_managers["WinMan"].addon_filter = 'User'
        return {'FINISHED'}



#UI display
class ScriptsManagementPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Scripts Management"
    bl_idname = "SCENE_PT_layout"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"



    class USERPREF_MT_addons_dev_guides(Menu):
        bl_label = "Development Guides"

    # menu to open web-pages with addons development guides
    def draw(self, context):
        layout = self.layout

        
    _support_icon_mapping = {
        'OFFICIAL': 'FILE_BLEND',
        'COMMUNITY': 'POSE_DATA',
        'TESTING': 'MOD_EXPLODE',
        }

    @staticmethod
    def is_user_addon(mod, user_addon_paths):
        import os

        if not user_addon_paths:
            for path in (bpy.utils.script_path_user(),
                         bpy.utils.script_path_pref()):
                if path is not None:
                    user_addon_paths.append(os.path.join(path, "addons"))

        for path in user_addon_paths:
            if bpy.path.is_subdir(mod.__file__, path):
                return True
        return False




    #Add-on layout
    def draw(self, context):
        import os
        import addon_utils

  
        userpref = context.user_preferences
        used_ext = {ext.module for ext in userpref.addons}

        userpref_addons_folder = os.path.join(userpref.filepaths.script_directory, "addons")
        scripts_addons_folder = bpy.utils.user_resource('SCRIPTS', "addons")

        #collect the categories that can be filtered on
        addons = [(mod, addon_utils.module_bl_info(mod)) for mod in addon_utils.modules(refresh=True)]

       
        #Management header layout
        layout = self.layout
        layout.label("Run Blender as admin for full permission",icon='LAYER_USED')

        split = layout.split(percentage=0.60, align=True,)
        if bpy.data.window_managers["WinMan"].addon_filter == 'Favourites':
            split.operator("wm.check_fav", icon='SPACE2',text="Favourites")
        else:
            split.operator("wm.check_fav", icon='SPACE3',text="Favourites")
        
        split.operator("wm.user_adon", text="User")
        split.operator("wm.ena_adon", icon='SAVE_AS',text="")
        split.operator("wm.all_adon", icon='BOOKMARKS',text="")
        


        #searche layout
        layout = self.layout
        layout.prop(context.window_manager, "addon_search", text="", icon='VIEWZOOM')

        
        


        row = layout.row()
        split = layout.split()
        col = split.column()
             
                
        filter = context.window_manager.addon_filter
        search = context.window_manager.addon_search.lower()
        support = context.window_manager.addon_support

        #initialized on demand
        user_addon_paths = []

        addon_numb = 0
        for mod, info in addons:
            module_name = mod.__name__
            module_realpath = mod.__file__
            

            is_enabled = module_name in used_ext

            if info["support"] not in support:
                continue

            #serche parmetres
            if search and search not in info["name"].lower():
                if info["author"]:
                    if search not in info["author"].lower():
                        continue
                else:
                    continue

            
            # check if addon should be visible with current filters
            if ((filter == "All") or
                (filter == info["category"]) or
                (filter == "Enabled" and is_enabled) or
                (filter == "Disabled" and not is_enabled) or
                (filter == "User" and (mod.__file__.startswith((scripts_addons_folder, userpref_addons_folder))))
                ):

                #limit visible addon on 'All' folder
                if bpy.data.window_managers["WinMan"].addon_filter == 'All' and addon_numb < 10:
    
                    # Addon UI Code
                    col_box = col.column()
                    box = col_box.box()
                    colsub = box.column()
                    row = colsub.row()


                    
                    if info["category"] == "Favourites":
                        row.operator("wm.un_chemin", icon='PINNED',emboss=False,text="").chemin = module_realpath
                        sub = row.row()
                        sub.label(info["name"], icon='SMALL_TRI_RIGHT_VEC')  
                    else:
                        row.operator("wm.get_chemin", icon='UNPINNED',emboss=False,text="").chemin = module_realpath
                        sub = row.row()
                        sub.label(info["name"],)

                    sub.operator("wm.addon_remove", text="", icon='PANEL_CLOSE',emboss=False).module = mod.__name__
                    

                    if is_enabled:
                        row.operator("wm.addon_disable", icon='FILE_TICK', text="", emboss=False).module = module_name
                    else:
                        row.operator("wm.addon_enable", icon='CHECKBOX_DEHLT', text="", emboss=False).module = module_name


                    #incrementation for limitation
                    addon_numb +=1

                
                
                if bpy.data.window_managers["WinMan"].addon_filter != 'All':
                    # Addon UI Code
                    col_box = col.column()
                    box = col_box.box()
                    colsub = box.column()
                    row = colsub.row()

                
                    if info["category"] == "Favourites":
                        row.operator("wm.un_chemin", icon='PINNED',emboss=False,text="").chemin = module_realpath
                        sub = row.row()
                        sub.label(info["name"], icon='SMALL_TRI_RIGHT_VEC')  
                    else:
                        row.operator("wm.get_chemin", icon='UNPINNED',emboss=False,text="").chemin = module_realpath
                        sub = row.row()
                        sub.label(info["name"],)
                    

                    sub.operator("wm.addon_remove", text="", icon='PANEL_CLOSE',emboss=False).module = mod.__name__


                    
                    if is_enabled:
                        row.operator("wm.addon_disable", icon='FILE_TICK', text="", emboss=False).module = module_name
                    else:
                        row.operator("wm.addon_enable", icon='CHECKBOX_DEHLT', text="", emboss=False).module = module_name



def register():
    bpy.utils.register_class(ScriptsManagementPanel)
    #Save Operator view all script for add
    bpy.utils.register_class(userOperator)
    #Save Operator show favourites
    bpy.utils.register_class(CheckeurdOperator)
    #Save Operator display all scripts
    bpy.utils.register_class(AlladonOperator)
    #Save Operator Add Favourites
    bpy.utils.register_class(unchemOperator)
    #Save Operator Add Favourites
    bpy.utils.register_class(cheminOperator)
    #Save Operator enabled
    bpy.utils.register_class(EnadonOperator)
    


def unregister():
    bpy.utils.unregister_class(ScriptsManagementPanel)
    bpy.utils.unregister_class(userOperator)
    bpy.utils.unregister_class(CheckeurdOperator)
    bpy.utils.unregister_class(AlladonOperator)
    bpy.utils.unregister_class(unchemOperator)
    bpy.utils.unregister_class(cheminOperator)
    bpy.utils.unregister_class(EnadonOperator)



if __name__ == "__main__":
    register()
