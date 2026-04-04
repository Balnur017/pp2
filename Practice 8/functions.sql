-- functions.sql
-- Функции для PhoneBook

CREATE OR REPLACE FUNCTION get_contacts_by_pattern(p_pattern TEXT)
RETURNS TABLE(name TEXT, phone TEXT) AS $$
BEGIN
    RETURN QUERY 
    SELECT c.name, c.phone 
    FROM contacts c
    WHERE c.name ILIKE '%' || p_pattern || '%'
       OR c.phone ILIKE '%' || p_pattern || '%';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_contacts_paginated(p_limit INT DEFAULT 10, p_offset INT DEFAULT 0)
RETURNS TABLE(name TEXT, phone TEXT) AS $$
BEGIN
    RETURN QUERY 
    SELECT c.name, c.phone 
    FROM contacts c
    ORDER BY c.name
    LIMIT p_limit 
    OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;