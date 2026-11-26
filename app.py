import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from my_project import create_app, db, load_config
from my_project.auth.domain import Agency

app = create_app()

def init_db():
    with app.app_context():
        db.create_all()

        if db.engine.name != 'mysql':
            from sqlalchemy import text
            try:
                with db.engine.begin() as conn:
                    conn.execute(text('DROP TRIGGER IF EXISTS trg_animators_log_update_sqlite;'))
                    conn.execute(text('''
                        CREATE TRIGGER trg_animators_log_update_sqlite
                        AFTER UPDATE OF hourly_rate ON animators
                        FOR EACH ROW
                        WHEN OLD.hourly_rate <> NEW.hourly_rate
                        BEGIN
                            INSERT INTO animator_audit_logs (
                                animator_id, old_hourly_rate, new_hourly_rate, modified_at, details
                            ) VALUES (
                                NEW.animator_id, OLD.hourly_rate, NEW.hourly_rate, datetime('now', 'localtime'),
                                'Hourly rate changed from ' || OLD.hourly_rate || ' to ' || NEW.hourly_rate
                            );
                        END;
                    '''))
            except Exception as e:
                print(f"Notice during trigger setup: {e}")

        if Agency.query.count() == 0:
            from seed_data import seed
            seed()

if __name__ == '__main__':
    init_db()

    config = load_config()
    server_cfg = config.get('server', {})
    host = server_cfg.get('host', '127.0.0.1')
    port = int(server_cfg.get('port', 5000))
    debug = bool(server_cfg.get('debug', True))

    print(f"Starting Flask server on http://{host}:{port} ...")
    app.run(host=host, port=port, debug=debug)
