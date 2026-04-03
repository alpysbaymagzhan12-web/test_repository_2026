
CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO phonebook_pr8 (name, phone)
    VALUES (p_name, p_phone)
    ON CONFLICT (name) DO UPDATE SET phone = EXCLUDED.phone;
END;
$$;


CREATE OR REPLACE PROCEDURE delete_contact(p_identifier VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM phonebook_pr8 
    WHERE name = p_identifier OR phone = p_identifier;
END;
$$;