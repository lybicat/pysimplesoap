import os
from .base import BaseTestcase
from pysimplesoap.wsdl import parse
from pysimplesoap.server import SoapDispatcher


class TestDispatcher(BaseTestcase):
    @classmethod
    def setUpClass(cls):
        _, _, _, _, services = parse(os.path.abspath('tst/data/ne3s.wsdl'))
        service_name = 'NE3SOperationNotificationService'
        service = services[service_name]
        cls.response = {
                'managerRegistrationId': 'mgr',
                'managerRegistrationKey': 'ODYzNTQ0NTg0'}
        def handle_operation(**kwargs):
            return cls.response

        cls.dispatcher = SoapDispatcher(
                name='ut',
                location='http://localhost:54321/services/NE3SOperationNotificationService',
                action='http://www.nokiasiemens.com/ne3s/1.0/',
                namespace='http://www.nokiasiemens.com/ne3s/1.0/',
                # namespaces={'ns': 'http://www.nokiasiemens.com/ne3s/1.0/',
                    # 'soapenv': 'http://schemas.xmlsoap.org/soap/envelope/'},
                documentation='NetAct simulator SOAP service',
                prefix='ns',
                debug=True)
        for port_name, port in service['ports'].iteritems():
            for operation_name, operation in port['operations'].iteritems():
                cls.dispatcher.register_function(operation_name, handle_operation,
                        returns=operation['output'].values()[0],
                        args=operation['input'].values()[0])

    def test_dispatch(self):
        fault={}
        self.response = {
                'managerRegistrationId': 'mgr',
                'managerRegistrationKey': 'ODYzNTQ0NTg0'}
        with open('tst/data/reportOperationStatus_req.txt', 'rb') as fp:
            request = fp.read()
        response = self.dispatcher.dispatch(request, fault=fault,
            headers={'content-type':'multipart/related; boundary="MIMEBoundary_a33628f952113627189ce7fb3be101170181698d5b86d135"; type="text/xml"; start="<0.933628f952113627189ce7fb3be101170181698d5b86d135@apache.org>"'})
        self.assertEqual(response, '''<?xml version="1.0" encoding="UTF-8"?><soapenv:Envelope xmlns:ns="http://www.nokiasiemens.com/ne3s/1.0/" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><soapenv:Body><ns:reportOperationStatusResponse><ns:managerRegistrationId>mgr</ns:managerRegistrationId><ns:managerRegistrationKey>ODYzNTQ0NTg0</ns:managerRegistrationKey></ns:reportOperationStatusResponse></soapenv:Body></soapenv:Envelope>''')

