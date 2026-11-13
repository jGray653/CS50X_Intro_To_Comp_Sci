-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Already know the theft happened on July 28, 2025
-- And that it happened on Humphrey Street
-- Looking for: Thief, City Escaped To, Accomplice

-- Information:
-- Query 1: took place at 10:15am, three witness interviews all mention bakery
-- Query 2, Interview 1: Within 10 minutes of theft, drive away from bakery
-- Query 2, Interview 2: before 10:15, withdrew money from atm on Leggett Street
-- Query 2, Interview 3: called for less than 1 minute, take earliest flight out of fiftyville tomorrow, other person bought ticket
-- Query 3: Vanessa: 5p2bi95, Bruce: 94kl13x, Barry: 6p58ws2, Luca: 4328gd8, Sofia: g412cb7, Iman: l93jtiz, Diana: 322w7je, Kelsey: 0nthk55
-- Query 4: Narrowed down to Bruce, Diana, Iman and Luca
-- Query 5: Earliest flight on the 29th, is to LaGuardia
-- Query 6: Narrowed down to Bruce and Diana
-- Query 7: Bruce
-- Query 8: Robin
-- Query 9: NYC


-- Query 1: looking at the crime scene reports based on known criteria
SELECT description FROM crime_scene_reports
WHERE year = 2025 AND month = 7 AND day = 28 AND street = 'Humphrey Street';

-- Query 2: Look for the interview transcripts
SELECT transcript FROM interviews
WHERE year = 2025 AND month = 7 AND day = 28 AND transcript LIKE "%bakery%";

-- Query 3: Look for cars and their owners that drove away in that time frame
SELECT activity, people.license_plate, name FROM people
JOIN bakery_security_logs ON people.license_plate = bakery_security_logs.license_plate
WHERE year = 2025 AND month = 7 AND day = 28 AND hour = 10 AND minute >= 15 AND minute <= 25;

-- Query 4: Now I can see who withdrew money from the atm on leggett street before 10:15am
SELECT name, transaction_type FROM people
JOIN bank_accounts ON people.id = bank_accounts.person_id
JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number
WHERE year = 2025 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND name IN (
    SELECT name FROM people
    JOIN bakery_security_logs ON people.license_plate = bakery_security_logs.license_plate
    WHERE year = 2025 AND month = 7 AND day = 28 AND hour = 10 AND minute >= 15 AND minute <= 25
);

-- Query 5: Now I am gonna look at the list of outbound flights from fiftyville
SELECT full_name, hour, minute FROM airports
JOIN flights ON airports.id = flights.destination_airport_id
WHERE origin_airport_id = (
SELECT id FROM airports
WHERE full_name LIKE 'Fiftyville%') AND year = 2025 AND month = 7 AND day = 29
ORDER BY hour ASC, minute ASC;

-- Query 6: Now I can see who made a call for less than 60 seconds on the day of the theft
SELECT name FROM people
    JOIN phone_calls ON people.phone_number = phone_calls.caller
    WHERE duration <= 60 AND year = 2025 AND month = 7 AND day = 28 AND name IN (
    SELECT name FROM people
    JOIN bank_accounts ON people.id = bank_accounts.person_id
    JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number
    WHERE year = 2025 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND name IN (
         SELECT name FROM people
         JOIN bakery_security_logs ON people.license_plate = bakery_security_logs.license_plate
         WHERE year = 2025 AND month = 7 AND day = 28 AND hour = 10 AND minute >= 15 AND minute <= 25
));

-- Query 7: To find who the thief is, I need to see who was on the flight to laguardia
SELECt name FROM people
JOIN passengers ON people.passport_number = passengers.passport_number
WHERE flight_id = (
SELECT id FROM flights
WHERE destination_airport_id = (
SELECT id FROM airports WHERE full_name LIKE 'LaGuardia%') AND year = 2025 AND month = 7 AND day = 29 AND hour <=10) AND name = 'Bruce' OR name = 'Diana';

-- Query 8: Now to see who bruce was calling to see who the accomplice is
SELECT name FROM people
WHERE phone_number = (
    SELECT receiver FROM phone_calls
    WHERE caller = (
        SELECT phone_number FROM people WHERE name = 'Bruce'
        )AND year = 2025 AND month = 7 AND day = 28 AND duration < 60
);

-- Query 9: Then to find the city that the destination airport is
SELECT city FROM airports
WHERE full_name LIKE 'LaGuardia%';
