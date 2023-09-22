from kivy.config import Config
Config.set('graphics', 'resizable', 0)

import re
from kivy.app import App 
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Rectangle, Line
from kivy.graphics.texture import Texture
from kivy.uix.image import Image, AsyncImage
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.scrollview import ScrollView
from kivy.clock import mainthread, Clock

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
widget_text = []

products = {'Eggs' : '0', 'Butter' : '0g', 'Ground Hot Pepper' : '0g', 'Salt' : '0g', 'Tomato' : '0g', 'Onion' : '0g', 'Ground Hot Pepper' : '0g',
            'Olive Oil' : '0g', 'Sour Cream' : '0g', 'Cottage Cheese' : "0g", 'Apples' : "0g", 'Wheat Flour' : '0g', 'Sugar' : '0g', 'Baking powder' : '0g', 
            'Vegetable Oil' : '0g', 'Chicken' : '0g', 'Champignons' : '0g', 'Sauerkraut' : '0g', 'Carrot' : '0g', 'Potato' : '0g', 'Tomato Paste' : '0g',
            'Garlic' : '0g', 'Pork' : '0g', 'Beet' : '0g', 'Cabbage' : '0g', 'Greens' : '0g', 'Ground Pepper' : '0g', 'Pasta' : '0g', 'Ground Paprika' : '0g',
            'Mutton' : '0g', 'Rice' : '0g', 'Hot Pepper' : '0g', 'Crab Sticks' : '0g', 'Canned Corn' : '0g', 'Cheese' : '0g', 'Mayonnaise' : '0g'}

descriptions = []

buttons = []

weekly_menu = []

weekly_menu_names = {}

recipes = {'scrambled eggs' : {'Eggs' : "2", 'Butter' : "10g", 'Ground Hot Pepper' : "1g", 'Salt' : "2g"},
           'omelet' : {'Eggs' : "3", 'Butter' : "15g", 'Tomato' : "450g", 'Onion' : "200g", 'Ground Hot Pepper' : "2g", 'Salt' : "3g", 'Olive Oil' : "30g", 'Sour Cream' : "25g"},
           'curd fritters with apples' : {'Cottage Cheese' : "200g", 'Apples' : "350g", 'Wheat Flour' : "80g", 'Eggs' : "2", 'Sugar' : "40g", 'Baking powder' : "10g", 'Vegetable Oil' : "50g"},
           'cabbage salt soup' : {'Chicken' : "800g", 'Champignons' : "300g", 'Sauerkraut' : "500g", 'Ground Hot Pepper' : "10g", 'Onion' : "100g", 'Carrot' : "100g", 'Potato' : "250g", "Tomato Paste" : "40g", 'Vegetable Oil' : "50g", "Garlic" : "15g"},
           'borsch' : {'Pork' : "550g", 'Beet' : "250g", 'Cabbage' : "300g", 'Onion' : "250g", 'Carrot' : "100g", 'Potato' : "500g", "Tomato Paste" : "50g", 'Vegetable Oil' : "150g", "Garlic" : "15g", 'Greens' : "15g", "Ground Pepper" : "10g"},
           'roast with potato' : {'Potato' : "600g", 'Pork' : "400g", 'Onion' : "50g", 'Carrot' : "60g", 'Garlic' : "10g", 'Ground Pepper' : "10g", 'Ground Paprika' : "15g", 'Salt' : "10g"},
           'pasta with meat' : {'Pasta' : "200g", 'Pork' : "400g", 'Onion' : "100g", 'Carrot' : "50g", 'Tomato' : "80g", "Tomato Paste" : "50g", 'Greens' : "15g"},
           'pilaf' : {'Mutton' : "650g", 'Rice' : "650g", 'Carrot' : "500g", 'Onion' : "300g", 'Garlic' : "30g", 'Hot Pepper' : "40g", 'Salt' : "10g", 'Vegetable Oil' : "150g"},
           'crab salad' : {'Crab Sticks' : "240g", 'Canned Corn' : "340g", 'Eggs' : "4", 'Cheese' : "200g", 'Mayonnaise' : "150g", 'Salt' : "15g"}}

order_list = {}


