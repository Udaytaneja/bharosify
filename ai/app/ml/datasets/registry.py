import hashlib
import os
import threading
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class DatasetMetadata(BaseModel):
    """Metadata representation for a registered dataset."""

    dataset_id: str
    name: str
    source: str
    version: str
    download_location: str
    license: str
    citation: str
    checksum: Optional[str] = None
    row_count: int = 0
    feature_count: int = 0
    target_definition: str
    sensitive_attributes: List[str] = Field(default_factory=list)
    purpose: str
    status: str = "EXPERIMENTAL"  # "EXPERIMENTAL" | "APPROVED_FOR_RESEARCH" | "NOT_APPROVED"
    is_synthetic: bool = False


class DatasetRegistryManager:
    """
    Dataset Registry Manager tracking dataset licenses, versions, sources,
    citations, checksums, target definitions, and research status.
    """

    def __init__(self):
        self._registry: Dict[str, DatasetMetadata] = {}
        self._lock = threading.Lock()
        self._initialize_default_registry()

    def _initialize_default_registry(self):
        """Initializes default dataset registrations."""
        self.register_dataset(
            DatasetMetadata(
                dataset_id="uci_credit_default",
                name="UCI Default of Credit Card Clients",
                source="UCI Machine Learning Repository",
                version="v1.0.0",
                download_location="https://archive.ics.uci.edu/ml/datasets/default+of+credit+card+clients",
                license="CC BY 4.0",
                citation="Yeh, I. C., & Lien, C. H. (2009). The comparisons of data mining techniques for the predictive accuracy of probability of default of credit card clients. Expert Systems with Applications, 36(2), 2473-2480.",
                row_count=30000,
                feature_count=23,
                target_definition="default payment next month (1 = default, 0 = non-default)",
                sensitive_attributes=["SEX", "AGE", "MARRIAGE", "EDUCATION"],
                purpose="Experimental credit default risk prediction benchmark",
                status="APPROVED_FOR_RESEARCH",
                is_synthetic=False,
            )
        )

        self.register_dataset(
            DatasetMetadata(
                dataset_id="uci_german_credit",
                name="UCI Statlog German Credit",
                source="UCI Machine Learning Repository",
                version="v1.0.0",
                download_location="https://archive.ics.uci.edu/ml/datasets/statlog+(german+credit+data)",
                license="CC BY 4.0",
                citation="Hofmann, Hans. (1994). Statlog (German Credit Data). UCI Machine Learning Repository.",
                row_count=1000,
                feature_count=20,
                target_definition="credit risk (1 = Good Credit Risk, 2/0 = Bad Credit Risk)",
                sensitive_attributes=["personal_status_sex", "age", "foreign_worker"],
                purpose="Secondary credit risk classification benchmark",
                status="APPROVED_FOR_RESEARCH",
                is_synthetic=False,
            )
        )

        self.register_dataset(
            DatasetMetadata(
                dataset_id="uci_credit_approval",
                name="UCI Credit Approval",
                source="UCI Machine Learning Repository",
                version="v1.0.0",
                download_location="https://archive.ics.uci.edu/ml/datasets/credit+approval",
                license="CC BY 4.0",
                citation="Quinlan, J. R. (1987). Credit Approval Dataset. UCI Machine Learning Repository.",
                row_count=690,
                feature_count=15,
                target_definition="approval status (+ = approved, - = rejected)",
                sensitive_attributes=["A2_age", "A9_prior_default"],
                purpose="Secondary credit approval benchmark",
                status="APPROVED_FOR_RESEARCH",
                is_synthetic=False,
            )
        )

        self.register_dataset(
            DatasetMetadata(
                dataset_id="ibm_aml_synthetic",
                name="IBM Anti-Money Laundering Synthetic Transaction Data",
                source="IBM Research / Kaggle",
                version="v1.0.0",
                download_location="https://www.kaggle.com/datasets/ealtman2019/ibm-transactions-for-anti-money-laundering-aml",
                license="CDLA-Sharing-1.0",
                citation="Altman, E. (2023). Synthetic Financial Transactions Dataset for AML. IBM Research.",
                row_count=500000,
                feature_count=12,
                target_definition="Is Laundering (1 = illicit laundering transaction, 0 = legitimate)",
                sensitive_attributes=[],
                purpose="Synthetic transaction AML & fraud classification experimentation",
                status="APPROVED_FOR_RESEARCH",
                is_synthetic=True,
            )
        )

        self.register_dataset(
            DatasetMetadata(
                dataset_id="ibm_amlsim_graph",
                name="IBM AMLSim Synthetic Transaction Graph Data",
                source="IBM Research Github",
                version="v1.0.0",
                download_location="https://github.com/IBM/AMLSim",
                license="Apache-2.0",
                citation="Suzumura, T., et al. (2021). AMLSim: Anti-Money Laundering Simulator. IBM Research.",
                row_count=100000,
                feature_count=10,
                target_definition="is_sar (1 = Suspicious Activity Report, 0 = normal)",
                sensitive_attributes=[],
                purpose="Synthetic transaction graph structure experimentation",
                status="APPROVED_FOR_RESEARCH",
                is_synthetic=True,
            )
        )

    def register_dataset(self, metadata: DatasetMetadata):
        """Registers a dataset in the registry."""
        with self._lock:
            self._registry[metadata.dataset_id] = metadata

    def get_dataset(self, dataset_id: str) -> Optional[DatasetMetadata]:
        """Retrieves dataset metadata by ID."""
        with self._lock:
            return self._registry.get(dataset_id)

    def list_datasets(self) -> List[DatasetMetadata]:
        """Lists all registered datasets."""
        with self._lock:
            return list(self._registry.values())


dataset_registry_manager = DatasetRegistryManager()
