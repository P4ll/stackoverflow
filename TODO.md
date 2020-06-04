# TODO
1. Подготовить датасет: время вопроса, 
Время: октябрь 2019

| Название колонки | Описание | Уже получили? |
| ---------------- | -------- | ------------- |
| id_post | ID поста | Y |
| id_user | ID пользователя | Y |
| post_score | рейтинг поста | Y |
| post_ans_count | кол-во ответов на вопрос | Y |
| post_tags | теги вопроса | Y |
| post_title | заголовок вопроса | Y |
| post_body | вопрос в html | Y |
| post_view_count | кол-во просмотров вопроса | Y |
| post_date | время создания вопроса | Y |
| post_is_closed | закрыт ли вопрос? | Y |
| user_rating | рейтинг пользователя, который задал вопрос | Y |
| user_reg_date | дата регистрации пользователя | Y |
| user_reached_people | кол-во затронутых людей пользователем | Y |
| user_questions_count | кол-во заданных пользователем вопросов | Y |
| user_ans_count | кол-во ответов пользователя | Y |
| type | хороший ли во вопрос: 0 - нет, 1 - да | Y |

2. Архитектура проекта
Реализовать класс DataMiner и Model

3. Реализовать класс каждой фичи

| Название фичи | Описание | Уже сделали? |
| ------------- | -------- | ------------ |
| Много отладочной (системной) информации | Дает ли пользователь системную и отладочную информацию, в каком кол-ве. | N |
| Кол-во ответов | Кол-во ответов пользователя | Y |
| Людей затронул | Примерное кол-во, когда пользователи видели полезное сообщение от этого пользователя | Y |
| Кол-во вопросов | Кол-во вопросов пользователя | Y |
| Уникальность задаваемого вопроса | Насколько много в системе похожих вопросов | N |
| Совпадение заголовка вопроса и темы текста | Совпадает ли то, что пользователь написал в заголовке с тем, что описано далее в вопросе | N |
| Правильность установки тегов | Говорит ли пользователь о том, что было установлено в тегах. | N |
| Рейтинг пользователя | “Объективная” оценка полезности пользователя для системы | Y |

4. BD для антиплагиата

```sql
CREATE DATABASE `mydatabase` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
```

```sql
CREATE TABLE `documents` (
  `id` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `created_date` datetime DEFAULT NULL,
  `updated_date` datetime DEFAULT NULL,
  `is_deleted` int DEFAULT NULL,
  `content` longtext COLLATE utf8_unicode_ci,
  `title` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `description` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `author` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `documentscol` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
```