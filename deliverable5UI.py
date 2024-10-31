import tkinter as tk
from tkinter import ttk, messagebox
import commendlin  # Import your commendlin.py functions

# Global variables
global input_frame, result_tree, primary_key_entry, column_dropdown, new_value_entry, table_dropdown
global so_condition1_entry, so_condition2_entry, set_operation_dropdown
global subquery_entry, membership_type_dropdown
global sc_condition1_entry, sc_condition2_entry, comparison_type_dropdown
global entries

# ===============================
# Data Mappings for Tables
# ===============================
table_columns = {
    "Patient": ["FirstName", "LastName", "DateOfBirth", "Gender", "Address", "PhoneNumber", "Email"],
    "Doctor": ["DepartmentID", "FirstName", "LastName", "Specialty", "PhoneNumber", "Email", "OfficeLocation", "LicenseNumber","Salary"],
    "Department": ["DepartmentName", "Location", "PhoneExtension", "HeadOfDepartment"],
    "Appointment": ["PatientID", "DoctorID", "AppointmentDate", "AppointmentTime", "Reason", "Status"],
    "MedicalRecord": ["PatientID", "DoctorID", "Diagnosis", "TreatmentPlan", "Prescription", "RecordDate", "Notes"],
    "Staff": ["DepartmentID", "FirstName", "LastName", "Role", "PhoneNumber", "Email"]
}

primary_keys = {
    "Patient": "PatientID",
    "Doctor": "DoctorID",
    "Department": "DepartmentID",
    "Appointment": "AppointmentID",
    "MedicalRecord": "RecordID",
    "Staff": "StaffID"
}

# ===============================
# Database Operations (CRUD)
# ===============================
def read_from_db():
    selected_table = table_dropdown.get()
    if selected_table == "Choose Table":
        messagebox.showerror("Error", "Please select a table")
        return

    columns, data = commendlin.read_data(selected_table.lower())
    clear_treeview(result_tree)
    setup_treeview(result_tree, columns)

    for row in data:
        result_tree.insert("", "end", values=row)

def insert_into_db():
    selected_table = table_dropdown.get()
    if selected_table == "Choose Table":
        messagebox.showerror("Error", "Please select a table")
        return

    values = [entry.get() for entry in entries]
    result = commendlin.insert_data(selected_table.lower(), values)
    messagebox.showinfo("Result", result)

def update_in_db():
    selected_table = table_dropdown.get()
    if selected_table == "Choose Table":
        messagebox.showerror("Error", "Please select a table")
        return

    primary_key_value = primary_key_entry.get()
    column = column_dropdown.get()
    new_value = new_value_entry.get()

    if not primary_key_value or not column or not new_value:
        messagebox.showerror("Error", "Please fill in all fields")
        return

    primary_key = primary_keys[selected_table]
    result = commendlin.update_data(selected_table.lower(), primary_key, primary_key_value, column, new_value)
    messagebox.showinfo("Result", result)

def delete_from_db():
    selected_table = table_dropdown.get()
    if selected_table == "Choose Table":
        messagebox.showerror("Error", "Please select a table")
        return

    primary_key_value = primary_key_entry.get()
    if not primary_key_value:
        messagebox.showerror("Error", "Please enter a primary key value")
        return

    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this record?")
    if confirm:
        result = commendlin.delete_data(selected_table.lower(), primary_key_value)
        messagebox.showinfo("Result", result)

# ===============================
# Set Operations
# ===============================
def set_operations_single_table():
    selected_table = table_dropdown.get()
    condition1 = so_condition1_entry.get()
    condition2 = so_condition2_entry.get()
    operation = set_operation_dropdown.get()

    if selected_table == "Choose Table":
        messagebox.showerror("Error", "Please select a table")
        return

    if not condition1 or not condition2:
        messagebox.showerror("Error", "Please provide both conditions")
        return

    result = commendlin.set_operations_single_table(selected_table.lower(), condition1, condition2, operation)
    
    if result:
        clear_treeview(result_tree)
        setup_treeview(result_tree, [f"Column{i+1}" for i in range(len(result[0]))])
        for row in result:
            result_tree.insert("", "end", values=row)
    else:
        messagebox.showinfo("Result", "No matching records found.")

