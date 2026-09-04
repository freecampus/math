"""Validation for external curriculum resources and their reuse terms."""

from __future__ import annotations

from collections import Counter
from collections.abc import Mapping
from datetime import date
from pathlib import Path
from typing import Any, cast
from urllib.parse import urlparse

from fcmath.validation.curriculum import ValidationIssue, load_structured_data

_RESOURCE_TYPES = {
    "course",
    "examination",
    "practice-bank",
    "solutions",
    "specification",
}
_LICENSE_STATUSES = {"open", "not-confirmed"}
_USE_POLICIES = {
    "adapt-with-attribution",
    "link-only",
    "separate-license-review",
}
_LINK_STATUSES = {"verified", "unchecked", "unavailable"}


def validate_external_resources(
    registry_path: str | Path,
    coverage_path: str | Path,
) -> tuple[ValidationIssue, ...]:
    """Validate an external-resource registry against known course chapters.

    A resource with no confirmed open license is deliberately restricted to
    linking. This prevents public availability from being mistaken for
    permission to copy or adapt examination content.
    """

    registry = load_structured_data(registry_path)
    coverage = load_structured_data(coverage_path)
    issues: list[ValidationIssue] = []

    if registry.get("schema_version") != 1:
        issues.append(ValidationIssue("resources", "schema_version must equal 1"))
    if registry.get("course_id") != coverage.get("course_id"):
        issues.append(
            ValidationIssue("resources", "course_id disagrees with coverage matrix")
        )

    chapter_ids = {
        str(chapter.get("id"))
        for unit in coverage.get("units", [])
        if isinstance(unit, Mapping)
        for chapter in unit.get("chapters", [])
        if isinstance(chapter, Mapping)
    }
    raw_resources = registry.get("resources")
    if not isinstance(raw_resources, list) or not raw_resources:
        issues.append(ValidationIssue("resources", "resources must be non-empty"))
        return tuple(sorted(issues))

    resources: list[dict[str, Any]] = []
    for index, raw_resource in enumerate(raw_resources):
        if not isinstance(raw_resource, dict):
            issues.append(
                ValidationIssue(f"resources[{index}]", "resource must be a mapping")
            )
            continue
        resources.append(cast(dict[str, Any], raw_resource))

    ids = [str(resource.get("id", "")) for resource in resources]
    for resource_id, count in Counter(ids).items():
        if not resource_id:
            issues.append(ValidationIssue("resources", "resource ID is required"))
        elif count > 1:
            issues.append(
                ValidationIssue("resources", f"duplicate resource ID {resource_id!r}")
            )

    for resource in resources:
        resource_id = str(resource.get("id", "<missing>"))
        location = f"resource:{resource_id}"
        for field in ("title", "owner", "notes"):
            if not isinstance(resource.get(field), str) or not resource[field].strip():
                issues.append(ValidationIssue(location, f"{field} is required"))

        url = resource.get("url")
        if not isinstance(url, str) or not _is_https_url(url):
            issues.append(ValidationIssue(location, "url must be an HTTPS URL"))
        if resource.get("resource_type") not in _RESOURCE_TYPES:
            issues.append(ValidationIssue(location, "invalid resource_type"))

        topics = resource.get("topic_tags")
        if (
            not isinstance(topics, list)
            or not topics
            or not all(isinstance(topic, str) and topic.strip() for topic in topics)
        ):
            issues.append(ValidationIssue(location, "topic_tags must be non-empty"))

        placements = resource.get("chapter_ids")
        if not isinstance(placements, list) or not all(
            isinstance(chapter_id, str) for chapter_id in placements
        ):
            issues.append(ValidationIssue(location, "chapter_ids must be a list"))
        else:
            for chapter_id in placements:
                if chapter_id not in chapter_ids:
                    issues.append(
                        ValidationIssue(
                            location, f"unknown chapter placement {chapter_id!r}"
                        )
                    )

        _validate_iso_date(resource.get("access_date"), location, "access_date", issues)
        _validate_link_check(resource.get("last_link_check"), location, issues)
        _validate_license(resource, location, issues)

    return tuple(sorted(issues))


def _is_https_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc)


def _validate_iso_date(
    value: object,
    location: str,
    field: str,
    issues: list[ValidationIssue],
) -> None:
    if not isinstance(value, str):
        issues.append(ValidationIssue(location, f"{field} must be an ISO date"))
        return
    try:
        date.fromisoformat(value)
    except ValueError:
        issues.append(ValidationIssue(location, f"{field} must be an ISO date"))


def _validate_link_check(
    value: object,
    location: str,
    issues: list[ValidationIssue],
) -> None:
    if not isinstance(value, Mapping):
        issues.append(ValidationIssue(location, "last_link_check must be a mapping"))
        return
    _validate_iso_date(value.get("date"), location, "last_link_check.date", issues)
    if value.get("status") not in _LINK_STATUSES:
        issues.append(ValidationIssue(location, "invalid last_link_check.status"))


def _validate_license(
    resource: Mapping[str, Any],
    location: str,
    issues: list[ValidationIssue],
) -> None:
    license_data = resource.get("license")
    use_policy = resource.get("use_policy")
    if use_policy not in _USE_POLICIES:
        issues.append(ValidationIssue(location, "invalid use_policy"))
    if not isinstance(license_data, Mapping):
        issues.append(ValidationIssue(location, "license must be a mapping"))
        return

    status = license_data.get("status")
    if status not in _LICENSE_STATUSES:
        issues.append(ValidationIssue(location, "invalid license.status"))
        return
    if (
        not isinstance(license_data.get("notes"), str)
        or not license_data["notes"].strip()
    ):
        issues.append(ValidationIssue(location, "license.notes is required"))

    if status == "not-confirmed" and use_policy != "link-only":
        issues.append(
            ValidationIssue(
                location,
                "a resource without a confirmed open license must be link-only",
            )
        )
    if status == "open":
        for field in ("identifier", "url"):
            if (
                not isinstance(license_data.get(field), str)
                or not license_data[field].strip()
            ):
                issues.append(
                    ValidationIssue(location, f"open license requires {field}")
                )
        attribution = resource.get("attribution")
        if not isinstance(attribution, str) or not attribution.strip():
            issues.append(
                ValidationIssue(location, "open resource requires attribution")
            )
