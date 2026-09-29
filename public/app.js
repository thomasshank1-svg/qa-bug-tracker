let state = { bugs: [], statuses: [], severities: [] };
function render() {
  $("#total").textContent = `${state.bugs.length} bugs`;
  $("#severity").innerHTML = state.severities.map((s) => `<option>${esc(s)}</option>`).join("");
  $("#bugs").innerHTML = state.bugs.map((bug) => `
    <article class="item bug">
      <div><span class="pill ${bug.severity === "Critical" || bug.severity === "High" ? "bad" : ""}">${esc(bug.severity)}</span><h3>#${bug.id} ${esc(bug.title)}</h3><p>${esc(bug.area)}</p><p class="small muted">${esc(bug.steps || "No steps")}</p></div>
      <select data-status="${bug.id}">${state.statuses.map((s) => `<option ${s === bug.status ? "selected" : ""}>${esc(s)}</option>`).join("")}</select>
    </article>
  `).join("");
  document.querySelectorAll("[data-status]").forEach((select) => select.addEventListener("change", () => action(select, async () => {
    await api("/api/status", { id: Number(select.dataset.status), status: select.value });
    await refresh();
  })));
}
async function refresh() { state = await api("/api/state"); render(); }
$("#bugForm").addEventListener("submit", (event) => {
  event.preventDefault();
  action(event.submitter, async () => {
    await api("/api/bugs", Object.fromEntries(new FormData(event.currentTarget)));
    event.currentTarget.reset();
    await refresh();
  });
});
refresh().catch((error) => toast(error.message));
