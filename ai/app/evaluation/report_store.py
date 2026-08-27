import json
import os
import time
from typing import Any, Dict, List, Optional


class EvaluationReportStore:
    """
    Metadata & Benchmark Evaluation Report Store.
    Persists evaluation run metadata: model_id, model_version, prompt_task, prompt_version,
    dataset_id, dataset_version, evaluator_timestamp, pass_fail_status, and metric summary.
    """

    def __init__(self, reports_dir: Optional[str] = None):
        if not reports_dir:
            reports_dir = os.path.join(os.path.dirname(__file__), "reports")
        self.reports_dir = reports_dir
        os.makedirs(self.reports_dir, exist_ok=True)
        self.in_memory_reports: Dict[str, Dict[str, Any]] = {}

    def save_report(self, report_id: str, report_data: Dict[str, Any]) -> str:
        """
        Saves an evaluation report with full metadata.
        """
        report_data["report_id"] = report_id
        report_data["created_at"] = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())

        self.in_memory_reports[report_id] = report_data

        file_path = os.path.join(self.reports_dir, f"{report_id}.json")
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(report_data, f, indent=2)
        except Exception:
            pass

        return report_id

    def get_report(self, report_id: str) -> Optional[Dict[str, Any]]:
        if report_id in self.in_memory_reports:
            return self.in_memory_reports[report_id]

        file_path = os.path.join(self.reports_dir, f"{report_id}.json")
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return None

    def list_reports(self) -> List[Dict[str, Any]]:

        reports = list(self.in_memory_reports.values())
        if not reports and os.path.exists(self.reports_dir):
            for fn in os.listdir(self.reports_dir):
                if fn.endswith(".json"):
                    fp = os.path.join(self.reports_dir, fn)
                    try:
                        with open(fp, "r", encoding="utf-8") as f:
                            reports.append(json.load(f))
                    except Exception:
                        pass
        return reports


report_store = EvaluationReportStore()
