# Бот-чеклист для ежедневных задач
Бот в телеграмме, который может создавать списки дел пользователя и проводить некоторые манипуляции с ними.
# Подробное описание
Что должен уметь бот?
- добавлять дело (дата, когда буду делать; дедлайн; *категория (например учеба, домашние дела и тд)*; важность - от 1 до 4)
- отмечать дело как выполненное
- удалять дело
- редактировать дело (например дедлайн или еще что-то)
- может присылать разные напоминания (пользователь выберет время)? типа у вас на сегодня такие-то дела или не забудьте в 2 позвонить маме
- показывать дела на какой-то день, отрезок времени, етц (или все вбитые)
- можно было запросить сортить дела сначала по дедлайну потом по важности (или наоборот)
- на запросы отвечать типа “добавлено” или “это изменено на то”
- когда пользователь выполняет дело хвалить его и присылать милую картиночку
- *добавлять категории (если у какого-то дела она не указывается то он попадает в категорию “без категории” или типа того)*
- *строить табличку “срочные и важные, несрочные и важные и тд” (по всем не выполненным делам, срочные - 3 дня до дедлайна (или дать пользователю выбирать?), важные - важность 1-2)*
- *добавлять проекты (дедлайн к нему) и в проект добавлять дела которые надо сделать (для них все будет работать как для обычных дел, можно подписывать что они в такому-то проекту относятся)*  

** *Курсивом* выделены дополнительные опции, которые мы реализуем, если будет время.

# Критерий завершенного проекта
В телеграмме есть рабочий бот по имени *@mythings_to_do_bot*, который умеет добавлять, удалять, редактировать дела, отмечать выполненные, а также показывать их, как попросит пользователь (на определенную дату, определенной важности, и т.д.).
## Команда проекта
Хургес Алина Михайловна (201)  

Сухарева Мария Игоревна (201)  

Алексеева Анастасия Павловна (201)
# Таймлайн проекта
**22.03** - первый созвон  

**~до 31.03** - смотрим запись Олега про боты в телеграмме, читаем про библиотеки, делаем маленького простого бота  

**~31.03** - второй созвон

**10.04** - произошел второй созвон, Маша сделала простенького бота (все остальные тоже с этим попрактиковались, но у Маши получилось загрузить его на сервер)

**17.04** - представляем небольшую презентацию: о чем наш проект, что мы делаем
# Чего нам не хватает для реализации проекта
Наверное, пока что мы не знаем, как создавать ботов и работать с ними.

Upd. Вроде как разобрались с этим. Теперь нам немножко не хватает организованности, времени и сил :(
# Распределение обязанностей в команде
**Мария Сухарева**
- создание бота и загрузка его на сервер
- добавлять дело (дата, когда хотят сделать; дедлайн; важность - от 1 до 4)
- отмечать дела как выполненные
- удалять дела

**Алина Хургес**
- редактировать дела (например дедлайн, еще что-то)
- сортировка дел по разным параметрам (сначала по дедлайнам, потом - по важности, и наоборот)
- показывать дела на выбранный день / отрезок времени или все записанные невыполненные дела

**Анастасия Алексеева**
- редактирование readme файла
- присылать напоминания (пользователь выберет время), например, на сегодня есть такие дела или не забудьте в 2 часа дня что-нибудь сделать
- на разные запросы (удалить/добавить/изменить дело и т.д.) отвечать “добавлено”, “изменено” и т.д.
- когда пользователь отмечает дело выполненным, хвалить его и присылать милую картиночку
