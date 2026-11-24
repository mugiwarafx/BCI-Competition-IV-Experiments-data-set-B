"""Regression checks for the executable mathematics in the fuzzy notebook.

Run from the repository root with: python -m unittest discover -s tests -v
The notebook's function definitions and calculation cells are executed directly;
plots and the EEG dataset are not needed.
"""

import ast
import json
from pathlib import Path
import unittest
from unittest.mock import Mock

from scipy.integrate import quad


NOTEBOOK = Path(__file__).resolve().parents[1] / "fuzzy" / "experiment-fuzzy-1.ipynb"
RESULTS = ("potencia_defuzzificada", "potencia_defuzzificada_modificada")


class DefuzzificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
        cls.sources = [
            "".join(cell["source"])
            for cell in notebook["cells"]
            if cell["cell_type"] == "code"
        ]

    def calculate(self, result_name, activation=0.6, membership=None, integrator=quad):
        namespace = {"quad": integrator, "pertinenca_temp_actual": activation}
        for source in self.sources:
            functions = [
                node for node in ast.parse(source).body
                if isinstance(node, ast.FunctionDef)
            ]
            exec(compile(ast.Module(body=functions, type_ignores=[]), str(NOTEBOOK), "exec"), namespace)
        if membership is not None:
            namespace["potencia_mitjana"] = membership
        for source in self.sources:
            if any(
                isinstance(node, ast.Assign)
                and any(isinstance(target, ast.Name) and target.id == result_name for target in node.targets)
                for node in ast.parse(source).body
            ):
                exec(compile(source, str(NOTEBOOK), "exec"), namespace)
                return namespace[result_name], namespace
        self.fail("Missing notebook calculation: " + result_name)

    def test_symmetric_centroids_are_fifty_percent(self):
        for result_name in RESULTS:
            with self.subTest(result=result_name):
                value, _ = self.calculate(result_name)
                self.assertAlmostEqual(value, 50.0, places=6)

    def test_activation_scales_both_moment_and_area(self):
        for result_name in RESULTS:
            for activation in (0.2, 0.6, 1.0):
                with self.subTest(result=result_name, activation=activation):
                    value, _ = self.calculate(result_name, activation=activation)
                    self.assertAlmostEqual(value, 50.0, places=6)

    def test_integrals_match_analytic_triangle_and_clipped_triangle(self):
        for result_name, suffix, expected_area in (
            (RESULTS[0], "", 15.0),
            (RESULTS[1], "_modificada", 0.6 * 25.0 * (2 * 0.85 - 0.85 ** 2)),
        ):
            with self.subTest(result=result_name):
                _, namespace = self.calculate(result_name)
                self.assertAlmostEqual(namespace["integral_no_ponderada" + suffix], expected_area, places=6)
                self.assertAlmostEqual(namespace["integral_ponderada" + suffix], 50.0 * expected_area, places=4)

    def test_crop_can_move_an_asymmetric_centroid(self):
        # Triangle vertices (10, 0), (20, 1), (70, 0).
        def asymmetric_membership(y):
            return max(min((y - 10) / 10, (70 - y) / 50), 0)

        original, _ = self.calculate(RESULTS[0], membership=asymmetric_membership)
        clipped, _ = self.calculate(RESULTS[1], membership=asymmetric_membership)
        full_area = (70 - 10) / 2
        original_centroid = (10 + 20 + 70) / 3
        removed_area = full_area * (1 - 0.85) ** 2
        removed_centroid = (18.5 + 20 + 27.5) / 3
        clipped_centroid = (
            full_area * original_centroid - removed_area * removed_centroid
        ) / (full_area - removed_area)
        self.assertAlmostEqual(original, original_centroid, places=5)
        self.assertAlmostEqual(clipped, clipped_centroid, places=5)
        self.assertGreater(abs(clipped - original), 0.25)

    def test_zero_activation_has_no_centroid(self):
        for result_name in RESULTS:
            with self.subTest(result=result_name):
                with self.assertRaisesRegex(ValueError, "àrea nul·la"):
                    self.calculate(result_name, activation=0.0)

    def test_empty_output_has_no_centroid(self):
        for result_name in RESULTS:
            with self.subTest(result=result_name):
                with self.assertRaisesRegex(ValueError, "àrea nul·la"):
                    self.calculate(result_name, membership=lambda y: 0.0)

    def test_known_symmetry_shortcut_avoids_quadrature(self):
        integrator = Mock(side_effect=AssertionError("The symmetry shortcut must not integrate"))
        for activation in (0.2, 0.6, 1.0):
            with self.subTest(activation=activation):
                value, _ = self.calculate("potencia_per_simetria", activation=activation, integrator=integrator)
                self.assertEqual(value, 50.0)
        integrator.assert_not_called()
        with self.assertRaisesRegex(ValueError, "àrea nul·la"):
            self.calculate("potencia_per_simetria", activation=0.0, integrator=integrator)


if __name__ == "__main__":
    unittest.main()
