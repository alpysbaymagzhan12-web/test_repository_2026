
CREATE OR REPLACE FUNCTION find_name_or_phone(p_text TEXT)
RETURNS TABLE (name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY 
    SELECT p.name, p.phone FROM phonebook_pr8 p
    WHERE p.name ILIKE '%' || p_text || '%' 
       OR p.phone ILIKE '%' || p_text || '%';
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_contact_pages(p_limit INT, p_offset INT)
RETURNS TABLE (name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY 
    SELECT p.name, p.phone FROM phonebook_pr8 p
    ORDER BY p.id 
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION insert_many_users(p_names TEXT[], p_phones TEXT[])
RETURNS TABLE (invalid_name TEXT, invalid_phone TEXT) AS $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1..array_length(p_names, 1) LOOP
        -- Валидация: нөмір тек цифрдан тұруы керек (мысалы 10-11 цифр)
        IF p_phones[i] ~ '^[0-9]+$' AND length(p_phones[i]) >= 10 THEN
            INSERT INTO phonebook_pr8 (name, phone)
            VALUES (p_names[i], p_phones[i])
            ON CONFLICT (name) DO UPDATE SET phone = EXCLUDED.phone;
        ELSE
            -- Қате деректерді нәтиже ретінде қайтару
            invalid_name := p_names[i];
            invalid_phone := p_phones[i];
            RETURN NEXT;
        END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;