# fifa-trade-bot

1. Включить браузер в постоянный режим.
2. Получить event от telegram.
3. Создать Task.
4. Запустить Task и контролировать его.
5. В случае успешного завершения, отправить уведомление в telegram.
6. Ждать следующий запрос.
7. Если произошел сбой, обработать его(отправкой сообщения в telegram). Повторить выполнение, если возможно.

# Сущности
1. Browser, должен только один раз включаться
2. Event, заявка от telegram 
3. Task, обработка event
4. Manager, обработка task