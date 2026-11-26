import random
from datetime import datetime
from sqlalchemy import text
from my_project import db
from my_project.auth.domain import Animator, Specialization, Client, animator_specializations

class ProcedureDAO:

    @staticmethod
    def _is_mysql():
        return db.engine.name == 'mysql'

    def insert_client_proc(self, full_name, phone, email):
        if self._is_mysql():
            with db.engine.begin() as conn:
                conn.execute(
                    text("CALL sp_insert_client(:name, :phone, :email, @new_id)"),
                    {"name": full_name, "phone": phone, "email": email}
                )
                res = conn.execute(text("SELECT @new_id AS new_id")).fetchone()
                return {"client_id": res[0] if res else None, "status": "Inserted via MySQL stored procedure"}
        else:
            client = Client(full_name=full_name, phone=phone, email=email)
            db.session.add(client)
            db.session.commit()
            return {"client_id": client.client_id, "status": "Inserted via procedure emulation (SQLite)"}

    def link_m2m_proc(self, first_name, last_name, specialization_name):
        if self._is_mysql():
            with db.engine.begin() as conn:
                res = conn.execute(
                    text("CALL sp_link_animator_specialization(:fname, :lname, :sname)"),
                    {"fname": first_name, "lname": last_name, "sname": specialization_name}
                ).fetchone()
                return {
                    "animator_id": res[0] if res else None,
                    "specialization_id": res[1] if res else None,
                    "message": "Linked successfully via sp_link_animator_specialization"
                }
        else:
            animator = Animator.query.filter_by(first_name=first_name, last_name=last_name).first()
            if not animator:
                raise ValueError("Animator with given name not found")
            spec = Specialization.query.filter_by(name=specialization_name).first()
            if not spec:
                raise ValueError("Specialization with given name not found")

            exists = db.session.execute(
                animator_specializations.select().where(
                    (animator_specializations.c.animator_id == animator.animator_id) &
                    (animator_specializations.c.specialization_id == spec.specialization_id)
                )
            ).fetchone()

            if not exists:
                db.session.execute(
                    animator_specializations.insert().values(
                        animator_id=animator.animator_id,
                        specialization_id=spec.specialization_id
                    )
                )
                db.session.commit()

            return {
                "animator_id": animator.animator_id,
                "specialization_id": spec.specialization_id,
                "message": "Linked successfully via procedure emulation (SQLite)"
            }

    def insert_ten_nonames_proc(self):
        if self._is_mysql():
            with db.engine.begin() as conn:
                res = conn.execute(text("CALL sp_insert_ten_nonames()")).fetchone()
                return {"result": res[0] if res else "Batch insert executed successfully"}
        else:
            all_specs = Specialization.query.all()
            max_num = 0
            import re
            for s in all_specs:
                m = re.match(r'^Noname(\d+)$', s.name)
                if m:
                    num = int(m.group(1))
                    if num > max_num:
                        max_num = num

            created = []
            for i in range(1, 11):
                name = f"Noname{max_num + i}"
                new_s = Specialization(name=name)
                db.session.add(new_s)
                created.append(name)
            db.session.commit()

            return {
                "result": f"Successfully inserted 10 nonames from Noname{max_num + 1} to Noname{max_num + 10}",
                "inserted": created
            }

    def get_animators_above_avg_proc(self):
        if self._is_mysql():
            with db.engine.begin() as conn:
                res = conn.execute(text("CALL sp_get_animators_above_avg_rate()")).fetchall()
                rows = []
                for r in res:
                    rows.append({
                        "animator_id": r[0],
                        "first_name": r[1],
                        "last_name": r[2],
                        "hourly_rate": float(r[3]),
                        "average_hourly_rate": float(r[4]),
                        "difference_from_avg": float(r[5])
                    })
                return rows
        else:
            animators = Animator.query.all()
            if not animators:
                return []
            rates = [float(a.hourly_rate) for a in animators]
            avg_rate = round(sum(rates) / len(rates), 2)
            filtered = [a for a in animators if float(a.hourly_rate) >= avg_rate]
            filtered.sort(key=lambda a: float(a.hourly_rate), reverse=True)

            return [
                {
                    "animator_id": a.animator_id,
                    "first_name": a.first_name,
                    "last_name": a.last_name,
                    "hourly_rate": float(a.hourly_rate),
                    "average_hourly_rate": avg_rate,
                    "difference_from_avg": round(float(a.hourly_rate) - avg_rate, 2)
                }
                for a in filtered
            ]

    def cursor_split_animators_proc(self):
        if self._is_mysql():
            with db.engine.begin() as conn:
                res = conn.execute(
                    text("CALL sp_cursor_split_animators(@t1, @t2, @total, @r1, @r2)")
                ).fetchone()
                return {
                    "table1_name": res[0] if res else None,
                    "table1_rows": res[1] if res else 0,
                    "table2_name": res[2] if res else None,
                    "table2_rows": res[3] if res else 0,
                    "total_rows_processed": res[4] if res else 0
                }
        else:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            t1 = f"animators_split1_{ts}"
            t2 = f"animators_split2_{ts}"

            animators = Animator.query.all()
            count_t1 = 0
            count_t2 = 0

            with db.engine.begin() as conn:
                conn.execute(text(f"""
                    CREATE TABLE {t1} (
                        animator_id INTEGER PRIMARY KEY,
                        first_name TEXT,
                        last_name TEXT,
                        phone TEXT,
                        email TEXT,
                        hourly_rate REAL
                    )
                """))
                conn.execute(text(f"""
                    CREATE TABLE {t2} (
                        animator_id INTEGER PRIMARY KEY,
                        first_name TEXT,
                        last_name TEXT,
                        phone TEXT,
                        email TEXT,
                        hourly_rate REAL
                    )
                """))

                for a in animators:
                    target = t1 if random.random() < 0.5 else t2
                    if target == t1:
                        count_t1 += 1
                    else:
                        count_t2 += 1
                    conn.execute(
                        text(f"INSERT INTO {target} VALUES (:id, :fname, :lname, :phone, :email, :rate)"),
                        {
                            "id": a.animator_id,
                            "fname": a.first_name,
                            "lname": a.last_name,
                            "phone": a.phone,
                            "email": a.email,
                            "rate": float(a.hourly_rate)
                        }
                    )

            return {
                "table1_name": t1,
                "table1_rows": count_t1,
                "table2_name": t2,
                "table2_rows": count_t2,
                "total_rows_processed": len(animators)
            }
