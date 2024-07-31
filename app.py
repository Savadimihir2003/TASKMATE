import streamlit as st
import pandas as pd
from datetime import datetime
import uuid

# Initialize task storage
if 'tasks' not in st.session_state:
    st.session_state.tasks = {}
if 'completed_tasks' not in st.session_state:
    st.session_state.completed_tasks = {}

# Function to add a task
def add_task(task, due_date, due_time):
    task_id = str(uuid.uuid4())
    due_datetime = datetime.combine(due_date, due_time)
    st.session_state.tasks[task_id] = {
        'task': task,
        'due_datetime': due_datetime,
        'completed': False
    }
    return task_id

# Function to display tasks
def display_tasks(tasks):
    if tasks:
        tasks_data = [
            {
                'Task ID': task_id,
                'Task': task_info['task'],
                'Due Date': task_info['due_datetime'].strftime('%Y-%m-%d'),
                'Due Time': task_info['due_datetime'].strftime('%H:%M'),
                'Completed': 'Yes' if task_info['completed'] else 'No'
            }
            for task_id, task_info in tasks.items()
        ]
        df = pd.DataFrame(tasks_data)
        st.table(df)
    else:
        st.write("No tasks.")

# Function to check for due tasks
def check_due_tasks():
    current_time = datetime.now()
    due_tasks = {
        task_id: task_info
        for task_id, task_info in st.session_state.tasks.items()
        if current_time >= task_info['due_datetime'] and not task_info['completed']
    }
    return due_tasks

# Function to mark task as complete
def complete_task(task_id):
    if task_id in st.session_state.tasks:
        st.session_state.tasks[task_id]['completed'] = True
        st.session_state.completed_tasks[task_id] = st.session_state.tasks.pop(task_id)

# Title
st.title("TASKMATE")
st.write("Your go-to-task Management Partner")

# Input form
with st.form(key='task_form'):
    task = st.text_input("Task")
    due_date = st.date_input("Due Date", value=datetime.now().date())
    due_time = st.time_input("Due Time", value=datetime.now().time())
    submit_button = st.form_submit_button(label='Add Task')
    if submit_button:
        task_id = add_task(task, due_date, due_time)
        st.success(f"Task '{task}' added with ID: {task_id}")
        st.experimental_rerun()  # Rerun the app to reset the form

# Display tasks
st.subheader("Tasks")
display_tasks(st.session_state.tasks)

# Sidebar
with st.sidebar:
    st.subheader("Due Tasks")
    due_tasks = check_due_tasks()
    if due_tasks:
        due_tasks_data = [
            {
                'Task': task_info['task'],
                'Status': 'Not Completed'
            }
            for task_id, task_info in due_tasks.items()
        ]
        df = pd.DataFrame(due_tasks_data)
        st.table(df)
    else:
        st.write("No due tasks.")

    st.subheader("Completed Tasks")
    if st.session_state.completed_tasks:
        completed_tasks_data = [
            {
                'Task': task_info['task'],
                'Status': 'Completed'
            }
            for task_id, task_info in st.session_state.completed_tasks.items()
        ]
        df = pd.DataFrame(completed_tasks_data)
        st.table(df)
    else:
        st.write("No completed tasks.")

# Button to mark tasks as completed
st.subheader("Mark Task as Completed")
task_id_to_complete = st.text_input("Task ID to Complete")
if st.button("Complete Task", key="complete_task_button"):
    if task_id_to_complete in st.session_state.tasks:
        task_name = st.session_state.tasks[task_id_to_complete]['task']
        complete_task(task_id_to_complete)
        st.session_state['success_message'] = f"Task '{task_name}' marked as completed."
        st.experimental_rerun()  # Rerun the app to update the sidebar
    elif task_id_to_complete in st.session_state.completed_tasks:
        task_name = st.session_state.completed_tasks[task_id_to_complete]['task']
        st.info(f"Task '{task_name}' is already completed.")
    else:
        st.error("Invalid Task ID.")

# Display success message
if 'success_message' in st.session_state:
    st.success(st.session_state['success_message'])
    del st.session_state['success_message']  # Clear the message
