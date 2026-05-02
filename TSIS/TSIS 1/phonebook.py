import csv
import json
from datetime import datetime
from connect import connect


VALID_SORTS = {
    "name": "name",
    "birthday": "birthday",
    "date": "id",
}


def parse_date(date_str):
    if not date_str:
        return None
    return datetime.strptime(date_str, "%Y-%m-%d").date()


def print_contacts(rows):
    if not rows:
        print("No contacts found.")
        return

    for row in rows:
        print("-" * 60)
        print(f"ID        : {row[0]}")
        print(f"Name      : {row[1]}")
        print(f"Phone     : {row[2] or '-'}")
        print(f"Email     : {row[3] or '-'}")
        print(f"Birthday  : {row[4] or '-'}")
        print(f"Group ID  : {row[5] or '-'}")
    print("-" * 60)


def add_contact_extended():
    name = input("Enter name: ").strip()
    phone = input("Enter phone: ").strip() or None
    email = input("Enter email: ").strip() or None
    birthday_input = input("Enter birthday (YYYY-MM-DD or empty): ").strip()
    group_id_input = input("Enter group_id: ").strip()

    try:
        birthday = parse_date(birthday_input) if birthday_input else None
        group_id = int(group_id_input) if group_id_input else None
    except ValueError:
        print("Invalid birthday or group_id.")
        return

    conn = connect()
    if not conn:
        return

    try:
        cur = conn.cursor()

        cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
        exists = cur.fetchone()

        if exists:
            action = input("Contact exists. Choose [skip/overwrite]: ").strip().lower()
            if action != "overwrite":
                print("Skipped.")
                return

            cur.execute(
                """
                UPDATE contacts
                SET phone = %s,
                    email = %s,
                    birthday = %s,
                    group_id = %s
                WHERE name = %s
                """,
                (phone, email, birthday, group_id, name),
            )
            print("Contact overwritten successfully.")

        else:
            cur.execute(
                """
                INSERT INTO contacts(name, phone, email, birthday, group_id)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (name, phone, email, birthday, group_id),
            )
            print("Contact added successfully.")

        conn.commit()

    except Exception as e:
        conn.rollback()
        print("Add contact error:", e)

    finally:
        cur.close()
        conn.close()


def search_all_fields():
    query = input("Enter search text: ").strip()

    conn = connect()
    if not conn:
        return

    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT id, name, phone, email, birthday, group_id
            FROM contacts
            WHERE name ILIKE %s
               OR phone ILIKE %s
               OR email ILIKE %s
               OR CAST(birthday AS TEXT) ILIKE %s
               OR CAST(group_id AS TEXT) ILIKE %s
            ORDER BY name
            """,
            (f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%"),
        )

        rows = cur.fetchall()
        print_contacts(rows)

    except Exception as e:
        print("Search error:", e)

    finally:
        cur.close()
        conn.close()


def search_by_email():
    query = input("Enter part of email: ").strip()

    conn = connect()
    if not conn:
        return

    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT id, name, phone, email, birthday, group_id
            FROM contacts
            WHERE COALESCE(email, '') ILIKE %s
            ORDER BY name
            """,
            (f"%{query}%",),
        )

        rows = cur.fetchall()
        print_contacts(rows)

    except Exception as e:
        print("Email search error:", e)

    finally:
        cur.close()
        conn.close()


def filter_by_group():
    group_id_input = input("Enter group_id: ").strip()

    try:
        group_id = int(group_id_input)
    except ValueError:
        print("group_id must be integer.")
        return

    conn = connect()
    if not conn:
        return

    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT id, name, phone, email, birthday, group_id
            FROM contacts
            WHERE group_id = %s
            ORDER BY name
            """,
            (group_id,),
        )

        rows = cur.fetchall()
        print_contacts(rows)

    except Exception as e:
        print("Filter error:", e)

    finally:
        cur.close()
        conn.close()


