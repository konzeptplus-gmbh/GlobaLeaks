# -*- coding: utf-8 -*-
from globaleaks.handlers.base import BaseHandler
from globaleaks.rest import errors, requests


class OperationHandler(BaseHandler):
    """
    Base handler for implementing handlers for executing platform configuration
    """
    require_confirmation = [
        'enable_encryption',
        'disable_2fa',
        'toggle_escrow',
        'toggle_user_escrow',
        'reset_submissions'
    ]

    def operation_descriptors(self):
        raise NotImplementedError

    def put(self, *args, **kwargs):
        request = self.validate_request(self.request.content.read(), requests.OpsDesc)

        if request['operation'] in self.require_confirmation:
            self.check_confirmation()

        func = self.operation_descriptors().get(request['operation'], None)
        if func is None:
            raise errors.InputValidationError('Invalid command')

        return func(self, request['args'], *args, **kwargs)
