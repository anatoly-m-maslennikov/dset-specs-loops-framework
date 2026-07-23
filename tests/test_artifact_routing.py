"""Verify type-free DSET artifact routing."""

from __future__ import annotations

import unittest

from dset_toolchain.artifact_routing import (
    CONTENT_ROLES,
    GOVERNANCE_ORIGINS,
    RELATION_SHAPES,
    REVISION_MODES,
    ArtifactRoute,
    parse_artifact_route,
    route_issues,
)


class ArtifactRoutingTests(unittest.TestCase):
    """Verify routing axes, names, and relational gates."""

    def standalone(self) -> dict[str, object]:
        """Return one complete standalone route candidate."""
        return {
            "revision_mode": "atomic",
            "content_role": "definition",
            "governance_origin": "internal",
            "relation_shape": "standalone",
            "scope_path": ["project:dset", "layer:gov"],
        }

    def test_content_roles_follow_the_canonical_loop(self) -> None:
        self.assertEqual(
            CONTENT_ROLES,
            (
                "inquiry",
                "definition",
                "rationale",
                "method",
                "implementation",
                "observation",
            ),
        )

    def test_standalone_route_has_one_deterministic_name(self) -> None:
        route = parse_artifact_route(self.standalone())

        self.assertEqual(route.key, "atomic.definition.internal.standalone")
        self.assertEqual(route.name, "Internal Atomic Definition Artifact")
        self.assertEqual(
            route.as_dict()["scope_path"],
            ["project:dset", "layer:gov"],
        )

        external = self.standalone()
        external["governance_origin"] = "external"
        self.assertEqual(
            parse_artifact_route(external).name,
            "External Atomic Definition Artifact",
        )

    def test_each_internal_and_external_route_has_one_unique_name(self) -> None:
        names: set[str] = set()
        for revision_mode in REVISION_MODES:
            for content_role in CONTENT_ROLES:
                for governance_origin in GOVERNANCE_ORIGINS:
                    for relation_shape in RELATION_SHAPES:
                        candidate = {
                            "revision_mode": revision_mode,
                            "content_role": content_role,
                            "governance_origin": governance_origin,
                            "relation_shape": relation_shape,
                            "scope_path": ["project:dset"],
                        }
                        if relation_shape == "relational":
                            candidate.update(
                                {
                                    "relation_kind": "connects",
                                    "endpoints": [
                                        {
                                            "role": "source",
                                            "target": "A",
                                            "origin": "internal",
                                        },
                                        {
                                            "role": "target",
                                            "target": "B",
                                            "origin": "external",
                                        },
                                    ],
                                }
                            )
                        route = parse_artifact_route(candidate)
                        self.assertNotIn(route.name, names)
                        names.add(route.name)
                        self.assertTrue(
                            route.name.startswith(governance_origin.title())
                        )
        self.assertEqual(len(names), 72)

    def test_relational_route_requires_kind_and_endpoints(self) -> None:
        candidate = self.standalone()
        candidate["relation_shape"] = "relational"

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
                        "target": "PROJECT-A",
                        "origin": "internal",
                    },
                    {
                        "role": "provider",
                        "target": "SYSTEM-B",
                        "origin": "external",
                    },
                ],
            }
        )
        route = parse_artifact_route(candidate)

        self.assertIsInstance(route, ArtifactRoute)
        self.assertEqual(route.name, "Internal Atomic Definition Relation")
        self.assertEqual(len(route.endpoints), 2)

    def test_type_and_subtype_are_rejected_as_routing_fields(self) -> None:
        candidate = self.standalone()
        candidate["type"] = "decision"

        self.assertIn("type and subtype are not routing fields", route_issues(candidate))

    def test_scope_path_is_extensible_but_structured(self) -> None:
        candidate = self.standalone()
        candidate["scope_path"] = [
            "project:dset",
            "feature_group:schedulers",
            "feature:catchup",
            "layer:tool",
            "component:worker",
        ]
        self.assertEqual(route_issues(candidate), [])

        candidate["scope_path"] = ["gov"]
        self.assertIn(
            "scope_path must be a non-empty list of kind:id segments",
            route_issues(candidate),
        )


if __name__ == "__main__":
    unittest.main()
