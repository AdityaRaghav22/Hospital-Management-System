import database.db_department as dept
import backend.utils as util

def add_dept(name, description):
    name = name.title().strip()
    description = description.title().strip()

    if dept.department_exists(name):
        print("Department Already Exists")
        return False
    
    try:
        dept_id = util.generate_id("department")
        dept.insert_dept(dept_id, name, description)
        print(f"Department Successfully Added: {name}")
        return True
    
    except Exception as e:
        print(f"[X] Failed To Add Department: {name}. Error: {e}")
        return False        

def delete_dept(id):

    if not util.validate_id(id, "DEPT"):
        print("Enter Valid Department Id")
        return False
    
    if dept.department_exists_id(id):
        try:
            dept.delete_department(id)
            print(f"Department Successfully Deleted: {id}")
            return True
        except Exception as e:
            print(f"[X] Failed To Delete Department: {id}. Error: {e}")
            return False
    else:
        print(f"[X] Department Don't Exists With Id: {id}")
        return False
    
def update_department(dept_id, name= None, description= None):

    if not util.validate_id(dept_id, "DEPT"):
        print("Enter Valid Department Id")
        return False
    
    if dept.department_exists_id(dept_id):
        try:
            if name:
                name = name.title().strip()
                dept.update_department(dept_id,name)
                print(f"Department Name Successfully Updated: {name}")

            if description:
                description = description.title().strip()
                dept.update_department(dept_id, description)
                print(f"Department Description Successfully Updated: {description}")
            return True
        
        except Exception as e:
            print(f"[X] Failed To Update Department With Id: {dept_id}. Error: {e}")
            return False
        
    else:
        print(f"[X] Department Don't Exists With Id: {dept_id}")
        return False
    
def view_one_dept(dept_id):
    
    if not util.validate_id(dept_id, "DEPT"):
        print("Enter Valid Department Id")
        return False
    
    if dept.department_exists_id(dept_id):
        try:
            dept_details = dept.view_department(dept_id)
            result = {
                "id" : dept_details["department_id"],
                "name": dept_details["department_name"],
                "description" : dept_details["department_description"]
            }
            print(f"Department's Details Successfully Fetched With Id: {dept_id}")
            return True, result
        except Exception as e:
            print(f"[X] Failed To Fetch Department's Details With Id: {dept_id}. Error: {e}")
            return False, {}
    else:
        print(f"[X] Department Don't Exists With Id: {dept_id}")
        return False, {}
    
def view_all_dept():
    try:
        dept_list = dept.view_all_departments()
        result = {
            "departments" : dept_list
        }
        print(f"{len(dept_list)} Departments Successfully Fetched ")
        return True, result
    except Exception as e:
        print(f"[X] Failed To Fetch Departments Details. Error: {e}")
        return False, {"departments" : []}
