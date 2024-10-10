"""Initial tables

Revision ID: 68381e3b5947
Revises: 
Create Date: 2024-10-09 18:29:00.732778

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '68381e3b5947'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Crear tabla settings
    op.create_table(
        'settings',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('config_name', sa.String(255), nullable=False, unique=True),
        sa.Column('config_value', sa.String(255), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP, server_default=sa.func.now(), onupdate=sa.func.now())
    )

    # Índice en config_name porque es único y puede ser consultado frecuentemente
    op.create_index('ix_settings_config_name', 'settings', ['config_name'])

    # Crear tabla sensors
    op.create_table(
        'sensors',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('sensor_name', sa.String(255), nullable=False),
        sa.Column('sensor_type', sa.String(255), nullable=False),
        sa.Column('location', sa.String(255), nullable=True),
        sa.Column('unit', sa.String(50), nullable=False),
        sa.Column('is_active', sa.Boolean, server_default='true'),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.func.now())
    )

    # Índices para mejorar consultas frecuentes
    op.create_index('ix_sensors_sensor_name', 'sensors', ['sensor_name'])
    op.create_index('ix_sensors_sensor_type', 'sensors', ['sensor_type'])
    op.create_index('ix_sensors_is_active', 'sensors', ['is_active'])

    # Crear tabla sensor_data
    op.create_table(
        'sensor_data',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('sensor_id', sa.Integer, sa.ForeignKey('sensors.id'), nullable=False),
        sa.Column('value', sa.Float, nullable=False),
        sa.Column('recorded_at', sa.TIMESTAMP, server_default=sa.func.now())
    )

    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('devices',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=50), nullable=False),
                    sa.Column('type', sa.String(length=50), nullable=False),
                    sa.Column('current_state_id', sa.Integer(), nullable=True),
                    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
                    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('device_states',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('device_id', sa.Integer(), nullable=True),
                    sa.Column('state', sa.String(length=50), nullable=False),
                    sa.Column('description', sa.Text(), nullable=True),
                    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
                    sa.ForeignKeyConstraint(['device_id'], ['devices.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )

    # Insertar dispositivos por defecto usando bulk_insert
    op.bulk_insert(
        sa.table('devices',
                 sa.column('name', sa.String),
                 sa.column('type', sa.String)
                 ),
        [
            {"name": "Default Lamp", "type": "lamp"},
            {"name": "Default Fan", "type": "fan"}
        ]
    )

    # Insertar estados por defecto de los dispositivos usando bulk_insert
    op.bulk_insert(
        sa.table('device_states',
                 sa.column('device_id', sa.Integer),
                 sa.column('state', sa.String),
                 sa.column('description', sa.Text)),
        [
            {"device_id": 1, "state": "on", "description": "Lámpara encendida"},
            {"device_id": 1, "state": "off", "description": "Lámpara apagada"},
            {"device_id": 2, "state": "speed_1", "description": "Ventilador en velocidad 1"},
            {"device_id": 2, "state": "speed_2", "description": "Ventilador en velocidad 2"},
            {"device_id": 2, "state": "off", "description": "Ventilador apagado"}
        ]
    )

    # Índices para sensor_data
    op.create_index('ix_sensor_data_sensor_id', 'sensor_data', ['sensor_id'])
    op.create_index('ix_sensor_data_recorded_at', 'sensor_data', ['recorded_at'])

    # Insertar datos de ejemplo en la tabla de sensores
    op.bulk_insert(
        sa.table('sensors',
                 sa.column('sensor_name', sa.String),
                 sa.column('sensor_type', sa.String),
                 sa.column('location', sa.String),
                 sa.column('unit', sa.String),
                 sa.column('is_active', sa.Boolean)
                 ),
        [
            {
                'sensor_name': 'Temperature Sensor',
                'sensor_type': 'Temperature',
                'location': 'Room 101',
                'unit': 'Celsius',
                'is_active': True
            },
            {
                'sensor_name': 'Motion Sensor (HC-SR501)',
                'sensor_type': 'PIR',
                'location': 'Room 101',
                'unit': 'Detection',
                'is_active': True
            },
            {
                'sensor_name': 'Air Quality Sensor',
                'sensor_type': 'Air Quality',
                'location': 'Room 101',
                'unit': 'AQI',
                'is_active': True
            }
        ]
    )

def downgrade():
    # Borrar índices
    op.drop_index('ix_sensor_data_recorded_at', table_name='sensor_data')
    op.drop_index('ix_sensor_data_sensor_id', table_name='sensor_data')
    op.drop_index('ix_sensors_is_active', table_name='sensors')
    op.drop_index('ix_sensors_sensor_type', table_name='sensors')
    op.drop_index('ix_sensors_sensor_name', table_name='sensors')
    op.drop_index('ix_settings_config_name', table_name='settings')

    # Borrar tabla sensor_data
    op.drop_table('sensor_data')

    # Borrar tabla sensors
    op.drop_table('sensors')

    # Borrar tabla settings
    op.drop_table('settings')

    op.drop_table('device_states')
    op.drop_table('devices')