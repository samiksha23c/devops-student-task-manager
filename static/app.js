document.addEventListener("DOMContentLoaded", () => {
  const filters = document.querySelectorAll("[data-filter]");
  const taskItems = document.querySelectorAll(".task-item");
  const emptyFilter = document.getElementById("empty-filter");

  filters.forEach((button) => {
    button.addEventListener("click", () => {
      filters.forEach((item) => item.classList.remove("active"));
      button.classList.add("active");
      const selected = button.dataset.filter;
      let visible = 0;
      taskItems.forEach((task) => {
        const show = selected === "all" || task.dataset.status === selected;
        task.hidden = !show;
        if (show) visible += 1;
      });
      if (emptyFilter) emptyFilter.hidden = visible !== 0;
    });
  });

  const titleInput = document.getElementById("title");
  if (titleInput) titleInput.focus({ preventScroll: true });
});
