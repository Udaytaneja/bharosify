import os
import json
import pytest
from ai.app.ml.datasets.doclaynet_metadata import (
    DOCLAYNET_GOVERNANCE_METADATA,
    DOCLAYNET_CLASS_MAPPING,
    AGENTTRUST_LAYOUT_CLASSES,
)
from ai.app.ml.datasets.doclaynet_converter import doclaynet_converter
from ai.app.ml.training.train_document_layout import document_layout_trainer


def test_1_dataset_registry_metadata():
    meta = DOCLAYNET_GOVERNANCE_METADATA
    assert meta.dataset_id == "ds_doclaynet_v1_1"
    assert meta.license == "CC-BY-4.0"
    assert meta.commercial_use_status == "COMMERCIAL_PERMITTED"
    assert meta.sample_count == 80863


def test_2_dataset_metadata_validation():
    assert len(DOCLAYNET_GOVERNANCE_METADATA.layout_classes) == 11
    assert "Table" in DOCLAYNET_GOVERNANCE_METADATA.layout_classes
    assert "Text" in DOCLAYNET_GOVERNANCE_METADATA.layout_classes


def test_3_class_mapping():
    assert DOCLAYNET_CLASS_MAPPING["Title"] == "TITLE"
    assert DOCLAYNET_CLASS_MAPPING["Table"] == "TABLE"
    assert DOCLAYNET_CLASS_MAPPING["Text"] == "TEXT_BLOCK"
    assert len(AGENTTRUST_LAYOUT_CLASSES) == 11


def test_4_yolo_annotation_conversion():
    # Test valid conversion from pixel bbox [100, 100, 200, 200] in 1000x1000 image
    yolo_box = doclaynet_converter.convert_coco_bbox_to_yolo([100, 100, 200, 200], 1000, 1000)
    assert yolo_box is not None
    assert yolo_box == [0.2, 0.2, 0.2, 0.2]


def test_5_invalid_bounding_boxes_validation():
    # Negative width
    assert doclaynet_converter.validate_bounding_box([0.5, 0.5, -0.1, 0.2]) is False
    # Out of bounds center
    assert doclaynet_converter.validate_bounding_box([1.5, 0.5, 0.2, 0.2]) is False


def test_6_duplicate_document_detection(tmp_path):
    f1 = tmp_path / "doc1.txt"
    f2 = tmp_path / "doc2.txt"
    f1.write_text("sample document content")
    f2.write_text("sample document content")

    h1 = doclaynet_converter.compute_file_hash(str(f1))
    h2 = doclaynet_converter.compute_file_hash(str(f2))
    assert h1 == h2  # Duplicate detected


def test_7_train_val_test_leakage_detection():
    doc_ids = [f"doc_{i}" for i in range(100)]
    splits = doclaynet_converter.deterministic_split_documents(doc_ids, seed=42)
    train_docs = {d for d, s in splits.items() if s == "train"}
    val_docs = {d for d, s in splits.items() if s == "val"}
    test_docs = {d for d, s in splits.items() if s == "test"}

    # Zero leakage check
    assert len(train_docs.intersection(val_docs)) == 0
    assert len(train_docs.intersection(test_docs)) == 0
    assert len(val_docs.intersection(test_docs)) == 0


def test_8_deterministic_split():
    doc_ids = [f"doc_{i}" for i in range(50)]
    split_a = doclaynet_converter.deterministic_split_documents(doc_ids, seed=42)
    split_b = doclaynet_converter.deterministic_split_documents(doc_ids, seed=42)
    assert split_a == split_b  # Deterministic repeatability


def test_9_dataset_yaml_generation(tmp_path):
    out_yaml = str(tmp_path / "dataset.yaml")
    gen_path = doclaynet_converter.generate_dataset_yaml(out_yaml)
    assert os.path.exists(gen_path)


def test_10_experiment_manifest_creation(tmp_path):
    out_dir = str(tmp_path / "exp")
    dataset_yaml = str(tmp_path / "dataset.yaml")
    doclaynet_converter.generate_dataset_yaml(dataset_yaml)

    res = document_layout_trainer.run_training(
        dataset_yaml=dataset_yaml,
        epochs=1,
        output_dir=out_dir
    )
    assert res["status"] == "COMPLETED"
    assert res["experiment_id"].startswith("exp_doclayout_")
    assert os.path.exists(res["experiment_manifest_path"])


def test_11_model_registry_integration(tmp_path):
    out_dir = str(tmp_path / "registry_exp")
    dataset_yaml = str(tmp_path / "dataset.yaml")
    doclaynet_converter.generate_dataset_yaml(dataset_yaml)

    res = document_layout_trainer.run_training(
        dataset_yaml=dataset_yaml,
        epochs=1,
        output_dir=out_dir
    )
    assert res["registered_model_id"] is not None


def test_12_missing_dataset_behavior():
    res = document_layout_trainer.run_training(dataset_yaml="non_existent_dataset.yaml")
    assert res["status"] == "DATASET_NOT_AVAILABLE"
    assert res["artifact_path"] is None
