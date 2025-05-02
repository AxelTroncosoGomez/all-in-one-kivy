from .basescreen import BaseScreen
from kivy.properties import ObjectProperty
from kivy.metrics import dp
from kivy.uix.codeinput import TextInput
from kivymd.uix.button import MDFloatingActionButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.menu import MDDropdownMenu
from kivymd.app import MDApp
from kivy.clock import Clock
from ..utils.dialogs.dialogs import show_snackbar
from ast import literal_eval

class AddRowDialog(MDBoxLayout):
    select_date_id = ObjectProperty()
    select_store_id = ObjectProperty()
    select_product_id = ObjectProperty()
    select_amount_id = ObjectProperty()
    select_price_id = ObjectProperty()

class AddRowButton(MDFloatingActionButton):
    datatable_container = ObjectProperty()
    add_row_button = ObjectProperty()
    db = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_new_spending_dialog = MDDialog(
            title="Add New Item",
            type="custom",
            content_cls=AddRowDialog(),
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    theme_text_color="Custom",
                    on_press=self.close_add_new_row_dialog
                ),
                MDFlatButton(
                    text="ADD",
                    theme_text_color="Custom",
                    on_press=self.add_row_to_table
                ),
            ],
        )

        self.dialog_content = self.add_new_spending_dialog.content_cls

    def add_row_to_table(self, row):
        # Get values from dialog
        self.date_from_input = self.dialog_content.ids.select_date_id.text
        self.store_from_input = self.dialog_content.ids.select_store_id.text
        self.product_from_input = self.dialog_content.ids.select_product_id.text
        self.amount_from_input = self.dialog_content.ids.select_amount_id.text
        self.price_from_input = self.dialog_content.ids.select_price_id.text

        if not all([
            self.store_from_input, 
            self.product_from_input, 
            self.amount_from_input, 
            self.price_from_input
        ]):
            show_snackbar("Please fill all fields")
            return

        # Create row data
        row_data = (
            self.date_from_input,
            self.store_from_input,
            self.product_from_input,
            int(self.amount_from_input),
            float(self.price_from_input)
        )
        try: 
            self.datatable_container.children[0].add_row(row_data)
            self.close_add_new_row_dialog(None)
        except Exception as e:
            show_snackbar(str(e))
        self.db.insert(row_data)

    def reset_inputs_from_dialog(self):
        self.dialog_content.ids.select_store_id.text = ""
        self.dialog_content.ids.select_product_id.text = ""
        self.dialog_content.ids.select_price_id.text = ""
    
    def close_add_new_row_dialog(self, instance_button):
        self.reset_inputs_from_dialog()
        self.add_new_spending_dialog.dismiss()

    def add_row_dialog(self):
        self.add_new_spending_dialog.open()

