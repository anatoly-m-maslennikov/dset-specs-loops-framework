"""Verify three-axis DSET artifact routing."""

from __future__ import annotations

import unittest

from dset_toolchain.artifact_routing import (
    CONTENT_ROLES,
    GOVERNANCE_LOCI,
    REVISION_MODES,
    ArtifactRoute,
    parse_artifact_route,
    route_issues,
)


class ArtifactRoutingTests(unittest.TestCase):
    """Verify routing axes, names, and relational gates."""

    def internal(self) -> dict[str, object]:
        """Return one complete internal route candidate."""
        return {
            "revision_mode": "atomic",
            "content_role": "definition",
            "governance_locus": "internal",
            "scope_path": ["layer:gov"],
        }

    def test_content_roles_follow_the_canonical_loop(self) -> None:
        self.assertEqual(
            CONTENT_ROLES,
            (
                "inquiry",
                "analysis",
                "definition",
                "method",
                "implementation",
                "observation",
            ),
        )

    def test_internal_route_has_one_deterministic_name(self) -> None:
        route = parse_artifact_route(self.internal())

        self.assertEqual(route.key, "atomic.definition.internal")
        self.assertEqual(route.name, "Internal Atomic Definition")
        self.assertEqual(
            route.as_dict()["scope_path"],
            ["layer:gov"],
        )

        external = self.internal()
        external["governance_locus"] = "external"
        self.assertEqual(
            parse_artifact_route(external).name,
            "External Atomic Definition",
        )

    def test_each_internal_and_external_route_has_one_unique_name(self) -> None:
        names: set[str] = set()
        for revision_mode in REVISION_MODES:
            for content_role in CONTENT_ROLES:
                for governance_locus in GOVERNANCE_LOCI:
                    candidate = {
                        "revision_mode": revision_mode,
                        "content_role": content_role,
                        "governance_locus": governance_locus,
                        "scope_path": [],
                    }
                    if governance_locus == "relation":
                        candidate.update(
                            {
                                "relation_kind": "connects",
                                "endpoints": [
                                    {
                                        "role": "source",
                                        "identity": "A",
                                        "origin": "internal",
                                    },
                                    {
                                        "role": "target",
                                        "identity": "B",
                                        "origin": "external",
                                    },
                                ],
                            }
                        )
                    route = parse_artifact_route(candidate)
                    self.assertNotIn(route.name, names)
                    names.add(route.name)
                    self.assertTrue(
                        route.name.startswith(governance_locus.title())
                    )
        self.assertEqual(len(names), 54)

    def test_relational_route_requires_kind_and_endpoints(self) -> None:
        candidate = self.internal()
        candidate["governance_locus"] = "relation"

        self.assertIn(
            "relational routes require a snake_case relation_kind",
            route_issues(candidate),
        )

        candidate.update(
            {
                "relation_kind": "contract_between",
                "endpoints": [
                    {
                        "role": "consumer",
                        "identity": "PROJECT-A",
                        "origin": "internal",
                    },
                    {
                        "role": "provider",
                        "identity": "SYSTEM-B",
                        "origin": "external",
                    },
                ],
            }
        )
        route = parse_artifact_route(candidate)

        self.assertIsInstance(route, ArtifactRoute)
        self.assertEqual(route.name, "Relation Atomic Definition")
        self.assertEqual(len(route.endpoints), 2)

    def test_type_and_subtype_are_rejected_as_routing_fields(self) -> None:
        candidate = self.internal()
        candidate["type"] = "decision"

        self.assertIn(
            "Type/subtype metadata is not part of routing: type",
            route_issues(candidate),
        )

    def test_scope_path_is_extensible_but_structured(self) -> None:
        candidate = self.internal()
        candidate["scope_path"] = [
            "feature_group:schedulers",
            "feature:catchup",
            "layer:tool",
            "component:worker",
        ]
        self.assertEqual(route_issues(candidate), [])

        candidate["scope_path"] = ["gov"]
        self.assertIn(
            "scope_path must contain only kind:id segments",
            route_issues(candidate),
        )

        candidate["scope_path"] = ["project:dset", "layer:gov"]
        self.assertIn(
            "scope_path must not repeat the ambient project identity",
            route_issues(candidate),
        )

        candidate["scope_path"] = []
        self.assertEqual(route_issues(candidate), [])


if __name__ == "__main__":
    unittest.main()
