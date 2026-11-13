-- 12. Titles of all of movies in which both Jennifer Lawrence and Bradley Cooper starred

SELECT title FROM movies
JOIN stars ON movies.id = stars.movie_id
JOIN people ON stars.person_id = people.id
WHERE name = 'Bradley Cooper' AND title IN (
    SELECT title FROM movies
    JOIN stars ON movies.id = stars.movie_id
    JOIN people ON stars.person_id = people.id
    WHERE name = 'Jennifer Lawrence'
);
