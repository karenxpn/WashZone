from services.service_models.provider import Provider


def create_provider(category, owner, name, description, address, contact_number, location):
    return Provider.objects.create(category_id=category,
                            owner_id=owner,
                            name=name,
                            description=description,
                            address=address,
                            contact_number=contact_number,
                            location=location)