# ===============================
# Set Membership
# ===============================
def set_membership():
    selected_table = table_dropdown.get()
    column = set_membership_column_dropdown.get()
    subquery = subquery_entry.get()
    check_type = membership_type_dropdown.get()

    if selected_table == "Choose Table":
        messagebox.showerror("Error", "Please select a table")
        return

    if column == "Select Column" or not subquery:
        messagebox.showerror("Error", "Please select a column and provide a subquery")
        return

    result = commendlin.set_membership(selected_table.lower(), column, subquery, check_type)

    if isinstance(result, tuple) and len(result) == 2:
        columns, data = result
        if data:
            clear_treeview(result_tree)
            setup_treeview(result_tree, columns)
            for row in data:
                result_tree.insert("", "end", values=row)
        else:
            messagebox.showinfo("Result", "No matching records found.")
    else:
        messagebox.showerror("Error", str(result))

# ===============================
# Set Comparison
# ===============================
def set_comparison():
    selected_table = table_dropdown.get()
    condition1 = sc_condition1_entry.get()
    condition2 = sc_condition2_entry.get()
    comparison_type = comparison_type_dropdown.get()

    if selected_table == "Choose Table" or comparison_type == "Choose Comparison":
        messagebox.showerror("Error", "Please select a table and a comparison type")
        return

    if not condition1 or not condition2:
        messagebox.showerror("Error", "Please provide both conditions")
        return

    result, set1, set2 = commendlin.set_comparison(selected_table.lower(), condition1, condition2, comparison_type)

    if isinstance(result, bool):
        result_message = f"Set Comparison Result ({comparison_type}): {result}"
        messagebox.showinfo("Set Comparison Result", result_message)

        clear_treeview(result_tree)
        result_tree["columns"] = ("Set", "Data")
        result_tree["show"] = "headings"
        for col in ("Set", "Data"):
            result_tree.heading(col, text=col)
            result_tree.column(col, anchor="center", width=300, stretch=True)

        for item in set1:
            result_tree.insert("", "end", values=("Set 1", str(item)))
        for item in set2:
            result_tree.insert("", "end", values=("Set 2", str(item)))
    else:
        messagebox.showerror("Error", result)

# ===============================
# WITH Clause
# ===============================
def execute_with_clause_query():
    # Get the selected or custom CTE (WITH clause) and the main query from the user
    selected_cte = with_clause_dropdown.get()
    custom_cte = cte_entry.get()
    main_query = main_query_entry.get()

    # If custom CTE is entered, use that; otherwise, use the selected predefined CTE
    if custom_cte:
        cte_query = custom_cte
    else:
        cte_query = selected_cte

    if not cte_query or not main_query:
        messagebox.showerror("Error", "Please provide both the WITH clause and the main query")
        return

    # Print the query for debugging
    print(f"Executing WITH clause query: {cte_query} {main_query}")

    # Call the backend function to execute the query
    result = commendlin.with_clause_subquery(cte_query, main_query)

    if isinstance(result, list) and result:
        clear_treeview(result_tree)
        setup_treeview(result_tree, [f"Column{i+1}" for i in range(len(result[0]))])
        for row in result:
            result_tree.insert("", "end", values=row)
    else:
        messagebox.showinfo("Result", "No matching records found or error occurred.")

# ===============================
# Advanced Aggregate
# ===============================
def execute_advanced_aggregate():
    selected_table = "Doctor"  # Since Salary is only in the Doctor table
    selected_column = "Salary"  # We are only working with the Salary column
    aggregate_function = aggregate_function_dropdown.get()  # e.g., SUM, AVG, etc.

    if aggregate_function == "Choose Function":
        messagebox.showerror("Error", "Please select an aggregate function.")
        return

    # Build the query string for aggregate function
    query = f"SELECT {aggregate_function}({selected_column}) FROM {selected_table.lower()}"
    print(f"Executing query: {query}")

    # Execute the query using commendlin
    result = commendlin.execute_query(query)
    if result:
        # Display the result in the Treeview
        clear_treeview(result_tree)
        setup_treeview(result_tree, ["Result"])
        for row in result:
            result_tree.insert("", "end", values=row)
    else:
        messagebox.showinfo("Result", "No matching records found.")

