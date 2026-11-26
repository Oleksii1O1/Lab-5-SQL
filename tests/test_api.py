import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from my_project import create_app, db
from my_project.auth.domain import (
    Address, Agency, Animator, Specialization,
    Client, HolidayType, OrderStatus, Role,
    PaymentMethod, Order, Payment, OrderAnimator,
    agency_animators, animator_specializations
)
from datetime import date, time

@pytest.fixture
def client():
    test_config = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    }
    app = create_app(test_config=test_config)

    with app.app_context():
        db.create_all()

        addr = Address(city="Львів", street="вул. Стрийська", building="30А", place_name="Казка")
        db.session.add(addr)

        agency = Agency(name="Веселка", phone="+380321111111", email="info@veselka.ua", city="Львів")
        db.session.add(agency)

        animator = Animator(first_name="Олена", last_name="Коваль", phone="+380501000001", email="olena@mail.ua", hourly_rate=400.0)
        db.session.add(animator)

        spec = Specialization(name="Клоунада")
        db.session.add(spec)

        client_obj = Client(full_name="Петренко Ірина", phone="+380671000001", email="irina@gmail.com")
        db.session.add(client_obj)

        htype = HolidayType(name="День народження")
        db.session.add(htype)

        status = OrderStatus(name="Виконано")
        db.session.add(status)

        role = Role(name="Ведучий")
        db.session.add(role)

        pm = PaymentMethod(name="Готівка")
        db.session.add(pm)

        db.session.commit()

        agency.animators.append(animator)
        animator.specializations.append(spec)
        db.session.commit()

        order = Order(
            agency_id=agency.agency_id,
            client_id=client_obj.client_id,
            holiday_type_id=htype.holiday_type_id,
            address_id=addr.address_id,
            status_id=status.status_id,
            event_date=date(2026, 5, 12),
            start_time=time(14, 0),
            duration_minutes=120,
            total_cost=1500.0
        )
        db.session.add(order)
        db.session.commit()

        payment = Payment(
            order_id=order.order_id,
            method_id=pm.method_id,
            amount=1500.0,
            paid_at=date(2026, 5, 12)
        )
        db.session.add(payment)

        oa = OrderAnimator(
            order_id=order.order_id,
            animator_id=animator.animator_id,
            role_id=role.role_id,
            fee=800.0
        )
        db.session.add(oa)
        db.session.commit()

    with app.test_client() as test_client:
        yield test_client

def test_get_all_agencies(client):
    res = client.get('/api/agencies')
    assert res.status_code == 200
    data = res.get_json()
    assert len(data) >= 1
    assert data[0]['name'] == 'Веселка'

def test_get_agency_by_id(client):
    res = client.get('/api/agencies/1')
    assert res.status_code == 200
    data = res.get_json()
    assert data['name'] == 'Веселка'

def test_create_agency(client):
    new_agency = {
        'name': 'Нова Агенція',
        'phone': '+380509998877',
        'email': 'new@agency.ua',
        'city': 'Київ'
    }
    res = client.post('/api/agencies', json=new_agency)
    assert res.status_code == 201
    data = res.get_json()
    assert data['agency_id'] is not None
    assert data['name'] == 'Нова Агенція'

def test_update_agency(client):
    update_data = {
        'name': 'Веселка Оновлена',
        'city': 'Дніпро'
    }
    res = client.put('/api/agencies/1', json=update_data)
    assert res.status_code == 200
    data = res.get_json()
    assert data['name'] == 'Веселка Оновлена'
    assert data['city'] == 'Дніпро'

def test_delete_agency(client):

    res_create = client.post('/api/agencies', json={
        'name': 'Агенція для видалення',
        'phone': '+380991112233',
        'city': 'Одеса'
    })
    new_id = res_create.get_json()['agency_id']

    res = client.delete(f'/api/agencies/{new_id}')
    assert res.status_code == 200

    res_check = client.get(f'/api/agencies/{new_id}')
    assert res_check.status_code == 404

def test_relationship_m1_agency_orders(client):
    res = client.get('/api/agencies/1/orders')
    assert res.status_code == 200
    orders = res.get_json()
    assert len(orders) >= 1
    assert orders[0]['total_cost'] == 1500.0

def test_relationship_m1_order_payments(client):
    res = client.get('/api/orders/1/payments')
    assert res.status_code == 200
    payments = res.get_json()
    assert len(payments) >= 1
    assert payments[0]['amount'] == 1500.0

