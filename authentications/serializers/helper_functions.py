def update_related_instance(instance, data, related_attr):
    related_instance = getattr(instance, related_attr)
    attributes = []
    for attr, value in data.items():
        attributes.append(attr)
        setattr(related_instance, attr, value)
    related_instance.save(update_fields=attributes)