def sort_contacts():
    sort_key = input("Sort by [name/birthday/date]: ").strip().lower()

    if sort_key not in VALID_SORTS:
        print("Invalid sort option.")
        return

    order_by = VALID_SORTS[sort_key]

    conn = connect()
    if not conn:
        return

    try:
        cur = conn.cursor()
        cur.execute(
            f"""
            SELECT id, name, phone, email, birthday, group_id
            FROM contacts
            ORDER BY {order_by} NULLS LAST
            """
        )

        rows = cur.fetchall()
        print_contacts(rows)

    except Exception as e:
        print("Sort error:", e)

    finally:
        cur.close()
        conn.close()


def paginate_navigation():
    try:
        limit = int(input("Enter page size: ").strip())
    except ValueError:
        print("Limit must be integer.")
        return

    offset = 0

    conn = connect()
    if not conn:
        return

    try:
        cur = conn.cursor()

        while True:
            cur.execute(
                """
                SELECT id, name, phone, email, birthday, group_id
                FROM contacts
                ORDER BY name
                LIMIT %s OFFSET %s
                """,
                (limit, offset),
            )

            rows = cur.fetchall()

            print(f"\nPage offset = {offset}")
            print_contacts(rows)

            command = input("Command [next/prev/quit]: ").strip().lower()

            if command == "next":
                if rows:
                    offset += limit
                else:
                    print("No more pages.")

            elif command == "prev":
                offset = max(0, offset - limit)

            elif command == "quit":
                break

            else:
                print("Unknown command.")

    except Exception as e:
        print("Pagination error:", e)

    finally:
        cur.close()
        conn.close()


def export_to_json():
    filename = input("Enter JSON filename to export: ").strip() or "contacts_export.json"

    conn = connect()
    if not conn:
        return

    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT id, name, phone, email, birthday, group_id
            FROM contacts
            ORDER BY name
            """
        )

        contacts = cur.fetchall()
        result = []

        for contact in contacts:
            contact_id, name, phone, email, birthday, group_id = contact

            result.append(
                {
                    "id": contact_id,
                    "name": name,
                    "phone": phone,
                    "email": email,
                    "birthday": str(birthday) if birthday else None,
                    "group_id": group_id,
                }
            )

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4, ensure_ascii=False)

        print(f"Exported to {filename}")

    except Exception as e:
        print("Export error:", e)

    finally:
        cur.close()
        conn.close()


def import_from_json():
    filename = input("Enter JSON filename to import: ").strip()

    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

    except Exception as e:
        print("Cannot read JSON:", e)
        return

    conn = connect()
    if not conn:
        return

    try:
        cur = conn.cursor()

        for item in data:
            name = item.get("name")
            phone = item.get("phone")
            email = item.get("email")
            birthday = parse_date(item.get("birthday")) if item.get("birthday") else None
            group_id = item.get("group_id")

            cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
            exists = cur.fetchone()

            if exists:
                action = input(f"Duplicate contact '{name}'. Choose [skip/overwrite]: ").strip().lower()

                if action == "overwrite":
                    cur.execute(
                        """
                        UPDATE contacts
                        SET phone = %s,
                            email = %s,
                            birthday = %s,
                            group_id = %s
                        WHERE name = %s
                        """,
                        (phone, email, birthday, group_id, name),
                    )
                    print(f"Overwritten {name}")
                else:
                    print(f"Skipped {name}")

            else:
                cur.execute(
                    """
                    INSERT INTO contacts(name, phone, email, birthday, group_id)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (name, phone, email, birthday, group_id),
                )
                print(f"Imported {name}")

        conn.commit()
        print("JSON import finished.")

    except Exception as e:
        conn.rollback()
        print("Import error:", e)

    finally:
        cur.close()
        conn.close()


