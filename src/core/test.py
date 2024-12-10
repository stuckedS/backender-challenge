import pytest
from django.core.management import call_command
from django.db import connection
from core.models import Outbox 
from core.tasks import my_celery_task 

@pytest.mark.django_db
def test_event_creation():
    """Тестируем создание события и его запись в базу данных"""
    event = Outbox.objects.create(
        event_type="user_signup",
        event_date_time="2024-12-10 00:00:00",
        environment="production",
        event_context={"user_id": 123, "username": "test_user"},
        metadata_version=1,
    )

    assert Outbox.objects.count() == 1
    assert event.event_type == "user_signup"
    assert event.environment == "production"


@pytest.mark.django_db
def test_clickhouse_insertion():
    """Тестируем вставку события в ClickHouse через Outbox или Celery"""
    call_command('process_events')  
    
    from clickhouse_driver import Client
    client = Client('clickhouse')
    result = client.execute('SELECT * FROM events_table WHERE event_type="user_signup"')

    assert len(result) > 0 

@pytest.mark.celery
def test_celery_task():
    """Тестируем задачу Celery для обработки событий"""
    result = my_celery_task.apply(args=["user_signup", {"user_id": 123, "username": "test_user"}])

    assert result.successful()