class SpendingsScreen(BaseScreen):
    top_appbar = ObjectProperty()
    spendings_screen_manager = ObjectProperty()
    content_spendings_screen = ObjectProperty()
    add_row_button = ObjectProperty()
    db = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.edit_spending_dialog = MDDialog(
            title="Edit Item",
            type="custom",
            content_cls=AddRowDialog(),
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    theme_text_color="Custom",
                    on_press = self.close_edit_spending_dialog
                ),
                MDFlatButton(
                    text="EDIT",
                    theme_text_color="Custom",
                    on_press = self.edit_row
                ),
            ],
        )
        self.edit_dialog_content = self.edit_spending_dialog.content_cls

        self.right_dropdown_items = [
            {
                "text": "Order by",
                "leading_icon": "order-bool-descending-variant",
                "on_release": lambda x="Order by": print("Ordering table..."),
            }
        ]

    def close_edit_spending_dialog(self, instance_button):
        self.edit_spending_dialog.dismiss()
        self.right_menu.dismiss()

    @staticmethod
    def _build_data_table(row_data):
        spendings_datatable = MDDataTable(
            check=True,
            pos_hint={"center_y": 0.5, "center_x": 0.5},
            use_pagination=False,
            column_data=[
                ("Fecha", dp(32)),
                ("Tienda", dp(18)),
                ("Nombre", dp(18)),
                ("Cantidad", dp(18)),
                ("Precio", dp(16)),
            ],
            row_data=row_data,
            sorted_on="Fecha",
        )
        # spendings_datatable.bind(on_check_press=self.on_check_press)
        return spendings_datatable

    def open_right_menu(self, button):
        self.right_menu = MDDropdownMenu(
            items = self.right_dropdown_items,
            width = dp(150)
        )
        self.right_menu.caller = button
        self.right_menu.open()

    def on_check_press(self, instance_table, current_row):
        checked_rows = []
        total_col_headings = instance_table.table_data.total_col_headings
        print("Estas son las filas")
        for i, row in enumerate(instance_table.table_data.row_data):
            print(f"Row: {row} indice: {instance_table.table_data.row_data.index(row)}")
            cell_row_obj = instance_table.table_data.view_adapter.get_visible_view(total_col_headings*i)
            is_row_active = cell_row_obj.ids.check.active
            print("Row active status: ", is_row_active)
            if is_row_active:
                checked_rows.append(row)

        print("Checked rows:", checked_rows)

        if len(checked_rows) == 1:
            self.right_dropdown_items = [
                {
                    "text": "Order by",
                    "leading_icon": "order-bool-descending-variant",
                    "on_release": lambda x="Order by", rows=checked_rows: print("Ordering table..."),
                },
                {
                    "text": "Edit",
                    "leading_icon": "pencil-outline",
                    "on_release": lambda x="Edit", rows=checked_rows: self.edit_row_dialog(x, rows),
                },
                {
                    "text": "Delete",
                    "leading_icon": "delete",
                    "on_release": lambda x="Delete", rows=checked_rows: self.delete_row_dialog(x, rows),
                }
            ]
        elif len(checked_rows) > 1:
            self.right_dropdown_items = [
                {
                    "text": "Order by",
                    "leading_icon": "order-bool-descending-variant",
                    "on_release": lambda x="Order by", rows=checked_rows: print("Ordering table..."),
                },
                {
                    "text": "Delete",
                    "leading_icon": "delete",
                    "on_release": lambda x="Delete", rows=checked_rows: self.delete_row_dialog(x, rows),
                }
            ]
        else:
            self.right_dropdown_items = [
                {
                    "text": "Order by",
                    "leading_icon": "order-bool-descending-variant",
                    "on_release": lambda x="Order by": print("Ordering table..."),
                }
            ]

    def delete_row_dialog(self, text_item, rows_checked):
        self.delete_row_confirmation_dialog = MDDialog(
            title="Confirm Action",
            type="confirmation",
            text="Are you sure?",
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    on_press=lambda _: self.delete_row_confirmation_dialog.dismiss()
                ),
                MDFlatButton(
                    text="OK",
                    on_press=lambda _: self.delete_rows(text_item, rows_checked)
                ),
            ],
        )
        self.delete_row_confirmation_dialog.open()

    def get_real_cell_values(self, cell):
        try:
            if isinstance(cell, int):
                return int(cell)
            elif isinstance(cell, float):
                return float(cell)
            else:
                raise
        except:
            val = str(cell)
        return val

    def delete_rows(self, text_item, rows_checked):
        for row in rows_checked:
            row_id = self.db.get_id_from_row(row)
            real_row = tuple(self.get_real_cell_values(cell) for cell in row)
            self.spendings_datatable.remove_row(real_row)
            self.db.delete_row_by_id(row_id)

        self.right_menu.dismiss()
        self.delete_row_confirmation_dialog.dismiss()
        self.spendings_datatable.table_data.select_all("normal")

    def edit_row_dialog(self, text_item, rows_checked):
        self.on_edit_row = rows_checked[0]
        self.real_on_edit_row = tuple(self.get_real_cell_values(cell) for cell in self.on_edit_row)
        print("Rows selected on edit_row()")
        print(rows_checked)
 
        self.edit_dialog_content.ids.select_date_id.text = str(self.on_edit_row[0])
        self.edit_dialog_content.ids.select_store_id.text = str(self.on_edit_row[1])
        self.edit_dialog_content.ids.select_product_id.text = str(self.on_edit_row[2])
        self.edit_dialog_content.ids.select_amount_id.text = str(self.on_edit_row[3])
        self.edit_dialog_content.ids.select_price_id.text = str(self.on_edit_row[4])

        self.edit_spending_dialog.open()

    def edit_row(self, instance_button):
        # TODO: Falta editar este
        new_row_date_edit = self.edit_dialog_content.ids.select_date_id.text
        new_row_store_edit = self.edit_dialog_content.ids.select_store_id.text
        new_row_product_edit = self.edit_dialog_content.ids.select_product_id.text
        new_row_amount_edit = self.edit_dialog_content.ids.select_amount_id.text
        new_row_price_edit = self.edit_dialog_content.ids.select_price_id.text

        new_row_data = (
            new_row_date_edit,
            new_row_store_edit,
            new_row_product_edit,
            int(new_row_amount_edit),
            float(new_row_price_edit)
        )

        self.spendings_datatable.update_row(
            old_data = self.real_on_edit_row,
            new_data = new_row_data
        )

        self.right_menu.dismiss()
        self.close_edit_spending_dialog(None)
        self.spendings_datatable.table_data.select_all("normal")
        on_edit_row_id = self.db.get_id_from_row(self.real_on_edit_row)
        print(f"Updating row with ID = {on_edit_row_id}")
        self.db.update(on_edit_row_id, new_row_data)


    def on_enter(self):
        print("Called on_enter() from SpendingsScreen()")
        # Delay the initialization logic by 0.3 seconds
        Clock.schedule_once(self.initialize_screen, 0.3)

    def initialize_screen(self, dt):
        # TODO: Volver todo esto a la "normalidad" y probar nuevamente sin Clock
        # Check if the MDDataTable is already added to the content_spendings_screen
        todays_records = self.db.select_data_from_date(exclude_id = True)
        print("Todays records")
        print(todays_records)

        self.spendings_datatable = self._build_data_table(todays_records)
        self.spendings_datatable.table_data.select_all("normal")
        self.spendings_datatable.bind(on_check_press=self.on_check_press)

        # if self.spendings_datatable not in self.content_spendings_screen.children:
        self.content_spendings_screen.clear_widgets()
        self.content_spendings_screen.add_widget(self.spendings_datatable)

        # Spendings Screen right button Options
        self.top_appbar.right_action_items = [
            ["dots-vertical", lambda x: self.open_right_menu(x)]
        ]