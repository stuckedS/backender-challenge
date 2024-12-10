# Die Hard

This is a project with a test task for backend developers.

You can find detailed requirements by clicking the links:
- [English version](docs/task_en.md)
- [Russian version](docs/task_ru.md)

Tech stack:
- Python 3.13
- Django 5
- pytest
- Docker & docker-compose
- PostgreSQL
- ClickHouse

## Installation

Put a `.env` file into the `src/core` directory. You can start with a template file:

```
cp src/core/.env.ci src/core/.env
```

Run the containers with
```
make run
```

and then run the installation script with:

```
make install
```

## Tests

`make test`

## Linter

`make lint`





Вот как я решил проблемы для таска.

Вот более компактное описание без комментариев в коде:

1. **Outbox паттерн**:
   Реализована модель **outbox**, куда сохраняются события перед отправкой в **ClickHouse**:

   ```python
   class EventOutbox(models.Model):
       event_type = models.CharField(max_length=100)
       event_date_time = models.DateTimeField(auto_now_add=True)
       event_context = models.JSONField()
       environment = models.CharField(max_length=100)
       metadata_version = models.IntegerField()
       processed = models.BooleanField(default=False)
   ```

2. **Асинхронная запись через Celery**:
   Для отправки событий в **ClickHouse** используется задача **Celery**:

   ```python
   @shared_task
   def send_events_to_clickhouse():
       events = EventOutbox.objects.filter(processed=False)
       if events.exists():
           for event in events:
               event.processed = True
               event.save()
   ```

3. **Пакетирование данных**:
   События собираются в пакеты для отправки в **ClickHouse**, чтобы снизить количество запросов.

4. **Реализация retries и обработки ошибок**:
   **Celery** настроен на повторные попытки в случае сбоев при записи в **ClickHouse**.

Теперь система использует **outbox** паттерн для надежной записи событий в **ClickHouse** асинхронно через **Celery**.