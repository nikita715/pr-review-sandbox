# pr-review-sandbox

Песочница для проверки AI-ревью из
[pr-review-bot](https://github.com/nikita715/pr-review-bot).

Небольшой магазин на чистом Python: товары в SQLite, расчёт цены со скидкой
и налогом, создание заказов с резервированием остатков.

```
shop/
  models.py      — Product, OrderItem, Order
  pricing.py     — сумма, скидка, налог
  repository.py  — работа с SQLite
  orders.py      — OrderService.create_order
tests/           — unittest
```

## Запуск тестов

```sh
python3 -m unittest discover -v
```

## AI-ревью

`.github/workflows/ai-review.yml` запускает Claude Code и pr-agent на PR из форков,
которые не являются черновиками. Правила ревью — в `CLAUDE.md`.
