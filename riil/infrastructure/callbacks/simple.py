# riil/infrastructure/callbacks/simple.py
"""
Simple print-based logger.
No dependencies.
"""
from riil.core.callback import Callback


class SimplePrintCallback(Callback):
    async def on_step_start(self, step, inputs, context):
        print(f"➡️ Starting: {step.__class__.__name__}")

    async def on_step_end(self, step, outputs, context):
        print(f"✅ Done: {step.__class__.__name__}")

    async def on_error(self, step, error, context):
        print(f"❌ Error in {step.__class__.__name__}: {str(error)}")