# ===============================
# OLAP
# ===============================
def execute_olap_function():
    selected_table = "Doctor"  # We're using the Doctor table for this example
    olap_function = olap_function_dropdown.get()
    partition_column = partition_dropdown.get()

    if olap_function == "Choose OLAP Function" or partition_column == "Choose Partition Column":
        messagebox.showerror("Error", "Please select an OLAP function and partition column.")
        return

    # Construct the OLAP query based on user selections
    if partition_column == "None":
        query = f"""
        SELECT 
            FirstName, 
            LastName, 
            Salary, 
            {olap_function}() OVER (ORDER BY Salary DESC) AS ranking
        FROM {selected_table}
        ORDER BY ranking;
        """
    else:
        query = f"""
        SELECT 
            FirstName, 
            LastName, 
            Salary, 
            {partition_column},
            {olap_function}() OVER (PARTITION BY {partition_column} ORDER BY Salary DESC) AS ranking
        FROM {selected_table}
        ORDER BY {partition_column}, ranking;
        """

    print(f"Executing OLAP query: {query}")

    # Execute the OLAP query using commendlin
    result = commendlin.execute_query(query)
    if isinstance(result, list) and result:
        clear_treeview(result_tree)
        setup_treeview(result_tree, ["FirstName", "LastName", "Salary", partition_column, "Ranking"])
        for row in result:
            result_tree.insert("", "end", values=row)
    else:
        messagebox.showinfo("Result", str(result) if isinstance(result, str) else "No matching records found or an error occurred.")


# ===============================
# Utility Functions
# ===============================
def clear_all():
    table_dropdown.set("Choose Table")
    
    for widget in input_frame.winfo_children():
        if isinstance(widget, tk.Entry):
            widget.delete(0, tk.END)
        elif isinstance(widget, ttk.Combobox):
            widget.set('')

    if primary_key_entry:
        primary_key_entry.delete(0, tk.END)
    if column_dropdown:
        column_dropdown.set("Select Column")
    if new_value_entry:
        new_value_entry.delete(0, tk.END)

    clear_treeview(result_tree)

    result_tree["columns"] = ()
    result_tree["show"] = "tree"

    messagebox.showinfo("Clear", "All fields have been cleared.")

def create_expandable_frame(parent, title):
    frame = ttk.Frame(parent)
    frame.pack(fill="x", pady=5)

    def toggle_frame():
        if toggle_btn.config('text')[-1] == '▼':
            toggle_btn.config(text='▶')
            content_frame.pack_forget()
        else:
            toggle_btn.config(text='▼')
            content_frame.pack(fill="x")

    toggle_btn = ttk.Button(frame, text="▶", width=2, command=toggle_frame)
    toggle_btn.pack(side="left")

    title_label = ttk.Label(frame, text=title)
    title_label.pack(side="left", padx=(5, 0))

    content_frame = ttk.Frame(frame)
    return content_frame

def clear_treeview(treeview):
    for item in treeview.get_children():
        treeview.delete(item)

def setup_treeview(treeview, columns):
    treeview["columns"] = columns
    treeview["show"] = "headings"
    for col in columns:
        treeview.heading(col, text=col)
        treeview.column(col, anchor="center", width=150, stretch=True)

def update_column_dropdown(event):
    selected_table = table_dropdown.get()
    columns = table_columns.get(selected_table, [])
    
    # Update the main column dropdown
    if 'column_dropdown' in globals():
        column_dropdown["values"] = columns
        column_dropdown.set("Select Column")
    
    # Update the set membership column dropdown
    if 'set_membership_column_dropdown' in globals():
        set_membership_column_dropdown["values"] = columns
        set_membership_column_dropdown.set("Select Column")

    # Create input fields for the selected table
    if selected_table in table_columns:
        create_input_fields(selected_table)

