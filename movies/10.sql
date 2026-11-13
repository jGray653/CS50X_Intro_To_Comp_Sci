-- 10. Names of all directors who have directed a movie that got a rating of at least 9.0
SELECT name FROM people
JOIN directors ON people.id = directors.person_id
JOIN ratings on directors.movie_id = ratings.movie_id
WHERE rating >= 9.0
GROUP BY name;
