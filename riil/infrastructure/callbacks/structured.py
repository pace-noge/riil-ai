# riil/infrastructure/callbacks/structured.py
"""
Structured JSON logger for ELK, Splunk, etc.
"""

import json
import sys
from datetime import datetime
from riil.core.callback import Callback


class StructuredJSONCallback(Callback):
    def _emit(self, event: str, data: dict):
        record = {
            "timestamp": datetime.utcnow().isoformat(),
            "event": event,
            **data
        }
        print(json.dumps(record), file=sys.stdout)

    async def on_step_start(self, step, inputs, context):
        self._emit("step.start", {
            "step_type": step.__class__.__name__,
            "inputs": self._safe(inputs)
        })

    async def on_step_end(self, step, outputs, context):
        self._emit("step.end", {
            "step_type": step.__class__.__name__,
            "outputs": self._safe(outputs)
        })

    async def on_error(self, step, error, context):
        self._emit("step.error", {
            "step_type": step.__class__.__name__,
            "error": str(error),
            "error_type": error.__class__.__name__
        })

    def _safe(self, data):
        return {k: v for k, v in data.items() if isinstance(v, (str, int, float, bool, dict, list, type(None)))}
