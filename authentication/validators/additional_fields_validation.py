from rest_framework.exceptions import ValidationError


def additional_fields_validation(self, data):
    # Ensure there are no extra fields in the request
    if hasattr(self, 'initial_data'):
        unknown_keys = set(self.initial_data.keys()) - set(self.fields.keys())
        if unknown_keys:
            raise ValidationError(f"Got unknown fields: {', '.join(unknown_keys)}")
    return data