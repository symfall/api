from django.urls import reverse


class GetWithoutTokenMixin:
    """
    Mixin to check Token auth in the getting flows
    """

    def test_get_file_with_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token 12345")
        response = self.client.get(
            reverse(
                self.url_name,
            )
        )
        self.assertEqual(response.status_code, 401)
        self.assertDictEqual(
            {"detail": "Invalid token."},
            response.json(),
        )

    def test_get_file_with_missing_token(self):
        response = self.client.get(
            reverse(
                self.url_name,
            ),
        )
        self.assertEqual(response.status_code, 401)
        self.assertDictEqual(
            {"detail": "Authentication credentials were not provided."},
            response.json(),
        )


class PostWithoutTokenMixin:
    """
    Mixin to check Token auth in the posting flows
    """

    def test_delete_file_with_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token 12345")
        response = self.client.post(
            reverse(
                self.url_name,
            )
        )
        self.assertEqual(response.status_code, 401)
        self.assertDictEqual(
            {"detail": "Invalid token."},
            response.json(),
        )

    def test_delete_file_with_missing_token(self):
        response = self.client.post(
            reverse(
                self.url_name,
            ),
        )
        self.assertEqual(response.status_code, 401)
        self.assertDictEqual(
            {"detail": "Authentication credentials were not provided."},
            response.json(),
        )


class PutWithoutTokenMixin:
    """
    Mixin to check Token auth in the putting flows
    """

    def test_put_file_with_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token 12345")
        response = self.client.put(
            reverse(
                self.url_name,
                kwargs={"pk": 1},
            )
        )
        self.assertEqual(response.status_code, 401)
        self.assertDictEqual(
            {"detail": "Invalid token."},
            response.json(),
        )

    def test_put_file_with_missing_token(self):
        response = self.client.put(
            reverse(
                self.url_name,
                kwargs={"pk": 1},
            ),
        )
        self.assertEqual(response.status_code, 401)
        self.assertDictEqual(
            {"detail": "Authentication credentials were not provided."},
            response.json(),
        )


class DeleteWithoutTokenMixin:
    """
    Mixin to check Token auth in the deleting flows
    """

    def test_delete_file_with_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token 12345")
        response = self.client.delete(
            reverse(
                self.url_name,
                kwargs={"pk": 1},
            )
        )
        self.assertEqual(response.status_code, 401)
        self.assertDictEqual(
            {"detail": "Invalid token."},
            response.json(),
        )

    def test_delete_file_with_missing_token(self):
        response = self.client.delete(
            reverse(
                self.url_name,
                kwargs={"pk": 1},
            ),
        )
        self.assertEqual(response.status_code, 401)
        self.assertDictEqual(
            {"detail": "Authentication credentials were not provided."},
            response.json(),
        )
