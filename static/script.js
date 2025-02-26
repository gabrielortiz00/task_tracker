document.addEventListener("DOMContentLoaded", function () {
    const tasks = document.querySelectorAll("li");

    tasks.forEach(task => {
        task.addEventListener("click", () => {
            task.classList.toggle("completed");
        });
    });
});
