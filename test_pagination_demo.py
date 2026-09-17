import base64
import json
import unittest

from pagination_demo import decode_cursor, encode_cursor, paginate, read_all


def _encode_payload(payload: object) -> str:
    raw = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


class PaginationDemoTests(unittest.TestCase):
    def setUp(self) -> None:
        self.items = [f"row-{i:04d}" for i in range(503)]

    def test_cursor_round_trip(self) -> None:
        self.assertEqual(decode_cursor(encode_cursor(137)), 137)
        self.assertEqual(decode_cursor(None), 0)
        self.assertEqual(decode_cursor(""), 0)

    def test_pages_reconstruct_all_rows_without_loss(self) -> None:
        first = paginate(self.items, limit=100)
        second = paginate(self.items, cursor=first.next_cursor, limit=100)

        self.assertEqual(len(first.items), 100)
        self.assertTrue(first.has_more)
        self.assertEqual(second.items[0], "row-0100")
        self.assertEqual(first.total, 503)
        self.assertEqual(read_all(self.items, limit=100), self.items)

    def test_limit_is_bounded(self) -> None:
        for invalid_limit in (0, 201):
            with self.subTest(limit=invalid_limit):
                with self.assertRaisesRegex(ValueError, "limit must be between 1 and 200"):
                    paginate(self.items, limit=invalid_limit)

    def test_malformed_cursor_is_rejected_consistently(self) -> None:
        malformed = (
            "not-base64!",
            _encode_payload([1]),
            _encode_payload({"offset": -1}),
            _encode_payload({"offset": True}),
            _encode_payload({"offset": "10"}),
            "A" * 257,
            "游标",
        )
        for cursor in malformed:
            with self.subTest(cursor=cursor):
                with self.assertRaisesRegex(ValueError, "invalid cursor"):
                    decode_cursor(cursor)


if __name__ == "__main__":
    unittest.main()
