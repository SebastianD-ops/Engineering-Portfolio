import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
import random

Reaction_Order = 0

#Rate Equation: v0 = k[A]^x * [B]^y concentrations are in mol/L
#x, y are partial orders of reaction for A and B, overall reaction order is the sum of the exponents
#current idea, use experimental data and determine the overall order of the reaction using earlier module
#exponents are usually determined experimentally, with each exponent being the type of reaction order with respect to the conc of that Compount/Element
#https://chem.libretexts.org/Bookshelves/General_Chemistry/Chemistry_1e_(OpenSTAX)/12%3A_Kinetics/12.04%3A_Rate_Laws

#two options for simulating, one molecule raised to the 0th, 1st or 2nd power, or multiple chemicals raised to the 1st or greater power
reactants = []
reactant_names = []
reactant_display = []

products = []
product_names = []
product_display = []

class reactant:
    def __init__(self, init_conc,partial_order,name):
        self.init_conc = init_conc
        self.partial_order = partial_order
        self.name = name
    def display(self):
        display_statement = (f"{self.name}",f"{self.init_conc}",f"{self.partial_order}")
        reactant_display.append(display_statement)
        reactant_names.append(self.name)

class product:
    def __init__(self,name):
        self.name = name
    def display(self):
        display_statement = (f"{self.name}")
        product_display.append(display_statement)
        product_names.append(self.name)