# ===============================
# UI Element Creation
# ===============================
def create_input_fields(table):
    global primary_key_entry, column_dropdown, new_value_entry, entries
    for widget in input_frame.winfo_children():
        widget.destroy()

    entries = []
    columns = table_columns[table]
    
    # Create a frame for each row
    for i in range(0, len(columns), 3):  # Process 3 columns at a time
        row_frame = tk.Frame(input_frame)
        row_frame.pack(fill="x", pady=5)
        
        for j in range(3):
            if i + j < len(columns):
                col = columns[i + j]
                label = tk.Label(row_frame, text=f"{col}:", width=15, anchor="e")
                label.pack(side="left", padx=(0, 5))
                entry = tk.Entry(row_frame, width=20)
                entry.pack(side="left", padx=(0, 15))
                entries.append(entry)

    # Create a new row for primary key, column dropdown, and new value
    bottom_frame = tk.Frame(input_frame)
    bottom_frame.pack(fill="x", pady=5)

    primary_key_label = tk.Label(bottom_frame, text=f"{primary_keys[table]}:", width=15, anchor="e")
    primary_key_label.pack(side="left", padx=(0, 5))
    primary_key_entry = tk.Entry(bottom_frame, width=20)
    primary_key_entry.pack(side="left", padx=(0, 15))

    column_dropdown = ttk.Combobox(bottom_frame, values=table_columns[table], width=18)
    column_dropdown.set("Select Column")
    column_dropdown.pack(side="left", padx=(0, 5))

    new_value_label = tk.Label(bottom_frame, text="New Value:", width=15, anchor="e")
    new_value_label.pack(side="left", padx=(0, 5))
    new_value_entry = tk.Entry(bottom_frame, width=20)
    new_value_entry.pack(side="left")

    # Make sure the input_frame is visible
    input_frame.pack(pady=5, fill="x")

def create_set_operation_ui(parent):
    set_operation_label = tk.Label(parent, text="Set Operations:")
    set_operation_label.grid(row=0, column=0, padx=5, pady=5)

    global set_operation_dropdown
    set_operation_dropdown = ttk.Combobox(parent, values=["UNION", "INTERSECT", "EXCEPT"])
    set_operation_dropdown.set("Choose Operation")
    set_operation_dropdown.grid(row=0, column=1, padx=5, pady=5)

    global so_condition1_entry
    condition1_label = tk.Label(parent, text="Condition 1:")
    condition1_label.grid(row=0, column=2, padx=5, pady=5)
    so_condition1_entry = tk.Entry(parent, width=30)
    so_condition1_entry.grid(row=0, column=3, padx=5, pady=5)

    global so_condition2_entry
    condition2_label = tk.Label(parent, text="Condition 2:")
    condition2_label.grid(row=1, column=2, padx=5, pady=5)
    so_condition2_entry = tk.Entry(parent, width=30)
    so_condition2_entry.grid(row=1, column=3, padx=5, pady=5)

    btn_set_operation_single_table = tk.Button(
        parent, 
        text="Perform Set Operation", 
        command=set_operations_single_table
    )
    btn_set_operation_single_table.grid(row=2, column=0, columnspan=4, pady=5)

def create_set_membership_ui(parent):
    global membership_type_dropdown, set_membership_column_dropdown, subquery_entry

    membership_type_dropdown = ttk.Combobox(parent, values=["IN", "NOT IN"], width=10)
    membership_type_dropdown.set("IN")
    membership_type_dropdown.grid(row=0, column=0, padx=5, pady=5)

    column_label = tk.Label(parent, text="Column:")
    column_label.grid(row=0, column=1, padx=5, pady=5)

    set_membership_column_dropdown = ttk.Combobox(parent, values=["Select Column"], width=30)
    set_membership_column_dropdown.set("Select Column")
    set_membership_column_dropdown.grid(row=0, column=2, padx=5, pady=5)

    subquery_label = tk.Label(parent, text="Subquery:")
    subquery_label.grid(row=1, column=0, padx=5, pady=5)
    subquery_entry = tk.Entry(parent, width=80)
    subquery_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5)

    btn_set_membership = tk.Button(parent, text="Check Set Membership", command=set_membership)
    btn_set_membership.grid(row=2, column=0, columnspan=3, pady=10)

