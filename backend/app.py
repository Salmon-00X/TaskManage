# backend/app.py

from flask import Flask, request, render_template, redirect, url_for
from algorithm import merge_sort, counting_sort, heap_sort, naive_string_search, insertion_sort

# Initialize the Flask application and specify the template folder
app = Flask(__name__, template_folder="../templates")

# Global variables for storing tasks and notes temporarily
tasks = []
notes = []

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route for the tasks page
@app.route('/tasks', methods=['GET', 'POST'])
def manage_tasks():
    global tasks
    if request.method == 'POST':
        # Get the form data from the request
        task_name = request.form.get('task_name')
        task_description = request.form.get('task_description')
        due_date = request.form.get('due_date')
        priority = int(request.form.get('priority'))

        # Check if form data is not empty
        if task_name and task_description and due_date:
            # Add new task to the list and sort using insertion sort
            tasks.append({
                'name': task_name,
                'description': task_description,
                'dueDate': due_date,
                'priority': priority
            })

            # Sort tasks immediately by due date using insertion sort
            tasks = insertion_sort(tasks, 'dueDate')

    # Render the tasks.html template with the current list of tasks
    return render_template('tasks.html', tasks=tasks)

# Route to sort tasks by due date using merge sort
@app.route('/sort_by_due_date', methods=['POST'])
def sort_by_due_date():
    global tasks
    tasks = merge_sort(tasks, 'dueDate')
    return redirect(url_for('manage_tasks'))

# Route to sort tasks by priority using counting sort
@app.route('/sort_by_priority', methods=['POST'])
def sort_by_priority():
    global tasks
    tasks = counting_sort(tasks, 'priority')
    return redirect(url_for('manage_tasks'))

# Route to sort tasks by both due date and priority using heap sort
@app.route('/sort_by_both', methods=['POST'])
def sort_by_both():
    global tasks
    tasks = heap_sort(tasks, 'dueDate', 'priority')
    return redirect(url_for('manage_tasks'))

# Route for the notes page
@app.route('/notes', methods=['GET', 'POST'])
def manage_notes():
    global notes
    if request.method == 'POST':
        note_title = request.form.get('note_title')
        note_content = request.form.get('note_content')

        # Check if form data is not empty
        if note_title and note_content:
            # Add new note to the list
            notes.append({
                'title': note_title,
                'content': note_content
            })

    # Render the notes.html template with the current list of notes
    return render_template('notes.html', notes=notes)

# Route to search notes using naive string search
@app.route('/search_notes', methods=['POST'])
def search_notes():
    global notes
    search_pattern = request.form.get('search_pattern')
    search_results = []

    # Perform naive string search on each note's title and content
    for note in notes:
        indices_title = naive_string_search(note['title'], search_pattern)
        indices_content = naive_string_search(note['content'], search_pattern)

        if indices_title or indices_content:
            search_results.append({
                'note': note,
                'indices_title': indices_title,
                'indices_content': indices_content
            })

    # Render the notes.html template with search results
    return render_template('notes.html', notes=notes, search_results=search_results, search_pattern=search_pattern)

# Run the Flask server
if __name__ == "__main__":
    app.run(debug=True)
