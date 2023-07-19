import re


class ResponseInfo:
    
    def __init__(self, data, message, success, status):
        self.data = data
        self.message = message
        self.success = success
        self.status = status

    def default_errors_payload(self):
        collect_error_message = ""

        if isinstance(self.data, list):
            self.data = [i for i in self.data if bool(i)][0]
        # if isinstance(self.data, dict):
        #     self.data = [i for i in self.data if bool(i)]
        first_key = list(self.data.keys())[0]
        first_value = list(self.data.values())[0]
        if isinstance(first_value, dict):
            first_key = [*first_value][0]
            errors = [*first_value.values()][0][0]

        else:
            errors = ' '.join([str(v) for v in first_value])
        self.custom_code = 400
        if "custom_code" in self.data.keys():
            self.custom_code = int(self.data['custom_code'][0])
        # case insensitive replace of "this field"  string
        insensitive_this_field = re.compile(
            re.escape('This field'), re.IGNORECASE)

        self.message = insensitive_this_field.sub(first_key, errors)
        temp_default_errors = {
            "data": {},
            "message": self.message,
            "success": False,
            "status": self.status if self.status else self.custom_code
        }
        return temp_default_errors


    def custom_success_payload(self):
        # if error in payload
        if 'error' in self.data:
            self.message = self.data['error']
            self.data = {}

        temp_custom_success = {
            "data": self.data,
            "message": self.message,
            "success": self.success,
            "status": self.status
        }
        return temp_custom_success