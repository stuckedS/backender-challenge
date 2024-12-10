from models import Outbox

def add_to_outbox(event_type, payload):
    """
    Функция для добавления события в транзакционный Outbox.
    """
    Outbox.objects.create(event_type=event_type, payload=payload)
