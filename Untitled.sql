SELECT users.first_name, users.last_name, events.id as id, events.name as Headline, events.description as Description 
FROM users 
JOIN events 
ON users.id = events.host_id;

SELECT * FROM events
