from typing import Dict, List, Optional
from pydantic import BaseModel


class DatasetGovernanceMetadata(BaseModel):
    dataset_id: str
    name: str
    source: str
    version: str
    license: str
    license_verified: bool
    commercial_use_status: str
    data_type: str
    real_or_synthetic: str
    sample_count: int
    split_counts: Dict[str, int]
    layout_classes: List[str]


DOCLAYNET_GOVERNANCE_METADATA = DatasetGovernanceMetadata(
    dataset_id="ds_doclaynet_v1_1",
    name="DocLayNet Document Layout Dataset",
    source="IBM Research / HuggingFace Datasets (https://huggingface.co/datasets/ibm/doclaynet)",
    version="1.1.0",
    license="CC-BY-4.0",
    license_verified=True,
    commercial_use_status="COMMERCIAL_PERMITTED",
    data_type="image_layout_bbox",
    real_or_synthetic="real",
    sample_count=80863,
    split_counts={
        "train": 69372,
        "val": 6489,
        "test": 4999
    },
    layout_classes=[
        "Caption", "Footnote", "Formula", "List-item", "Page-footer",
        "Page-header", "Picture", "Section-header", "Table", "Text", "Title"
    ]
)

# Explicit DocLayNet class mapping to AgentTrust Layout Classes
DOCLAYNET_CLASS_MAPPING: Dict[str, str] = {
    "Caption": "CAPTION",
    "Footnote": "FOOTNOTE",
    "Formula": "FORMULA",
    "List-item": "LIST_ITEM",
    "Page-footer": "PAGE_FOOTER",
    "Page-header": "PAGE_HEADER",
    "Picture": "FIGURE",
    "Section-header": "SECTION_HEADER",
    "Table": "TABLE",
    "Text": "TEXT_BLOCK",
    "Title": "TITLE",
}

# Index mapping for YOLO class IDs (0-10)
AGENTTRUST_LAYOUT_CLASSES: List[str] = [
    "CAPTION",
    "FOOTNOTE",
    "FORMULA",
    "LIST_ITEM",
    "PAGE_FOOTER",
    "PAGE_HEADER",
    "FIGURE",
    "SECTION_HEADER",
    "TABLE",
    "TEXT_BLOCK",
    "TITLE"
]

# Separate Financial Semantic Field Classes (NOT provided directly by DocLayNet)
AGENTTRUST_FINANCIAL_SEMANTIC_CLASSES: List[str] = [
    "DOCUMENT_HEADER",
    "DOCUMENT_TITLE",
    "ACCOUNT_NUMBER",
    "IFSC",
    "DATE",
    "AMOUNT",
    "BANK_NAME",
    "CUSTOMER_NAME",
    "SALARY",
    "EMPLOYER",
    "TRANSACTION_TABLE",
    "SIGNATURE",
    "STAMP",
    "TOTAL",
    "FOOTER"
]