def create_set_comparison_ui(parent):
    global sc_condition1_entry, sc_condition2_entry, comparison_type_dropdown

    condition1_label = tk.Label(parent, text="Condition 1:")
    condition1_label.grid(row=0, column=0, padx=5, pady=5)
    sc_condition1_entry = tk.Entry(parent, width=30)
    sc_condition1_entry.grid(row=0, column=1, padx=5, pady=5)

    condition2_label = tk.Label(parent, text="Condition 2:")
    condition2_label.grid(row=1, column=0, padx=5, pady=5)
    sc_condition2_entry = tk.Entry(parent, width=30)
    sc_condition2_entry.grid(row=1, column=1, padx=5, pady=5)

    comparison_type_label = tk.Label(parent, text="Comparison Type:")
    comparison_type_label.grid(row=2, column=0, padx=5, pady=5)
    comparison_type_dropdown = ttk.Combobox(parent, values=["EQUAL", "SUBSET", "SUPERSET", "OVERLAPPING", "DISJOINT"], width=20)
    comparison_type_dropdown.set("Choose Comparison")
    comparison_type_dropdown.grid(row=2, column=1, padx=5, pady=5)

    btn_set_comparison = tk.Button(
        parent, 
        text="Compare Sets", 
        command=set_comparison
    )
    btn_set_comparison.grid(row=3, column=0, columnspan=2, pady=5)

def create_with_clause_ui(parent):
    global with_clause_dropdown, cte_entry, main_query_entry

    with_clause_label = tk.Label(parent, text="Select Predefined WITH Clause:")
    with_clause_label.grid(row=0, column=0, padx=5, pady=5)

    predefined_ctes = [
        "WITH AvgSalary AS (SELECT AVG(Salary) AS avg_salary FROM Doctor)",
        "WITH DeptCount AS (SELECT DepartmentID, COUNT(*) AS doc_count FROM Doctor GROUP BY DepartmentID)"
    ]
    with_clause_dropdown = ttk.Combobox(parent, values=predefined_ctes, width=60)
    with_clause_dropdown.set("Select Predefined WITH Clause")
    with_clause_dropdown.grid(row=0, column=1, padx=5, pady=5)

    cte_label = tk.Label(parent, text="Or Enter Custom WITH Clause:")
    cte_label.grid(row=1, column=0, padx=5, pady=5)
    cte_entry = tk.Entry(parent, width=80)
    cte_entry.grid(row=1, column=1, padx=5, pady=5)

    main_query_label = tk.Label(parent, text="Main Query:")
    main_query_label.grid(row=2, column=0, padx=5, pady=5)
    main_query_entry = tk.Entry(parent, width=80)
    main_query_entry.grid(row=2, column=1, padx=5, pady=5)

    btn_with_clause_query = tk.Button(parent, text="Execute WITH Clause Query", command=execute_with_clause_query)
    btn_with_clause_query.grid(row=3, column=0, columnspan=2, pady=5)

def create_advanced_aggregate_ui(root):
    # Create a frame to hold the Aggregate Function widgets
    agg_function_frame = tk.Frame(root)
    agg_function_frame.pack(pady=10)

    # Aggregate function label
    agg_function_label = tk.Label(agg_function_frame, text="Select Aggregate Function for Doctor's Salary:")
    agg_function_label.grid(row=0, column=0, padx=5, pady=5)

    # Dropdown for selecting the aggregate function
    global aggregate_function_dropdown
    aggregate_function_dropdown = ttk.Combobox(agg_function_frame, values=["SUM", "AVG", "MAX", "MIN", "COUNT"])
    aggregate_function_dropdown.set("Choose Function")
    aggregate_function_dropdown.grid(row=0, column=1, padx=5, pady=5)

    # Button to execute the selected aggregate function
    btn_execute_aggregate = tk.Button(agg_function_frame, text="Execute", command=execute_advanced_aggregate)
    btn_execute_aggregate.grid(row=0, column=2, padx=5, pady=5)

