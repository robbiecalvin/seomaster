import unittest,os,json
from unittest.mock import patch
from integrations import ProviderClient
class IntegrationTests(unittest.TestCase):
    def test_denied(self):
        with self.assertRaises(PermissionError): ProviderClient().fetch('pagespeed',{})
    @patch.dict(os.environ,{'GOOGLE_ACCESS_TOKEN':'fake'})
    def test_search(self):
        def transport(req):
            self.assertIn('searchAnalytics/query',req.full_url); self.assertEqual(json.loads(req.data)['rowLimit'],1000); return {'rows':[]}
        self.assertEqual(ProviderClient(True,transport).fetch('search-console',{'site':'sc-domain:example.com','startDate':'2026-01-01','endDate':'2026-01-02','dimensions':['query']})['response'],{'rows':[]})
    def test_unknown(self):
        with self.assertRaises(ValueError): ProviderClient(True).fetch('unknown',{})
