(() => {
  "use strict";

  const script = document.currentScript;
  const assetBase = script
    ? new URL(".", script.src)
    : new URL("./assets/", location.href);
  const STORAGE_KEY = "fcmath.progress.v1";
  const SCHEMA_VERSION = 1;
  // Map a curriculum version to stable-ID renames required for the next one.
  // Add entries here before changing or removing any published curriculum ID.
  const CURRICULUM_MIGRATIONS = Object.freeze({});
  let curriculum = null;
  let pageMap = null;

  function emptyState() {
    return {
      schemaVersion: SCHEMA_VERSION,
      curriculumVersion: pageMap?.curriculumVersion || 1,
      completed: {},
    };
  }

  function migrateState(candidate) {
    if (!candidate || typeof candidate !== "object") return emptyState();
    if (
      candidate.schemaVersion === 1 &&
      candidate.completed &&
      typeof candidate.completed === "object"
    ) {
      return migrateCurriculumState({
        schemaVersion: 1,
        curriculumVersion: Number(candidate.curriculumVersion) || 1,
        completed: Object.fromEntries(
          Object.entries(candidate.completed).filter(
            ([id, value]) =>
              typeof id === "string" && typeof value === "string",
          ),
        ),
      });
    }
    // The only supported legacy shape was a flat array of completed IDs.
    if (Array.isArray(candidate.completed)) {
      const timestamp = new Date().toISOString();
      return migrateCurriculumState({
        ...emptyState(),
        completed: Object.fromEntries(
          candidate.completed.map((id) => [String(id), timestamp]),
        ),
      });
    }
    return emptyState();
  }

  function migrateCurriculumState(state) {
    const targetVersion = pageMap?.curriculumVersion || 1;
    if (state.curriculumVersion > targetVersion) return emptyState();
    const migrated = { ...state, completed: { ...state.completed } };
    while (migrated.curriculumVersion < targetVersion) {
      const renames =
        CURRICULUM_MIGRATIONS[migrated.curriculumVersion] || Object.freeze({});
      migrated.completed = Object.fromEntries(
        Object.entries(migrated.completed).map(([id, timestamp]) => [
          renames[id] || id,
          timestamp,
        ]),
      );
      migrated.curriculumVersion += 1;
    }
    return migrated;
  }

  function loadState() {
    try {
      return migrateState(
        JSON.parse(localStorage.getItem(STORAGE_KEY) || "null"),
      );
    } catch (_error) {
      return emptyState();
    }
  }

  function saveState(state) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    window.dispatchEvent(
      new CustomEvent("fcmath:progress-changed", { detail: state }),
    );
  }

  function currentPageId() {
    if (!pageMap?.pages) return null;
    const path = decodeURIComponent(location.pathname).replace(
      /\/+$/,
      "/index.html",
    );
    for (const [source, id] of Object.entries(pageMap.pages)) {
      const rendered = `/${source.replace(/\.qmd$/, ".html")}`;
      if (
        path.endsWith(rendered) ||
        (rendered.endsWith("/index.html") &&
          path.endsWith(rendered.slice(0, -10)))
      ) {
        return id;
      }
    }
    return null;
  }

  function lessonProgress(pageId) {
    if (!pageId || document.querySelector(".lesson-completion")) return;
    const target =
      document.querySelector("main .quarto-title-block") ||
      document.querySelector("main header") ||
      document.querySelector("main");
    if (!target) return;
    const panel = document.createElement("aside");
    panel.className = "lesson-completion";
    panel.setAttribute("aria-label", "Lesson completion");
    const button = document.createElement("button");
    button.type = "button";
    button.className = "btn btn-sm btn-outline-primary";
    panel.append(button);
    const source = Object.entries(pageMap.pages).find(
      ([, id]) => id === pageId,
    )?.[0];
    if (source && pageMap.notebooks?.[source]) {
      const colab = document.createElement("a");
      colab.className = "btn btn-sm btn-outline-secondary";
      colab.href = pageMap.notebooks[source];
      colab.target = "_blank";
      colab.rel = "noopener";
      colab.textContent = "Open complete lesson in Colab";
      panel.append(colab);
    }

    const render = () => {
      const complete = Boolean(loadState().completed[pageId]);
      button.textContent = complete
        ? "Completed — mark incomplete"
        : "Mark this lesson complete";
      button.setAttribute("aria-pressed", String(complete));
      panel.classList.toggle("is-complete", complete);
    };
    button.addEventListener("click", () => {
      const state = loadState();
      if (state.completed[pageId]) delete state.completed[pageId];
      else state.completed[pageId] = new Date().toISOString();
      saveState(state);
      render();
      announce(
        state.completed[pageId]
          ? "Lesson marked complete."
          : "Lesson marked incomplete.",
      );
    });
    window.addEventListener("fcmath:progress-changed", render);
    render();
    target.insertAdjacentElement("afterend", panel);
  }

  function allCourseItems() {
    if (!curriculum?.courses) return [];
    const assessments = Object.fromEntries(
      (curriculum.assessments || []).map((assessment) => [
        assessment.id,
        assessment,
      ]),
    );
    return curriculum.courses.map((course) => ({
      id: course.id,
      title: course.title,
      items: course.units.flatMap((unit) => {
        const unitAssessments = (unit.assessment_ids || [])
          .map((assessmentId) => assessments[assessmentId])
          .filter(Boolean);
        return [...unit.lessons, ...unit.challenges, ...unitAssessments];
      }),
    }));
  }

  function renderDashboards() {
    const state = loadState();
    document.querySelectorAll("[data-progress-summary]").forEach((root) => {
      const courses = allCourseItems();
      const total = courses.reduce(
        (sum, course) => sum + course.items.length,
        0,
      );
      const completed = courses.reduce(
        (sum, course) =>
          sum + course.items.filter((item) => state.completed[item.id]).length,
        0,
      );
      const percent = total ? Math.round((completed / total) * 100) : 0;
      root.replaceChildren();
      const overall = document.createElement("div");
      overall.className = "progress-overall";
      overall.innerHTML = `
        <p><strong>${completed} of ${total} catalog activities complete</strong></p>
        <progress max="${
          total || 1
        }" value="${completed}">${percent}%</progress>
        <p>${percent}% complete in this browser</p>`;
      root.append(overall);
      const list = document.createElement("ul");
      list.className = "course-progress-list";
      courses.forEach((course) => {
        const done = course.items.filter(
          (item) => state.completed[item.id],
        ).length;
        const item = document.createElement("li");
        item.innerHTML = `<span>${course.title}</span><span>${done}/${course.items.length}</span>`;
        list.append(item);
      });
      root.append(list);
    });
  }

  function exportProgress() {
    const blob = new Blob([`${JSON.stringify(loadState(), null, 2)}\n`], {
      type: "application/json",
    });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = `freecampus-math-progress-${new Date()
      .toISOString()
      .slice(0, 10)}.json`;
    link.click();
    URL.revokeObjectURL(link.href);
    announce("Progress exported.");
  }

  async function importProgress(file) {
    const parsed = JSON.parse(await file.text());
    const legacy = Array.isArray(parsed?.completed);
    if (!parsed || (!legacy && parsed.schemaVersion !== SCHEMA_VERSION)) {
      throw new Error("This file is not a FreeCampus Math progress export.");
    }
    const targetVersion = pageMap?.curriculumVersion || 1;
    if (Number(parsed.curriculumVersion || 1) > targetVersion) {
      throw new Error("This progress file uses a newer curriculum version.");
    }
    const state = migrateState(parsed);
    saveState(state);
    announce("Progress imported.");
  }

  function bindManagement() {
    document
      .querySelector('[data-progress-action="export"]')
      ?.addEventListener("click", exportProgress);
    document
      .querySelector('[data-progress-action="import"]')
      ?.addEventListener("change", async (event) => {
        const file = event.target.files?.[0];
        if (!file) return;
        try {
          await importProgress(file);
        } catch (error) {
          announce(
            error instanceof Error ? error.message : "Progress import failed.",
          );
        } finally {
          event.target.value = "";
        }
      });
    document
      .querySelector('[data-progress-action="reset"]')
      ?.addEventListener("click", () => {
        if (
          !window.confirm(
            "Reset all FreeCampus Math progress stored in this browser?",
          )
        )
          return;
        saveState(emptyState());
        announce("Progress reset.");
      });
  }

  function announce(message) {
    const target = document.querySelector("[data-progress-announcement]");
    if (target) target.textContent = message;
  }

  async function initialize() {
    try {
      const [mapResponse, catalogResponse] = await Promise.all([
        fetch(new URL("curriculum-map.json", assetBase)),
        fetch(new URL("../courses/_catalog.yml", assetBase)),
      ]);
      if (mapResponse.ok) pageMap = await mapResponse.json();
      if (catalogResponse.ok) curriculum = await catalogResponse.json();
    } catch (_error) {
      // Completion controls degrade silently; the lesson itself remains complete.
    }
    lessonProgress(currentPageId());
    renderDashboards();
    bindManagement();
    window.addEventListener("fcmath:progress-changed", renderDashboards);
    window.addEventListener("storage", renderDashboards);
    document.addEventListener("fcmath:quiz-complete", (event) => {
      const id = event.detail?.id;
      if (typeof id !== "string") return;
      const state = loadState();
      state.completed[id] = new Date().toISOString();
      saveState(state);
      announce("Quiz completion saved in this browser.");
    });
  }

  document.addEventListener("DOMContentLoaded", initialize, { once: true });
})();
