import streamlit as st

# --- Base Class ---
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def get_info(self):
        return f"{self.name} earns ${self.salary}"

# --- Derived Classes ---
class Manager(Employee):
    def __init__(self, name, salary, team_size):
        super().__init__(name, salary)
        self.team_size = team_size

    def get_info(self):
        return f"👩‍💼 Manager {self.name} manages {self.team_size} people and earns ${self.salary}"

class Developer(Employee):
    def __init__(self, name, salary, language):
        super().__init__(name, salary)
        self.language = language

    def get_info(self):
        return f"💻 Developer {self.name} codes in {self.language} and earns ${self.salary}"

class Intern(Employee):
    def __init__(self, name, salary, duration_months):
        super().__init__(name, salary)
        self.duration = duration_months

    def get_info(self):
        return f"📘 Intern {self.name} is here for {self.duration} months and earns ${self.salary}"

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

# Display result
if submitted:
    if employee_type == "Manager":
        emp = Manager(name, salary, team_size)
    elif employee_type == "Developer":
        emp = Developer(name, salary, language)
    else:
        emp = Intern(name, salary, duration)

    st.success("✅ Employee Added!")
    st.markdown(f"### Profile\n{emp.get_info()}")