def test_relationship_mm_agency_animators(client):
    res = client.get('/api/agencies/1/animators')
    assert res.status_code == 200
    animators = res.get_json()
    assert len(animators) >= 1
    assert animators[0]['first_name'] == 'Олена'

def test_relationship_mm_animator_specializations(client):
    res = client.get('/api/animators/1/specializations')
    assert res.status_code == 200
    specs = res.get_json()
    assert len(specs) >= 1
    assert specs[0]['name'] == 'Клоунада'

def test_relationship_mm_order_animators(client):
    res = client.get('/api/orders/1/animators')
    assert res.status_code == 200
    assignments = res.get_json()
    assert len(assignments) >= 1
    assert assignments[0]['role_name'] == 'Ведучий'
    assert assignments[0]['fee'] == 800.0

def test_reviews_crud(client):

    review_data = {
        'animator_id': 1,
        'rating': 5,
        'comment': 'Чудовий аніматор, свято вдалося!',
        'review_date': '2026-05-15'
    }
    res = client.post('/api/reviews', json=review_data)
    assert res.status_code == 201
    created = res.get_json()
    assert created['review_id'] is not None
    assert created['rating'] == 5
    rev_id = created['review_id']

    res_get = client.get(f'/api/reviews/{rev_id}')
    assert res_get.status_code == 200
    assert res_get.get_json()['comment'] == 'Чудовий аніматор, свято вдалося!'

    res_anim = client.get('/api/reviews/animator/1')
    assert res_anim.status_code == 200
    assert len(res_anim.get_json()) >= 1

    res_upd = client.put(f'/api/reviews/{rev_id}', json={'rating': 4, 'comment': 'Оновлений коментар'})
    assert res_upd.status_code == 200
    assert res_upd.get_json()['rating'] == 4

    res_del = client.delete(f'/api/reviews/{rev_id}')
    assert res_del.status_code == 200
    res_check = client.get(f'/api/reviews/{rev_id}')
    assert res_check.status_code == 404

def test_procedure_insert_client(client):
    payload = {
        'full_name': 'Василенко Тарас Дмитрович',
        'phone': '+380998887766',
        'email': 'taras.v@gmail.com'
    }
    res = client.post('/api/procedures/insert-client', json=payload)
    assert res.status_code == 201
    data = res.get_json()
    assert data['client_id'] is not None

    res_client = client.get(f"/api/clients/{data['client_id']}")
    assert res_client.status_code == 200
    assert res_client.get_json()['full_name'] == 'Василенко Тарас Дмитрович'

def test_procedure_link_m2m(client):

    client.post('/api/specializations', json={'name': 'Аквагрим 2'})

    payload = {
        'first_name': 'Олена',
        'last_name': 'Коваль',
        'specialization_name': 'Аквагрим 2'
    }
    res = client.post('/api/procedures/link-m2m', json=payload)
    assert res.status_code == 200
    data = res.get_json()
    assert data['animator_id'] == 1
    assert data['specialization_id'] is not None

def test_procedure_insert_ten_nonames(client):
    res = client.post('/api/procedures/insert-nonames')
    assert res.status_code == 200
    data = res.get_json()
    assert 'Successfully inserted 10 nonames' in data['result']

    res_specs = client.get('/api/specializations')
    names = [s['name'] for s in res_specs.get_json()]
    assert any('Noname' in n for n in names)

def test_procedure_and_function_stats_avg(client):
    res = client.get('/api/procedures/stats-avg')
    assert res.status_code == 200
    data = res.get_json()
    assert isinstance(data, list)
    assert len(data) >= 1

    assert 'average_hourly_rate' in data[0]
    assert 'difference_from_avg' in data[0]
    assert data[0]['hourly_rate'] >= data[0]['average_hourly_rate']

def test_procedure_cursor_split(client):
    res = client.post('/api/procedures/cursor-split')
    assert res.status_code == 200
    data = res.get_json()
    assert 'table1_name' in data
    assert 'table2_name' in data
    assert data['total_rows_processed'] >= 1
    assert data['table1_rows'] + data['table2_rows'] == data['total_rows_processed']

def test_animator_rate_change_audit_log(client):

    res_upd = client.put('/api/animators/1', json={'hourly_rate': 450.0})
    assert res_upd.status_code == 200

    res_logs = client.get('/api/audit-logs')
    assert res_logs.status_code == 200
    logs = res_logs.get_json()
    assert len(logs) >= 1

    last_log = logs[-1]
    assert last_log['animator_id'] == 1
    assert last_log['new_hourly_rate'] == 450.0