def import_from_csv():
    filename = input("Enter CSV filename: ").strip()

    try:
        with open(filename, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

    except Exception as e:
        print("Cannot read CSV:", e)
        return

    conn = connect()
    if not conn:
        return

    try:
        cur = conn.cursor()

        for row in rows:
            name = (row.get("name") or "").strip()
            phone = (row.get("phone") or "").strip() or None
            email = (row.get("email") or "").strip() or None
            birthday_input = (row.get("birthday") or "").strip()
            group_id_input = (row.get("group_id") or "").strip()

            if not name:
                continue

            birthday = parse_date(birthday_input) if birthday_input else None
            group_id = int(group_id_input) if group_id_input else None

            cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
            exists = cur.fetchone()

            if exists:
                action = input(f"Duplicate contact '{name}'. Choose [skip/overwrite]: ").strip().lower()

                if action == "overwrite":
                    cur.execute(
                        """
                        UPDATE contacts
                        SET phone = %s,
                            email = %s,
                            birthday = %s,
                            group_id = %s
                        WHERE name = %s
                        """,
                        (phone, email, birthday, group_id, name),
                    )
                    print(f"Overwritten {name}")
                else:
                    print(f"Skipped {name}")

            else:
                cur.execute(
                    """
                    INSERT INTO contacts(name, phone, email, birthday, group_id)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (name, phone, email, birthday, group_id),
                )
                print(f"Imported {name}")

        conn.commit()
        print("CSV import finished.")

    except Exception as e:
        conn.rollback()
        print("CSV import error:", e)

    finally:
        cur.close()
        conn.close()


def add_new_phone_to_contact():
    name = input("Enter contact name: ").strip()
    phone = input("Enter new phone: ").strip()

    if not phone:
        print("Phone cannot be empty.")
        return

    conn = connect()
    if not conn:
        return

    try:
        cur = conn.cursor()

        cur.execute(
            """
            UPDATE contacts
            SET phone = %s
            WHERE name = %s
            """,
            (phone, name),
        )

        if cur.rowcount == 0:
            print("Contact not found.")
        else:
            conn.commit()
            print("Phone updated.")

    except Exception as e:
        conn.rollback()
        print("Add phone error:", e)

    finally:
        cur.close()
        conn.close()


def move_contact_to_group():
    name = input("Enter contact name: ").strip()
    group_id_input = input("Enter new group_id: ").strip()

    try:
        group_id = int(group_id_input)
    except ValueError:
        print("group_id must be integer.")
        return

    conn = connect()
    if not conn:
        return

    try:
        cur = conn.cursor()

        cur.execute(
            """
            UPDATE contacts
            SET group_id = %s
            WHERE name = %s
            """,
            (group_id, name),
        )

        if cur.rowcount == 0:
            print("Contact not found.")
        else:
            conn.commit()
            print("Contact moved to another group.")

    except Exception as e:
        conn.rollback()
        print("Move error:", e)

    finally:
        cur.close()
        conn.close()


def main():
    while True:
        print("\n========== EXTENDED PHONEBOOK ==========")
        print("1. Add contact with extended fields")
        print("2. Search across all fields")
        print("3. Search by email")
        print("4. Filter by group")
        print("5. Sort contacts")
        print("6. Paginated navigation")
        print("7. Export to JSON")
        print("8. Import from JSON")
        print("9. Import from CSV")
        print("10. Add one more phone to contact")
        print("11. Move contact to another group")
        print("0. Exit")

        choice = input("Choose: ").strip()

        if choice == "1":
            add_contact_extended()
        elif choice == "2":
            search_all_fields()
        elif choice == "3":
            search_by_email()
        elif choice == "4":
            filter_by_group()
        elif choice == "5":
            sort_contacts()
        elif choice == "6":
            paginate_navigation()
        elif choice == "7":
            export_to_json()
        elif choice == "8":
            import_from_json()
        elif choice == "9":
            import_from_csv()
        elif choice == "10":
            add_new_phone_to_contact()
        elif choice == "11":
            move_contact_to_group()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()