from services.service_models.service import Service


def create_service(provider, owner, name, description, price, duration):
    return Service.objects.create(
        provider=provider,
        owner_id=owner,
        name=name,
        description=description,
        base_price=price,
        duration_in_minutes=duration,
    )