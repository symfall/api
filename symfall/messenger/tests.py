from rest_framework.test import APITestCase


class HealthCheckViewTest(APITestCase):
    def test_health_check(self):
        """
        Method for viewing health check in json format
        """
        response = self.client.get('/health_check/', data={'format': 'json'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual({
            'Cache backend: default': 'working',
            'DatabaseBackend': 'working',
            'DiskUsage': 'working',
            'MemoryUsage': 'working',
            'MigrationsHealthCheck': 'working'},
            response.json()
        )
