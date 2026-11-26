import os
import sys
import re

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from my_project import create_app, db
from my_project.auth.domain import (
    Address, Agency, Animator, Specialization,
    Client, HolidayType, OrderStatus, Role,
    PaymentMethod, Order, Payment, OrderAnimator,
    Review, AnimatorAuditLog
)

def seed():
    app = create_app()
    with app.app_context():
        db.create_all()
        if Agency.query.count() > 0:
            print("Database already contains data.")
            return

        sql_path = os.path.join(os.path.dirname(__file__), "data.sql")
        with open(sql_path, "r", encoding="utf-8") as f:
            sql_content = f.read()

        if '-- ============================================================================' in sql_content:
            seeding_sql = sql_content.split('-- ============================================================================')[0]
        else:
            seeding_sql = sql_content

        statements = re.findall(r'(INSERT INTO\s+.*?;\s*)', seeding_sql, re.DOTALL | re.IGNORECASE)
        print(f"Found {len(statements)} insert statements in data.sql.")

        for stmt in statements:

            cleaned = re.sub(r'--.*?\n', '', stmt).strip()

            cleaned = cleaned.replace('`', '')
            try:
                db.session.execute(db.text(cleaned))
            except Exception as e:
                print(f"Error executing statement: {e}")

        db.session.commit()
        print("Seeding completed successfully!")
        print(f"Agencies count: {Agency.query.count()}")
        print(f"Animators count: {Animator.query.count()}")
        print(f"Orders count: {Order.query.count()}")
        print(f"Payments count: {Payment.query.count()}")
        print(f"Reviews count: {Review.query.count()}")

if __name__ == '__main__':
    seed()