#CODE FOR GUI
class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Batch Reactor Project")
        self.root.geometry("600x500")
        self.selected_reactant = None

        self.reactant_product_switch = tk.Frame(self.root)
        self.ProductButton = tk.Button(self.reactant_product_switch,text="Products",
                                     command=lambda:(self.hide(self.ReactantPage), self.show(self.ProductPage)))
        self.ReactantButton = tk.Button(self.reactant_product_switch,text="Reactants",
                                        command=lambda:(self.hide(self.ProductPage), self.show(self.ReactantPage)))
        self.ReactantButton.grid(row=0,column=0)
        self.ProductButton.grid(row=0, column=1)
        self.reactant_product_switch.pack()

        self.Windows = tk.Frame(self.root)
        self.Windows.pack()

        self.ReactantPage = tk.Frame(self.Windows)
        self.ReactantPage.pack()
        self.ProductPage = tk.Frame(self.Windows)

        self.visuals = tk.Frame(self.ReactantPage)
        #TABLE
        self.table = ttk.Treeview(self.visuals)
        self.table['columns'] = ('Name','Initial Concentration','Partial Order')
        #table columns
        self.table.column("#0",width=0, stretch=tk.NO)
        self.table.column('Name',anchor='w', width=150)
        self.table.column('Initial Concentration',anchor='w', width=200)
        self.table.column('Partial Order', anchor='w', width=250)
        #table headings
        self.table.heading('#0',text='',anchor='w')
        self.table.heading('Name',text='Name',anchor='w')
        self.table.heading('Initial Concentration', text='Initial Concentration', anchor='w')
        self.table.heading('Partial Order', text='Partial Order', anchor='w')

        self.table.tag_configure('oddrow', background='gray94')
        self.table.tag_configure('evenrow', background='white')

        for i in range(len(reactant_display)):
            if i % 2 == 0:
                self.table.insert(parent='',index=i,values=reactant_display[i],tags='evenrow')
            else:
                self.table.insert(parent='',index=i,values=reactant_display[i],tags='oddrow')

        self.table.pack(expand=True,fill='both')
        self.visuals.grid(row=0, column=0)

        self.table.bind('<<TreeviewSelect>>', self.on_row_select)

        #BUTTONS FRAME ------
        self.buttons_frame = tk.Frame(self.ReactantPage)
        self.buttons_frame.grid(row=1, column=0)
        #REACTANT NAMING ------
        self.reactant_name_label = tk.Label(self.buttons_frame,text="Reactant Name:")
        self.reactant_name_label.grid(row=0,column=0)
        self.reactant_name = tk.StringVar()
        self.add_reactant_name = tk.Entry(self.buttons_frame,textvariable=self.reactant_name)
        self.add_reactant_name.grid(row=0,column=1)
        #REACTANT INIT_CONCENTRATION -----
        self.reactant_conc_label = tk.Label(self.buttons_frame, text="Reactant Initial Concentration:")
        self.reactant_conc_label.grid(row=0, column=2)
        self.reactant_conc = tk.StringVar()

        self.add_reactant_conc = tk.Entry(self.buttons_frame, textvariable=self.reactant_conc)
        self.add_reactant_conc.grid(row=0, column=3)
        self.reactant_conc_unit_label = tk.Label(self.buttons_frame, text="mol/L")
        self.reactant_conc_unit_label.grid(row=0, column=4)
        # REACTANT PARTIAL ORDER ------
        self.reactant_order_label = tk.Label(self.buttons_frame, text="Reactant Order:")
        self.reactant_order_label.grid(row=1, column=0)
        self.reactant_order = tk.StringVar()
        self.add_reactant_order = tk.Entry(self.buttons_frame, textvariable=self.reactant_order)
        self.add_reactant_order.grid(row=1, column=1)

        # ADD REACTANT BUTTON ------
        self.add_reactant = tk.Button(self.buttons_frame,text="Add Reactant",fg="black",bg="white",command=self.add_reactant)
        self.add_reactant.grid(row=2,column=1,sticky=tk.E + tk.W)
        # REMOVE REACTANT BUTTON -----
        self.remove_reactant = tk.Button(self.buttons_frame,text="Remove Reactant",fg="red",bg="white",command=self.remove_reactant)
        self.remove_reactant.grid(row=2,column=3,sticky=tk.E + tk.W)

        # ------ ------------ -------
        # ------ PRODUCT PAGE -------
        # ------ ------------ -------

        self.visuals_product = tk.Frame(self.ProductPage)

        # TABLE PRODUCT
        self.table_product = ttk.Treeview(self.visuals_product)
        self.table_product['columns'] = ('Name')
        # table columns
        self.table_product.column("#0", width=0, stretch=tk.NO)
        self.table_product.column('Name', anchor='w', width=150)
        # table headings
        self.table_product.heading('#0', text='', anchor='w')
        self.table_product.heading('Name', text='Name', anchor='w')

        self.table_product.tag_configure('oddrow', background='gray94')
        self.table_product.tag_configure('evenrow', background='white')

        for i in range(len(product_display)):
            if i % 2 == 0:
                self.table_product.insert(parent='', index=i, values=product_display[i], tags='evenrow')
            else:
                self.table_product.insert(parent='', index=i, values=product_display[i], tags='oddrow')

        self.table_product.pack(expand=True, fill='both')
        self.visuals_product.grid(row=0, column=0)

        self.table_product.bind('<<TreeviewSelect>>', self.on_row_select_product)

        # BUTTONS FRAME ------
        self.buttons_frame_product = tk.Frame(self.ProductPage)
        self.buttons_frame_product.grid(row=1, column=0)
        # PRODUCT NAMING ------
        self.product_name_label = tk.Label(self.buttons_frame_product, text="Product Name:")
        self.product_name_label.grid(row=0, column=0)
        self.product_name = tk.StringVar()
        self.add_product_name = tk.Entry(self.buttons_frame_product, textvariable=self.product_name)
        self.add_product_name.grid(row=0, column=1)


        # ADD PRODUCT BUTTON ------
        self.add_product = tk.Button(self.buttons_frame_product, text="Add Product", fg="black", bg="white",command=self.add_product)
        self.add_product.grid(row=1, column=0, sticky=tk.E + tk.W)
        # REMOVE PRODUCT BUTTON -----
        self.remove_product = tk.Button(self.buttons_frame_product, text="Remove Product", fg="red", bg="white",command=self.remove_product)
        self.remove_product.grid(row=1, column=2, sticky=tk.E + tk.W)

        #--------------------------
        #-- SIMULATION SECTION ----
        #--------------------------

        self.simbuttons = tk.Frame(self.root)
        self.simbuttons.pack(pady=50)


        # SIMULATION LENGTH ------
        self.simlength_label = tk.Label(self.simbuttons, text="Simulation Length:")
        self.simlength_label.grid(row=1, column=0)
        self.simlength = tk.StringVar()
        self.simlength_entry = tk.Entry(self.simbuttons, textvariable=self.simlength)
        self.simlength_entry.grid(row=1, column=1)
        # REACTION K VALUE ------
        self.k_label = tk.Label(self.simbuttons, text="Rate Constant:")
        self.k_label.grid(row=2, column=0)
        self.k_value = tk.StringVar()
        self.k_entry = tk.Entry(self.simbuttons, textvariable=self.k_value)
        self.k_entry.grid(row=2, column=1)


        # SIMULATE REACTOR BUTTON -----
        self.simulate = tk.Button(self.simbuttons, text="Simulate", fg="blue", bg="white",command=self.runge_Kutte)
        self.simulate.grid(row=3, column=0, sticky=tk.E + tk.W)

    def hide(self,frame):
        frame.pack_forget()
    def show(self,frame):
        frame.pack()

    def on_row_select(self, event):
        selected_item = self.table.selection()
        if selected_item:
            item_id = selected_item[0]
            values = self.table.item(item_id,'values')
            self.selected_reactant = values

    def on_row_select_product(self, event):
        selected_item = self.table_product.selection()
        if selected_item:
            item_id = selected_item[0]
            values = self.table_product.item(item_id,'values')
            self.selected_product = values

    def update_table(self,table,display_list):
        for row in table.get_children():
            table.delete(row)

        for i, row_data in enumerate(display_list):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            table.insert('', i, values=row_data, tags=tag)

    def add_reactant(self):
        Invalid_conc = True
        Invalid_name = True
        Invalid_order = True

        if Invalid_conc:
            try:
                reactant_conc = float(self.reactant_conc.get())
            except:
                messagebox.showerror("Invalid value", "Invalid value for Concentration")
            finally:
                if isinstance(reactant_conc, float):
                    Invalid_conc = False

        if Invalid_order:
            try:
                reactant_order = float(self.reactant_order.get())
            except:
                messagebox.showerror("Invalid value", "Invalid value for Order")
            finally:
                if isinstance(reactant_order, float):
                    Invalid_order = False



        if Invalid_name:
            if self.reactant_name.get() in reactant_names or self.reactant_name.get() in product_names:
                messagebox.showerror("Invalid Name", "Reactant or Product already present")
            else:
                Invalid_name = False

        if not Invalid_name and not Invalid_conc and not Invalid_order:
            Reagent = reactant(reactant_conc, reactant_order,self.reactant_name.get())
            Reagent.display()
            reactants.append(Reagent)
            self.update_table(self.table,reactant_display)
    def remove_reactant(self):
        if self.selected_reactant != None:
            index = reactant_names.index(self.selected_reactant[0])
            reactant_display.remove(self.selected_reactant)
            reactant_names.remove(reactant_names[index])
            reactants.remove(reactants[index])
            self.selected_reactant = None
        self.update_table(self.table, reactant_display)

    def add_product(self):
        Invalid_name = True

        if Invalid_name:
            if self.product_name.get() in reactant_names or self.product_name.get() in product_names:
                messagebox.showerror("Invalid Name", "Reactant or Product already present")
            else:
                Invalid_name = False

        if not Invalid_name:
            Prod = product(self.product_name.get())
            Prod.display()
            products.append(Prod)
            self.update_table(self.table_product,product_display)

    def remove_product(self):
        if self.selected_product != None:
            index = product_names.index(self.selected_product[0])
            product_display.remove(self.selected_product[0])
            product_names.remove(product_names[index])
            products.remove(products[index])
            self.selected_product = None
        self.update_table(self.table_product,product_display)
    def runge_Kutte(self):
        #get all reactant species
        Invalid_k = True
        Invalid_simlength = True
        dt = 1

        if Invalid_k:
            try:
                k = float(self.k_value.get())
            except:
                messagebox.showerror("Invalid value", "Invalid value for reaction rate coefficient")
            finally:
                if isinstance(k, float):
                    Invalid_k = False

        if Invalid_simlength:
            try:
                simlength = int(self.simlength.get())
            except:
                messagebox.showerror("Invalid value", "Invalid value for Simulation length")
            finally:
                if isinstance(simlength, int):
                    Invalid_simlength = False

        timestep = int(simlength/dt)

        if not Invalid_k and not Invalid_simlength:
            self.reactant_concentrations = {}
            self.product_concentrations = {}
            for reactant in reactant_display:
                self.reactant_concentrations[reactant[0]] = []
                self.reactant_concentrations[reactant[0]].append(float(reactant[1]))
                print(self.reactant_concentrations[reactant[0]])
            self.product_concentrations = {}
            for product in product_display:
                self.product_concentrations[product[0]] = []
                self.product_concentrations[product[0]].append(0)
                print(self.product_concentrations[product[0]])

            for step in range(timestep):
                print("\n")
                diff_eq_reactant = -k  # d[Reactant]/dt, since all reactants have a common differential eq, just expressed differently, find the general equation
                diff_eq_product = k
                # REACTANTS CONC SOLVER
                for reactant in reactant_display:
                    diff_eq_reactant *= float(reactant[1]) ** float(reactant[2])
                    diff_eq_reactant *= float(reactant[1]) ** float(reactant[2])
                    # now calculate k values for each reactant
                    k1 = diff_eq_reactant
                    temp_conc_1 = (self.reactant_concentrations[reactant[0]][-1]) + (
                                k1 * dt) / 2  # halfway concentration
                    k2 = -k * temp_conc_1
                    temp_conc_2 = (self.reactant_concentrations[reactant[0]][-1]) + (k2 * dt) / 2
                    k3 = -k * temp_conc_2
                    temp_conc_3 = (self.reactant_concentrations[reactant[0]][-1]) + k3 * dt
                    k4 = -k * temp_conc_3

                    final_conc = (self.reactant_concentrations[reactant[0]][-1]) + (dt / 6) * (
                                k1 + 2 * k2 + 2 * k3 + k4)
                    self.reactant_concentrations[reactant[0]].append(final_conc)
                    print(self.reactant_concentrations[reactant[0]])
                # PRODUCTS

                for product in product_display:
                    # now calculate k values for each reactant
                    k1 = diff_eq_product
                    temp_conc_1 = (self.product_concentrations[product[0]][-1]) + (k1 * dt) / 2  # halfway concentration
                    k2 = -k * temp_conc_1
                    temp_conc_2 = (self.product_concentrations[product[0]][-1]) + (k2 * dt) / 2
                    k3 = -k * temp_conc_2
                    temp_conc_3 = (self.product_concentrations[product[0]][-1]) + k3 * dt
                    k4 = -k * temp_conc_3

                    final_conc = (self.product_concentrations[product[0]][-1]) + (dt / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
                    self.product_concentrations[product[0]].append(final_conc)
                    print(self.product_concentrations[product[0]])


GUI = GUI()
GUI.root.mainloop()


for product in product_display:
    r = random.random()
    b = random.random()
    g = random.random()
    color = (r, g, b)
    plt.plot(GUI.product_concentrations[product[0]],c=color)

for reactant in reactant_display:
    r = random.random()
    b = random.random()
    g = random.random()
    color = (r, g, b)
    plt.plot(GUI.reactant_concentrations[reactant[0]],c=color)
plt.title("Concentration of species in reaction vessel over time")
plt.show()