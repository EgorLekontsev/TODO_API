async function loadTodos() {
    const res = await fetch('/todos');
    const todos = await res.json();
    const list = document.getElementById('todo-list');
    list.innerHTML = '';
    todos.forEach(todo => {
        const li = document.createElement('li');

        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.checked = todo.completed;
        checkbox.onchange = async () => {
            await fetch(`/todos/${todo.id}?completed=${checkbox.checked}`, {
                method: 'PATCH'
            });
            loadTodos();
        };

        const label = document.createElement('label');
        label.textContent = todo.title;
        if (todo.completed) {
            label.classList.add('completed');
        }

        li.appendChild(checkbox);
        li.appendChild(label);
        list.appendChild(li);
    });
}

document.getElementById('todo-form').addEventListener('submit', async e => {
    e.preventDefault();
    const input = document.getElementById('todo-title');
    const title = input.value.trim();
    if (!title) return;

    await fetch('/todos', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({title})
    });

    input.value = '';
    loadTodos();
});

loadTodos();
