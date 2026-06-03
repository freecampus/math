"""Small helpers for notebook display code."""

from __future__ import annotations

from dataclasses import dataclass

import ipywidgets as widgets
from IPython.display import display as ipython_display


@dataclass(frozen=True)
class NotebookDisplay:
    """A pair of controls and output widgets for notebook interfaces."""

    controls: widgets.Widget
    output: widgets.Widget

    def display(self) -> None:
        """Display controls and output in a notebook frontend."""

        ipython_display(self.controls)  # type: ignore[no-untyped-call]
        ipython_display(self.output)  # type: ignore[no-untyped-call]