def create_olap_ui(root):
    olap_frame = tk.Frame(root)
    olap_frame.pack(pady=10)

    olap_function_label = tk.Label(olap_frame, text="Select OLAP Function:")
    olap_function_label.grid(row=0, column=0, padx=5, pady=5)

    global olap_function_dropdown
    olap_function_dropdown = ttk.Combobox(olap_frame, values=["RANK", "DENSE_RANK", "ROW_NUMBER"])
    olap_function_dropdown.set("Choose OLAP Function")
    olap_function_dropdown.grid(row=0, column=1, padx=5, pady=5)

    partition_label = tk.Label(olap_frame, text="Partition By:")
    partition_label.grid(row=0, column=2, padx=5, pady=5)

    global partition_dropdown
    partition_dropdown = ttk.Combobox(olap_frame, values=["None", "DepartmentID", "Specialty"])
    partition_dropdown.set("Choose Partition Column")
    partition_dropdown.grid(row=0, column=3, padx=5, pady=5)

    btn_execute_olap = tk.Button(olap_frame, text="Execute OLAP Function", command=execute_olap_function)
    btn_execute_olap.grid(row=0, column=4, padx=5, pady=5)

# ===============================
# Main Window Setup
# ===============================

def create_main_window():
    global table_dropdown, input_frame, result_tree

    root = tk.Tk()
    root.title("Healthcare Database Management")

    # Table selection - always visible
    table_selection_frame = tk.Frame(root)
    table_selection_frame.pack(pady=10, fill="x")

    label = tk.Label(table_selection_frame, text="Select a table to manage:", font=("Times New Roman", 14))
    label.pack(side="left", padx=10)

    table_dropdown = ttk.Combobox(table_selection_frame, values=list(table_columns.keys()))
    table_dropdown.set("Choose Table")
    table_dropdown.pack(side="left", padx=10)
    table_dropdown.bind("<<ComboboxSelected>>", update_column_dropdown)

    # Basic operations in expandable frame
    operations_frame = create_expandable_frame(root, "Basic Operations")
    
    global input_frame
    input_frame = tk.Frame(operations_frame)
    input_frame.pack(pady=5, fill="x")

    button_frame = tk.Frame(operations_frame)
    button_frame.pack(pady=10)

    btn_insert = tk.Button(button_frame, text="Insert Data", command=insert_into_db)
    btn_insert.grid(row=0, column=0, padx=5)

    btn_update = tk.Button(button_frame, text="Update Data", command=update_in_db)
    btn_update.grid(row=0, column=1, padx=5)

    btn_delete = tk.Button(button_frame, text="Delete Data", command=delete_from_db)
    btn_delete.grid(row=0, column=2, padx=5)

    btn_read = tk.Button(button_frame, text="Read Data", command=read_from_db)
    btn_read.grid(row=0, column=3, padx=5)

    btn_clear = tk.Button(button_frame, text="Clear All", command=clear_all)
    btn_clear.grid(row=0, column=4, padx=5)

    # Set operations UI
    set_operations_frame = create_expandable_frame(root, "Set Operations")
    create_set_operation_ui(set_operations_frame)

    # Set membership UI
    set_membership_frame = create_expandable_frame(root, "Set Membership")
    create_set_membership_ui(set_membership_frame)

    # Set comparison UI
    set_comparison_frame = create_expandable_frame(root, "Set Comparison")
    create_set_comparison_ui(set_comparison_frame)

    # WITH Clause UI
    with_clause_frame = create_expandable_frame(root, "WITH Clause")
    create_with_clause_ui(with_clause_frame)

    # Advanced Aggregate
    create_advanced_aggregate_ui(root)

    # OLAP Function UI
    create_olap_ui(root)

    # Treeview to display results in a table format
    result_tree = ttk.Treeview(root)
    result_tree.pack(fill='both', expand=True, padx=10, pady=10)

    scrollbar = ttk.Scrollbar(root, orient="vertical", command=result_tree.yview)
    result_tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side='right', fill='y')

    root.mainloop()

# Start the application
if __name__ == "__main__":
    create_main_window()