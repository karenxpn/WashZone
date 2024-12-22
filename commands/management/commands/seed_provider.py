from services.service_models.provider import Provider


def create_provider(category, owner, name, description, location):
    Provider.objects.create(category_id=category,
                            owner_id=owner,
                            name=name,
                            description=description,
                            location=location)