class Menu(Widget):

    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(Menu, self).__init__(**kwargs)
        self.width = Window.size[0]
        self.height = Window.size[1]

        with self.canvas:
            self.rect = Rectangle(source='prod.png', pos = self.pos, size=self.size)
class RP(Widget):

    def __init__(self, **kwargs):
        #make sure we aren't overriding any important functionality
        super(RP, self).__init__(**kwargs)
        self.width = Window.size[0]
        self.height = Window.size[1]
        with self.canvas:
            self.rect = Rectangle(source='prod.png', pos = self.pos, size=self.size)
class Background(BoxLayout):
    def __init__(self, **kwargs):
        super(Background, self).__init__(**kwargs)
        self.width = Window.size[0]
        self.height = Window.size[1]
        with self.canvas:
            self.rect = Rectangle(source='prod.png', pos = self.pos, size=self.size)
class MyApp(App):
    def split_mass(self, element):
        result_list = re.findall(r'\d+', element)
        result = result_list[0]
        return result

    def todishes(self, insatnce):
        self.sm.current = "Book of Recipes"
        self.hide_text()

    def toproducts(self,instance):
        self.sm.current = "List of Products"
        self.hide_text()

    def tomain(self,instance):
        self.sm.current = "Main Screen"
        self.hide_text()

    def torecipe(self, instance):
        self.sm.current = "Recipe"
        button_text = instance.text.split(")")[1]
        self.label_r.text = button_text.strip() + " :"
        recipe = ScrollView(size_hint = (1, .6))
        gl_recipe = GridLayout(cols = 2, size_hint_y = None, spacing = 30)
        gl_recipe.bind(minimum_height = gl_recipe.setter('height'))
        for name, des in sorted(recipes.items()):

            if name.lower() == button_text.lower().strip():
                
                for item, value in sorted(des.items()):
                    prod_description = ""
                    print(item)
                    prod_description = f"- {item.title() :}"
                    prod = Label(text = prod_description, font_size = 50, bold = True, size_hint_y = None, color = (1,1,1,1), halign="left", valign="center", size_hint_x = .7, text_size = (Window.size[0]*.7, Window.size[1]*.15))
                    mass = Label(text = value, font_size = 50, bold = True, size_hint_y = None, color = (1,1,1,1), halign="left", valign="center", size_hint_x = .3, text_size = (Window.size[0]*.3, Window.size[1]*.15))
                    gl_recipe.add_widget(prod)
                    gl_recipe.add_widget(mass)
        self.recipe_description.clear_widgets()
        self.R_D.clear_widgets()
        self.but_layout.clear_widgets()
        self.but_layout.add_widget(Button(text = " + Add to weekly menu", font_size=50, color = (1,1,1,1), background_color = (1, 1, 1, 1), text_size = (Window.size[0], 0.1*Window.size[1]), bold = True, valign = 'center', halign = 'left', on_release = self.add_recipe))
        
        recipe.add_widget(gl_recipe)
        self.R_D.add_widget((Button(text = "Back",
                                    color = (1, 0, 0, .8),
                                    size_hint = (1, 1),
                                    font_size = 50, 
                                    halign = "left",
                                    valign = "center",
                                    text_size = (Window.size[0] - 15, 0.1*Window.size[1]),
                                    on_release = self.todishes,
                                    background_color = (1, 1, 1, 0),
                                    bold = True 
                                    ))) 
        self.R_D.add_widget(self.label_r)
        
        self.recipe_description.add_widget(self.R_D)
        self.recipe_description.add_widget(recipe)
        self.recipe_description.add_widget(self.but_layout)

    def show_weekly_menu(self, instance):
        self.call_weekly_menu()



    def call_weekly_menu(self):
        self.sm.current = "Weekly Menu"
        self.bl_menu.clear_widgets()
        self.screen_week_menu.clear_widgets()
        
        self.bl_menu.add_widget(self.root_menu)
        self.hide_text()
        menu_bl = BoxLayout(orientation='vertical')

        menu_bl.add_widget((Button(text = "Back",
                                    color = (1, 0, 0, .8),
                                    size_hint = (1, 0.1),
                                    font_size = 50, 
                                    halign = "left",
                                    valign = "center",
                                    text_size = (Window.size[0] - 15, 0.1*Window.size[1]),
                                    on_release = self.tomain,
                                    background_color = (1, 1, 1, 0),
                                    bold = True 
                                    )))
        menu_bl.add_widget(Label(text = "Weekly Menu :", font_size = 60, bold = True, valign = 'top', text_size = (Window.size[0] - 15, Window.size[1]*.1), halign = 'left', color = (1,1,1,1), size_hint = (1, .1)))
        menu_scroll = ScrollView(size_hint = (1, .8))
        self.gl_menu = GridLayout(cols = 3, size_hint_y = None, spacing = 15)
        self.gl_menu.bind(minimum_height = self.gl_menu.setter('height'))
        self.number_w = 0
        for recipe_name in sorted(weekly_menu):
            numb = weekly_menu_names.get(recipe_name)        
            self.number_w += 1
            self.gl_menu.add_widget(Button(text = "-", bold = False, size_hint_y = None, color = (1,1,1,1), halign="center", valign="middle", size_hint_x = .1, font_size = 80, text_size = (Window.size[0], Window.size[1]*.1), background_color = (self.number_w,self.number_w,self.number_w,0), on_press=self.delete_portion))
            self.number_w += 1
            self.gl_menu.add_widget(Label(text = recipe_name.split(":")[0] + ': ' + numb , font_size = 40, bold = True, size_hint_y = None, color = (1,1,1,1), halign="center", valign="middle", text_size = (Window.size[0], Window.size[1]*.1), size_hint_x = .8))
            self.number_w += 1
            self.gl_menu.add_widget(Button(text = "+", bold = False, size_hint_y = None, color = (1,1,1,1), halign="center", valign="middle", size_hint_x = .1, font_size = 80, text_size = (Window.size[0], Window.size[1]*.1), background_color = (self.number_w,self.number_w,self.number_w,0), on_press=self.add_portion))
        menu_scroll.add_widget(self.gl_menu)
        menu_bl.add_widget(menu_scroll)
        self.screen_week_menu.add_widget(self.bl_menu)
        self.screen_week_menu.add_widget(menu_bl)

    def add_portion(self, instance):
        ind = int(instance.background_color[0])
        i_text = self.gl_menu.children[len(self.gl_menu.children) - ind + 1].text
        number = re.findall(r'\d+', i_text)
        only_text = i_text.split(':')[0]
        int_number = int(number[0]) + 1
        new_number = str(int_number)
        new_text = only_text + ': ' + new_number
        self.gl_menu.children[len(self.gl_menu.children) - ind + 1].text = new_text          


        if only_text + ":" in weekly_menu_names:
            num = int(weekly_menu_names[only_text + ":"]) + 1
            weekly_menu_names[only_text + ":"] = str(num)
        self.number_w = 0

    def delete_portion(self, instance):
        ind = int(instance.background_color[0])
        i_text = self.gl_menu.children[len(self.gl_menu.children) - ind - 1].text
        number = re.findall(r'\d+', i_text)
        only_text = i_text.split(':')[0]
        int_number = int(number[0]) - 1
        new_number = str(int_number)
        if int_number <= 0 :
            new_number = '0'
            self.gl_menu.remove_widget(self.gl_menu.children[len(self.gl_menu.children) - ind - 2])
            self.gl_menu.remove_widget(self.gl_menu.children[len(self.gl_menu.children) - ind - 1])
            self.gl_menu.remove_widget(self.gl_menu.children[len(self.gl_menu.children) - ind])
            if only_text + ':' in weekly_menu:
                weekly_menu.remove(only_text + ':')
            del weekly_menu_names[only_text + ':']
        else:
            new_text = only_text + ': ' + new_number
            self.gl_menu.children[len(self.gl_menu.children) - ind - 1].text = new_text
            if only_text + ":" in weekly_menu_names: 
                num = int(weekly_menu_names[only_text + ":"]) - 1
                if num <= 0:
                    num = 0
                    weekly_menu_names[only_text + ":"] = str(num)
                    del weekly_menu_names[only_text + ":"]

    def form_order(self, instance):
        order_list = {}
        for name in weekly_menu_names.items():
            portions = int(name[1])             
            name = name[0].split(':')[0].strip().lower()
            for items, values in sorted(recipes.get(name).items()):
                number = 0
                result_list = re.findall(r'\d+', values)
                result = result_list[0]
                letter = values.split(result)[1]
                if int(result) - int(re.findall(r'\d+', products[items])[0]) > 0:
                    for i in range(portions):
                        if items in products:
                            n_new = int(re.findall(r'\d+', products[items])[0])
                            print(str(n_new))
                            n_result = int(result)
                            n_result -= n_new
                            l = products[items].split(str(n_new))[-1]
                            products[items] = str(n_new) + l 
                        number += int(n_result)
                        values = str(number)+letter
                    if items in order_list.keys():
                        result_list_temp_1 = re.findall(r'\d+', order_list[items])
                        result_temp_1 = result_list_temp_1[0]
                        letter_temp = order_list[items].split(result_temp_1)[1]
                        result_list_temp_2 = re.findall(r'\d+', values)
                        result_temp_2 = result_list_temp_2[0]
                        fin_num = int(result_temp_1) + int(result_temp_2)                    
                        value = str(fin_num) + letter_temp
                        order_list[items] = value
                    else:
                        order_list[items] = values
        n = 0
        self.main_label.clear_widgets()
        for key, value in sorted(order_list.items()):
            n += 1
            k = f'{n}) {key}, {value}.'
            self.main_label.add_widget(Label(text = k,
                                            font_size = 50,
                                            color = (1,1,1,1),
                                            bold = True,
                                            size_hint_y = None,
                                            text_size = (Window.size[0], 0),
                                            halign = "left",
                                            valign = "top"))

    def add_recipe(self, instance):
        if self.label_r.text not in weekly_menu:
            weekly_menu.append(self.label_r.text)
            weekly_menu_names[self.label_r.text] = "1"
        print(weekly_menu, weekly_menu_names)


    def hide_text(self):
        self.main_label.clear_widgets()

    def form_products(self):
        self.i = 0
        self.bl_menu_products.clear_widgets()
        self.screen_products.clear_widgets()
        
        self.bl_menu_products.add_widget(self.root_products)
        self.hide_text()
        menu_p = BoxLayout(orientation='vertical')

        menu_p.add_widget((Button(text = "Back",
                                    color = (1, 0, 0, .8),
                                    size_hint = (1, 0.1),
                                    font_size = 50, 
                                    halign = "left",
                                    valign = "center",
                                    text_size = (Window.size[0] - 15, .1*Window.size[1]),
                                    on_release = self.tomain,
                                    background_color = (1, 1, 1, 0),
                                    bold = True 
                                    )))
        menu_p.add_widget(Label(text = "Products :", font_size = 60, bold = True, valign = 'top', text_size = (Window.size[0]-15, Window.size[1]*.1), halign = 'left', color = (1,1,1,1), size_hint = (1, .1)))
        p_menu_scroll = ScrollView(size_hint = (1, .8))
        self.new_menu = GridLayout(cols = 3, size_hint_y = None, spacing = 15)
        self.new_menu.bind(minimum_height = self.new_menu.setter('height'))
        self.number_p = 0
        for name, value in sorted(products.items()):   
            self.number_p += 1
            self.new_menu.add_widget(Button(text = "-", bold = False, size_hint_y = None, color = (1,1,1,1), halign="center", valign="middle", size_hint_x = .1, font_size = 80, text_size = (Window.size[0], Window.size[1]*.1), background_color = (self.number_p,self.number_p,self.number_p,0), on_press=self.delete_product, on_release=self.stop_deleting))
            self.number_p += 1
            self.new_menu.add_widget(Label(text = name + ' : ' + value , font_size = 40, bold = True, size_hint_y = None, color = (1,1,1,1), halign="center", valign="middle", text_size = (Window.size[0], Window.size[1]*.1), size_hint_x = .8))
            self.number_p += 1
            self.new_menu.add_widget(Button(text = "+", bold = False, size_hint_y = None, color = (1,1,1,1), halign="center", valign="middle", size_hint_x = .1, font_size = 80, text_size = (Window.size[0], Window.size[1]*.1), background_color = (self.number_p,self.number_p,self.number_p,0), on_press=self.add_product, on_release=self.stop_adding))
        p_menu_scroll.add_widget(self.new_menu)
        menu_p.add_widget(p_menu_scroll)
        self.screen_products.add_widget(self.bl_menu_products)
        self.screen_products.add_widget(menu_p)



    def add_product(self, instance):
        ind = int(instance.background_color[0])
        self.id = ind
        i_text = self.new_menu.children[len(self.new_menu.children) - self.id + 1].text
        mass = i_text.split(':')[1].strip()
        name = i_text.split(':')[0].strip()
        mass_num = int(re.findall(r'\d+', mass)[0])
        measure = mass.split(str(mass_num))[1]  
        new_text = name + ' : ' + str(mass_num + 1) + measure
        if name in products:
            products[name] = str(mass_num + 1) + measure
        self.new_menu.children[len(self.new_menu.children) - self.id + 1].text = new_text   
        Clock.schedule_interval(self.add_i, 0.1)
        self.i = 0

    def add_i(self, instance):
        self.i += 10
        i_text = self.new_menu.children[len(self.new_menu.children) - self.id + 1].text
        mass = i_text.split(':')[1].strip()
        name = i_text.split(':')[0].strip()
        mass_num = int(re.findall(r'\d+', mass)[0])
        measure = mass.split(str(mass_num))[1]  
        new_text = name + ' : ' + str(mass_num + self.i) + measure
        if name in products:
            products[name] = str(mass_num + self.i) + measure
        self.new_menu.children[len(self.new_menu.children) - self.id + 1].text = new_text
        with open('products.py', 'w') as prod:
            prod.write(products)
        print(name, products[name])

    def stop_adding(self, instance):
        Clock.unschedule(self.add_i)

    def delete_product(self, instance):
        ind = int(instance.background_color[0])
        self.id = ind
        i_text = self.new_menu.children[len(self.new_menu.children) - self.id - 1].text
        mass = i_text.split(':')[1].strip()
        name = i_text.split(':')[0].strip()
        mass_num = int(re.findall(r'\d+', mass)[0])
        measure = mass.split(str(mass_num))[1]  
        new_text = name + ' : ' + str(mass_num - 1) + measure
        self.new_menu.children[len(self.new_menu.children) - self.id - 1].text = new_text
        Clock.schedule_interval(self.delete_i, 0.1)
        self.i = 0        


    def delete_i(self, instance):
        self.i += 10
        i_text = self.new_menu.children[len(self.new_menu.children) - self.id - 1].text
        mass = i_text.split(':')[1].strip()
        name = i_text.split(':')[0].strip()
        mass_num = int(re.findall(r'\d+', mass)[0])
        measure = mass.split(str(mass_num))[1]
        if mass_num - self.i <= 0:
            mass_num = 10
            self.i = 10
        new_text = name + ' : ' + str(mass_num - self.i) + measure
        self.new_menu.children[len(self.new_menu.children) - self.id - 1].text = new_text

    def stop_deleting(self, instance):
        Clock.unschedule(self.delete_i)

    def form_dishes(self):
        #self.i = 0
        self.bl_menu_dishes.clear_widgets()
        self.screen_dishes.clear_widgets()
        
        self.bl_menu_dishes.add_widget(self.root_dishes)
        self.hide_text()
        menu_d = BoxLayout(orientation='vertical')

        menu_d.add_widget((Button(text = "Back",
                                    color = (1, 0, 0, .8),
                                    size_hint = (1, 0.1),
                                    font_size = 50, 
                                    halign = "left",
                                    valign = "center",
                                    text_size = (Window.size[0] - 15, .1*Window.size[1]),
                                    on_release = self.tomain,
                                    background_color = (1, 1, 1, 0),
                                    bold = True 
                                    )))
        menu_d.add_widget(Label(text = "Book Of Recipes :", font_size = 60, bold = True, valign = 'top', text_size = (Window.size[0] - 15, Window.size[1]*.1), halign = 'left', color = (1,1,1,1), size_hint = (1, .1)))
        menu_d.add_widget(self.list_recipes_scroll)
        self.screen_dishes.add_widget(self.bl_menu_dishes)
        self.screen_dishes.add_widget(menu_d)

    def build(self):
        self.list_recipes_scroll = ScrollView(size_hint = (1, .8))
        list_recipes = GridLayout(cols = 1, size_hint_y = None, spacing = 30)
        list_recipes.bind(minimum_height = list_recipes.setter('height'))
        number = 0
        
        for name,values in sorted(recipes.items()):
            text_name = name.title()
            number += 1
            but = Button(text = f"{number}) {text_name}", font_size = 50, bold = True, size_hint_y = None, color = (1,1,1,1), background_color = (1,1,1,0), halign="left", valign="top")
            
            but.bind(size=but.setter('text_size'))
            but.bind(on_release=self.torecipe)
            list_recipes.add_widget(but)

        self.list_recipes_scroll.add_widget(list_recipes)

        self.sm = ScreenManager(transition = FadeTransition())
        screen_main = Screen(name = "Main Screen")
        self.screen_dishes = Screen(name = "Book of Recipes")
        self.screen_products = Screen(name = "List of Products")
        screen_recipe = Screen(name = "Recipe")
        self.screen_week_menu = Screen(name = "Weekly Menu")

        self.root_dishes = Menu()
        self.root_products = Menu()
        root_recipes = RP()
        self.root_menu = RP()
        self.bl_menu_dishes = BoxLayout(padding = [5,5])
        self.bl_menu_dishes.add_widget(self.root_dishes)
        self.bl_menu_products = BoxLayout(padding = [5,5])
        bl_recipe = BoxLayout(padding = [5,5])
        bl_recipe.add_widget(root_recipes)
        self.bl_menu = BoxLayout(padding = [5,5])

        # Forming main screen
        b = Background()
        gl = GridLayout( cols = 2, spacing = 5, size_hint_y = 0.4)        
        gl.add_widget(Button(text = "Weekly Menu", bold = True, font_size = 40, size_hint = (0.5,0.5), on_release = self.show_weekly_menu))
        gl.add_widget(Button(text = "Create an Order", bold = True, font_size = 40, size_hint = (0.5,0.5), on_release = self.form_order))
          
        gl.add_widget(Button(font_size = 40,
                            text = "Book of Recipes",
                            bold = True,
                            size_hint = (0.5,0.5),
                            on_release = self.todishes));                
        gl.add_widget(Button(font_size = 40,
                            text = "Product List",
                            bold = True,
                            size_hint = (0.5,0.5),
                            on_release = self.toproducts))

        gl_b = BoxLayout(orientation = 'vertical')
        
        self.main_label_scroll = ScrollView()
        self.main_label = GridLayout(cols = 1, size_hint_y = None, spacing = 10, padding = [10, 0, 0, 20])
        self.main_label.bind(minimum_height = self.main_label.setter('height'))
        self.main_label_scroll.add_widget(self.main_label)

        gl_b.add_widget(self.main_label_scroll)
        gl_b.add_widget(gl)

        main_screen_bl = FloatLayout()
        main_screen_bl.add_widget(b)
        main_screen_bl.add_widget(gl_b)
        screen_main.add_widget(main_screen_bl)

        # Forming screen of products

        self.form_products()

        # Forming screen of dishes

        self.form_dishes()

        # Forming a screen for a recipe
        self.but_layout = BoxLayout(orientation = 'vertical', size_hint = (1, .1))
        
        self.R_D = BoxLayout(orientation='vertical', size_hint = (1, .2))
        self.recipe_description = BoxLayout(orientation = 'vertical')

        self.label_r = (Label(text = "<Recipe>", font_size = 60, bold = True, valign = 'top', text_size = (Window.size[0]-15, Window.size[1]*.1), halign = 'left', color = (1,1,1,1), size_hint = (1, 1)))
        self.recipe_description.add_widget(self.R_D)
        self.recipe_description.add_widget(self.but_layout)
        screen_recipe.add_widget(bl_recipe)
        screen_recipe.add_widget(self.recipe_description)
         

        # Forming an app

        self.sm.add_widget(screen_main)
        self.sm.add_widget(self.screen_products)
        self.sm.add_widget(self.screen_dishes)
        self.sm.add_widget(screen_recipe)
        self.sm.add_widget(self.screen_week_menu)
        self.sm.current = "Main Screen"


        return self.sm
if __name__ == '__main__':
    MyApp().run()