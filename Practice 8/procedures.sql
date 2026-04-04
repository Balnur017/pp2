-- procedures.sql
-- Процедуры для PhoneBook

CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM contacts WHERE name = p_name) THEN
        UPDATE contacts SET phone = p_phone WHERE name = p_name;
    ELSE
        INSERT INTO contacts(name, phone) VALUES(p_name, p_phone);
    END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE bulk_insert_contacts(
    p_names TEXT[], 
    p_phones TEXT[],
    OUT incorrect_data TEXT
)
LANGUAGE plpgsql AS $$
DECLARE
    i INT;
BEGIN
    incorrect_data := '';
    
    FOR i IN 1..array_length(p_names, 1) LOOP
        IF p_phones[i] !~ '^\+?\d{10,15}$' THEN
            incorrect_data := incorrect_data || 
                format('Неверный телефон у %s: %s\n', p_names[i], p_phones[i]);
            CONTINUE;
        END IF;

        CALL upsert_contact(p_names[i], p_phones[i]);
    END LOOP;
END;
$$;

CREATE OR REPLACE PROCEDURE delete_contact(p_name VARCHAR DEFAULT NULL, p_phone VARCHAR DEFAULT NULL)
LANGUAGE plpgsql AS $$
BEGIN
    IF p_name IS NOT NULL THEN
        DELETE FROM contacts WHERE name = p_name;
    ELSIF p_phone IS NOT NULL THEN
        DELETE FROM contacts WHERE phone = p_phone;
    ELSE
        RAISE EXCEPTION 'Укажите либо имя, либо телефон!';
    END IF;
END;
$$;