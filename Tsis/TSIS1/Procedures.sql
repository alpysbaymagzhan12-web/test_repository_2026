-- ============================================================
-- PhoneBook Stored Procedures / Functions (TSIS 1)
-- NOTE: Procedures from Practice 8 are NOT duplicated here.
-- ============================================================


-- ------------------------------------------------------------
-- 3.4.1  add_phone
--   Adds a new phone number to an existing contact.
-- ------------------------------------------------------------
CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone        VARCHAR,
    p_type         VARCHAR   -- 'home' | 'work' | 'mobile'
)
LANGUAGE plpgsql AS $$
DECLARE
    v_contact_id INTEGER;
BEGIN
    -- Resolve contact
    SELECT id INTO v_contact_id
    FROM   contacts
    WHERE  username = p_contact_name;

    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact "%" not found.', p_contact_name;
    END IF;

    -- Validate phone type
    IF p_type NOT IN ('home', 'work', 'mobile') THEN
        RAISE EXCEPTION 'Invalid phone type "%". Must be home, work, or mobile.', p_type;
    END IF;

    -- Insert new phone
    INSERT INTO phones (contact_id, phone, type)
    VALUES (v_contact_id, p_phone, p_type);

    RAISE NOTICE 'Phone % (%) added to contact %.', p_phone, p_type, p_contact_name;
END;
$$;


-- ------------------------------------------------------------
-- 3.4.2  move_to_group
--   Moves a contact to a different group.
--   Creates the group automatically if it does not exist.
-- ------------------------------------------------------------
CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name   VARCHAR
)
LANGUAGE plpgsql AS $$
DECLARE
    v_contact_id INTEGER;
    v_group_id   INTEGER;
BEGIN
    -- Resolve contact
    SELECT id INTO v_contact_id
    FROM   contacts
    WHERE  username = p_contact_name;

    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact "%" not found.', p_contact_name;
    END IF;

    -- Upsert group (create if missing)
    INSERT INTO groups (name)
    VALUES (p_group_name)
    ON CONFLICT (name) DO NOTHING;

    SELECT id INTO v_group_id
    FROM   groups
    WHERE  name = p_group_name;

    -- Update contact
    UPDATE contacts
    SET    group_id = v_group_id
    WHERE  id = v_contact_id;

    RAISE NOTICE 'Contact "%" moved to group "%".', p_contact_name, p_group_name;
END;
$$;


-- ------------------------------------------------------------
-- 3.4.3  search_contacts(p_query)
--   Extended pattern search: matches username, email, AND
--   any phone number stored in the phones table.
--   Returns a set of contacts (with their primary phone).
-- ------------------------------------------------------------
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE (
    username  VARCHAR,
    email     VARCHAR,
    birthday  DATE,
    grp_name  VARCHAR,
    phone     VARCHAR,
    ph_type   VARCHAR
)
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT ON (c.id, ph.id)
           c.username,
           c.email,
           c.birthday,
           g.name   AS grp_name,
           ph.phone,
           ph.type  AS ph_type
    FROM   contacts c
    LEFT   JOIN groups g  ON g.id  = c.group_id
    LEFT   JOIN phones ph ON ph.contact_id = c.id
    WHERE  c.username ILIKE '%' || p_query || '%'
       OR  c.email    ILIKE '%' || p_query || '%'
       OR  ph.phone   ILIKE '%' || p_query || '%'
    ORDER  BY c.id, ph.id;
END;
$$;