"""Regression tests for malformed inputs at the research-data boundary."""

import copy
import unittest

from career_methods import validate_inputs


class InputValidationTests(unittest.TestCase):
    def setUp(self):
        self.profiles = [
            {
                "student_id": "S",
                "field": "cs",
                "skills": ["python"],
                "preferred_type": "internship",
                "preferred_modes": ["remote"],
            }
        ]
        self.opportunities = [
            {
                "opportunity_id": "O",
                "title": "Role",
                "required_skills": ["python"],
                "accepted_fields": ["cs"],
                "type": "internship",
                "mode": "remote",
            }
        ]
        self.labels = [
            {
                "student_id": "S",
                "opportunity_id": "O",
                "grade": 2,
                "rationale": "Direct match",
            }
        ]

    def validate(self):
        return validate_inputs(self.profiles, self.opportunities, self.labels)

    def test_valid_inputs_keep_existing_check_names(self):
        checks = self.validate()
        self.assertEqual(len(checks), 8)
        self.assertTrue(all(checks.values()))
        self.assertIn("complete_pair_grid", checks)

    def test_empty_collections_are_rejected(self):
        for index, name in enumerate(["profiles", "opportunities", "labels"]):
            inputs = [self.profiles, self.opportunities, self.labels]
            inputs[index] = []
            with self.subTest(collection=name), self.assertRaisesRegex(
                ValueError, name + ".*nonempty list"
            ):
                validate_inputs(*inputs)

    def test_non_list_collections_are_rejected(self):
        for index in range(3):
            inputs = [self.profiles, self.opportunities, self.labels]
            inputs[index] = "invalid"
            with self.subTest(collection=index), self.assertRaisesRegex(
                ValueError, "list of objects"
            ):
                validate_inputs(*inputs)

    def test_non_object_rows_are_rejected(self):
        for index in range(3):
            inputs = [self.profiles, self.opportunities, self.labels]
            inputs[index] = [None]
            with self.subTest(collection=index), self.assertRaisesRegex(
                ValueError, "must be an object"
            ):
                validate_inputs(*inputs)

    def test_list_fields_reject_strings(self):
        for records, field in [
            (self.profiles, "skills"),
            (self.profiles, "preferred_modes"),
            (self.opportunities, "required_skills"),
            (self.opportunities, "accepted_fields"),
        ]:
            original = records[0][field]
            records[0][field] = "remote"
            with self.subTest(field=field), self.assertRaisesRegex(
                ValueError, field + ".*list"
            ):
                self.validate()
            records[0][field] = original

    def test_list_fields_reject_blank_or_non_string_members(self):
        for records, field in [
            (self.profiles, "skills"),
            (self.profiles, "preferred_modes"),
            (self.opportunities, "required_skills"),
            (self.opportunities, "accepted_fields"),
        ]:
            original = records[0][field]
            for member in [" ", 3, None]:
                records[0][field] = [member]
                with self.subTest(field=field, member=member), self.assertRaisesRegex(
                    ValueError, field
                ):
                    self.validate()
            records[0][field] = original

    def test_required_lists_cannot_be_empty(self):
        for records, field in [
            (self.profiles, "preferred_modes"),
            (self.opportunities, "required_skills"),
            (self.opportunities, "accepted_fields"),
        ]:
            original = records[0][field]
            records[0][field] = []
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, field):
                self.validate()
            records[0][field] = original

    def test_empty_student_skills_remain_valid(self):
        self.profiles[0]["skills"] = []
        self.assertTrue(all(self.validate().values()))

    def test_missing_fields_give_value_errors(self):
        for records, field in [
            (self.profiles, "student_id"),
            (self.opportunities, "required_skills"),
            (self.labels, "opportunity_id"),
        ]:
            original = records[0].pop(field)
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, field):
                self.validate()
            records[0][field] = original

    def test_scalar_fields_reject_blank_and_non_string_values(self):
        for records, field in [
            (self.profiles, "field"),
            (self.profiles, "preferred_type"),
            (self.opportunities, "mode"),
            (self.labels, "rationale"),
        ]:
            original = records[0][field]
            for value in [" ", None, 7]:
                records[0][field] = value
                with self.subTest(field=field, value=value), self.assertRaisesRegex(
                    ValueError, field
                ):
                    self.validate()
            records[0][field] = original

    def test_duplicate_identifiers_are_rejected(self):
        for records, expected in [
            (self.profiles, "unique_student_ids"),
            (self.opportunities, "unique_opportunity_ids"),
        ]:
            records.append(copy.deepcopy(records[0]))
            with self.subTest(check=expected), self.assertRaisesRegex(
                ValueError, expected
            ):
                self.validate()
            records.pop()

    def test_duplicate_pairs_are_rejected(self):
        self.labels.append(copy.deepcopy(self.labels[0]))
        with self.assertRaisesRegex(ValueError, "unique_labeled_pairs"):
            self.validate()

    def test_unknown_references_are_rejected(self):
        self.labels[0]["student_id"] = "UNKNOWN"
        with self.assertRaisesRegex(ValueError, "complete_pair_grid"):
            self.validate()

    def test_invalid_grades_are_rejected(self):
        for value in [True, "2", 3, None]:
            self.labels[0]["grade"] = value
            with self.subTest(grade=value), self.assertRaisesRegex(
                ValueError, "valid_relevance_grades"
            ):
                self.validate()


if __name__ == "__main__":
    unittest.main()
