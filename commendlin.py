import mysql.connector

# Replace with your database connection details
def connect_db():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="peterlin",
        database="Healthcaredb"
    )
    return connection

def read_data(table):
    connection = connect_db()
    cursor = connection.cursor()

    try:
        query = f"SELECT * FROM {table}"
        cursor.execute(query)
        data = cursor.fetchall()

        # Fetch column names (optional, useful for display)
        columns = [desc[0] for desc in cursor.description]

        cursor.close()
        connection.close()

        return columns, data  # Return both column names and data

    except mysql.connector.Error as e:
        cursor.close()
        connection.close()
        return f"Error: {e}", None

def insert_data(table, values):
    connection = connect_db()
    cursor = connection.cursor()

    if table == "patient":
        query = """
            INSERT INTO Patient (FirstName, LastName, DateOfBirth, Gender, Address, PhoneNumber, Email)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
    elif table == "doctor":
        query = """
            INSERT INTO Doctor (DepartmentID, FirstName, LastName, Specialty, PhoneNumber, Email, OfficeLocation, LicenseNumber, Salary)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
    elif table == "department":
        query = """
            INSERT INTO Department (DepartmentName, Location, PhoneExtension, HeadOfDepartment)
            VALUES (%s, %s, %s, %s)
        """
    elif table == "appointment":
        query = """
            INSERT INTO Appointment (PatientID, DoctorID, AppointmentDate, AppointmentTime, Reason, Status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
    elif table == "medicalrecord":
        query = """
            INSERT INTO MedicalRecord (PatientID, DoctorID, Diagnosis, TreatmentPlan, Prescription, RecordDate, Notes)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
    elif table == "staff":
        query = """
            INSERT INTO Staff (DepartmentID, FirstName, LastName, Role, PhoneNumber, Email)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
    else:
        return "Table not found"

    try:
        cursor.execute(query, values)
        connection.commit()
        cursor.close()
        connection.close()
        return "Data inserted successfully"
    except mysql.connector.Error as e:
        cursor.close()
        connection.close()
        return f"Error: {e}"

def update_data(table, primary_key, primary_key_value, column, new_value):
    connection = connect_db()
    cursor = connection.cursor()

    try:
        if table == "patient":
            query = f"UPDATE Patient SET {column} = %s WHERE PatientID = %s"
        elif table == "doctor":
            query = f"UPDATE Doctor SET {column} = %s WHERE DoctorID = %s"
        elif table == "department":
            query = f"UPDATE Department SET {column} = %s WHERE DepartmentID = %s"
        elif table == "appointment":
            query = f"UPDATE Appointment SET {column} = %s WHERE AppointmentID = %s"
        elif table == "medicalrecord":
            query = f"UPDATE MedicalRecord SET {column} = %s WHERE RecordID = %s"
        elif table == "staff":
            query = f"UPDATE Staff SET {column} = %s WHERE StaffID = %s"
        else:
            return "Table not found"

        cursor.execute(query, (new_value, primary_key_value))
        connection.commit()

        if cursor.rowcount > 0:
            return f"Record updated successfully"
        else:
            return "No record found to update"

    except mysql.connector.Error as e:
        return f"Error: {e}"
    finally:
        cursor.close()
        connection.close()
    
def delete_data(table, primary_key_value):
    connection = connect_db()
    cursor = connection.cursor()

    try:
        if table == "patient":
            query = "DELETE FROM Patient WHERE PatientID = %s"
        elif table == "doctor":
            query = "DELETE FROM Doctor WHERE DoctorID = %s"
        elif table == "department":
            query = "DELETE FROM Department WHERE DepartmentID = %s"
        elif table == "appointment":
            query = "DELETE FROM Appointment WHERE AppointmentID = %s"
        elif table == "medicalrecord":
            query = "DELETE FROM MedicalRecord WHERE RecordID = %s"
        elif table == "staff":
            query = "DELETE FROM Staff WHERE StaffID = %s"
        else:
            return "Table not found"

        cursor.execute(query, (primary_key_value,))
        connection.commit()

        if cursor.rowcount > 0:
            return "Record deleted successfully"
        else:
            return "No record found to delete"

    except mysql.connector.Error as e:
        return f"Error: {e}"
    finally:
        cursor.close()
        connection.close()

def set_operations_single_table(table, condition1, condition2, operation):
    connection = connect_db()
    cursor = connection.cursor()

    valid_operations = ["UNION", "INTERSECT", "EXCEPT"]
    if operation not in valid_operations:
        return "Invalid set operation!"

    try:
        query1 = f"SELECT * FROM {table} WHERE {condition1}"
        query2 = f"SELECT * FROM {table} WHERE {condition2}"

        query = f"{query1} {operation} {query2}"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return result

    except mysql.connector.Error as e:
        cursor.close()
        connection.close()
        return f"Error: {e}"

def set_membership(table, column, subquery, check_type='IN'):
    connection = connect_db()
    cursor = connection.cursor()

    if check_type not in ['IN', 'NOT IN']:
        return "Invalid check type!", None

    try:
        query = f"SELECT * FROM {table} WHERE {column} {check_type} ({subquery})"
        cursor.execute(query)
        result = cursor.fetchall()
        
        # Fetch column names
        columns = [desc[0] for desc in cursor.description]
        
        cursor.close()
        connection.close()
        return columns, result

    except mysql.connector.Error as e:
        cursor.close()
        connection.close()
        return f"Error: {e}", None

def set_comparison(table, condition1, condition2, comparison_type):
    connection = connect_db()
    cursor = connection.cursor()

    valid_comparisons = ["EQUAL", "SUBSET", "SUPERSET", "OVERLAPPING", "DISJOINT"]
    if comparison_type not in valid_comparisons:
        return "Invalid comparison type!", None, None

    try:
        # Construct queries to fetch data for both conditions
        query1 = f"SELECT * FROM {table} WHERE {condition1}"
        query2 = f"SELECT * FROM {table} WHERE {condition2}"

        # Execute queries and convert results to sets for comparison
        cursor.execute(query1)
        set1 = set(tuple(row) for row in cursor.fetchall())

        cursor.execute(query2)
        set2 = set(tuple(row) for row in cursor.fetchall())

        # Perform set comparison based on the selected comparison type
        if comparison_type == "EQUAL":
            result = set1 == set2
        elif comparison_type == "SUBSET":
            result = set1.issubset(set2)
        elif comparison_type == "SUPERSET":
            result = set1.issuperset(set2)
        elif comparison_type == "OVERLAPPING":
            result = bool(set1.intersection(set2))
        elif comparison_type == "DISJOINT":
            result = set1.isdisjoint(set2)

        cursor.close()
        connection.close()
        return result, list(set1), list(set2)

    except mysql.connector.Error as e:
        cursor.close()
        connection.close()
        return f"Error: {e}", None, None
    
def with_clause_subquery(cte_query, main_query):
    connection = connect_db()
    cursor = connection.cursor()

    try:
        query = f"{cte_query} {main_query}"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return result

    except mysql.connector.Error as e:
        cursor.close()
        connection.close()
        return f"Error: {e}"

def execute_query(query):
    connection = connect_db()
    cursor = connection.cursor()

    try:
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return result
    except mysql.connector.Error as e:
        cursor.close()
        connection.close()
        return f"Error: {e}"

