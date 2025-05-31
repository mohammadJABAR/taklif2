const apiUrl = "http://127.0.0.1:8000/tasks";

async function fetchTasks() {
  const res = await fetch(apiUrl);
  const tasks = await res.json();
  console.log(tasks);
  // TODO: نمایش در صفحه
}

fetchTasks();