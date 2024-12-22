from services.service_models.feature import Feature


def create_feature(owner, name, description, cost):
    return Feature.objects.create(owner_id=owner, name=name, description=description, cost=cost)