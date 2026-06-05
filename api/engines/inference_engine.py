

from datetime import datetime, timezone
from typing import Any, Dict, List

from api.core.logging import logger
from api.managers.model_manager import model_manager


class InferenceEngine:
    """Inference execution engine built on top of ModelManager."""

    def run(
        self,
        model_id: str,
        input_text: str,
    ) -> Dict[str, Any]:
        result = model_manager.run_inference(
            model_id=model_id,
            input_text=input_text,
        )

        logger.info(
            f"Inference engine executed model: {model_id}",
            source="inference_engine",
        )

        return result

    def history(self) -> List[Dict[str, Any]]:
        return model_manager.list_inferences()

    def health(self) -> Dict[str, Any]:
        return {
            "healthy": True,
            "engine": "inference_engine",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def diagnostics(self) -> Dict[str, Any]:
        return {
            "health": self.health(),
            "metrics": self.get_metrics(),
            "inferences": len(self.history()),
        }

    def get_metrics(self) -> Dict[str, Any]:
        metrics = model_manager.get_metrics()

        return {
            "engine": "inference_engine",
            **metrics,
        }


inference_engine = InferenceEngine()