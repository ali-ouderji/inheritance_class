import streamlit as st
import pandas as pd

# --- Base Class ---
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def get_info(self):
        return f"{self.name} earns ${self.salary}"

    def to_dict(self):
        return {
            "Type": "Employee",
            "Name": self.name,
            "Salary": self.salary
        }

    def identity(self):
        return (self.name, "Employee")

# --- Derived Classes ---
class Manager(Employee):
    def __init__(self, name, salary, team_size):
        super().__init__(name, salary)
        self.team_size = team_size

    def get_info(self):
        return f"👩‍💼 Manager {self.name} manages {self.team_size} people and earns ${self.salary}"

    def to_dict(self):
        return {
            "Type": "Manager",
            "Name": self.name,
            "Salary": self.salary,
            "Team Size": self.team_size
        }

    def identity(self):
        return (self.name, "Manager")

class Developer(Employee):
    def __init__(self, name, salary, language):
        super().__init__(name, salary)
        self.language = language

    def get_info(self):
        return f"💻 Developer {self.name} codes in {self.language} and earns ${self.salary}"

    def to_dict(self):
        return {
            "Type": "Developer",
            "Name": self.name,
            "Salary": self.salary,
            "Language": self.language
        }

    def identity(self):
        return (self.name, "Developer")

class Intern(Employee):
    def __init__(self, name, salary, duration_months):
        super().__init__(name, salary)
        self.duration = duration_months

    def get_info(self):
        return f"📘 Intern {self.name} is here for {self.duration} months and earns ${self.salary}"

    def to_dict(self):
        return {
            "Type": "Intern",
            "Name": self.name,
            "Salary": self.salary,
            "Duration (months)": self.duration
        }

    def identity(self):
        return (self.name, "Intern")

# --- Initialize session state ---
if "employee_list" not in st.session_state:
    st.session_state.employee_list = []

# --- Streamlit UI ---
st.title("🏢 Employee Management System")
st.write("Demonstrates Python inheritance using real-world employee roles.")

employee_type = st.selectbox("Select Employee Type", ["Manager", "Developer", "Intern"])

with st.form("employee_form"):
    name = st.text_input("Name")
    salary = st.number_input("Salary", min_value=0, step=500)

    if employee_type == "Manager":
        team_size = st.number_input("Team Size", min_value=1)
    elif employee_type == "Developer":
        language = st.selectbox("Programming Language", ["Python", "JavaScript", "Java", "C++"])
    else:  # Intern
        duration = st.slider("Internship Duration (months)", min_value=1, max_value=12)

    submitted = st.form_submit_button("Add Employee")

# Add new employee (check for duplicates)
if submitted and name:
    # Create employee instance
    if employee_type == "Manager":
        emp = Manager(name, salary, team_size)
    elif employee_type == "Developer":
        emp = Developer(name, salary, language)
    else:
        emp = Intern(name, salary, duration)

    identities = [e.identity() for e in st.session_state.employee_list]
    if emp.identity() in identities:
        st.warning("⚠️ This employee already exists.")
    else:
        st.session_state.employee_list.append(emp)
        st.success("✅ Employee Added!")
        st.markdown(f"### Profile\n{emp.get_info()}")

# --- Show all employees with remove buttons ---
if st.session_state.employee_list:
    st.subheader("📋 All Employees")

    for idx, emp in enumerate(st.session_state.employee_list):
        col1, col2 = st.columns([5, 1])
        with col1:
            st.markdown(f"- {emp.get_info()}")
        with col2:
            if st.button("🗑️ Remove", key=f"remove_{idx}"):
                st.session_state.employee_list.pop(idx)
                st.experimental_rerun()

    # --- Download as CSV ---
    data = [emp.to_dict() for emp in st.session_state.employee_list]
    df = pd.DataFrame(data).fillna("")

    if not df.empty:
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download CSV", csv, "employees.csv", "text/csv")
else:
    st.info("No employees added yet.")
