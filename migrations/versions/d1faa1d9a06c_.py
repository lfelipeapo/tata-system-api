"""empty message

Revision ID: d1faa1d9a06c
Revises: 
Create Date: 2023-06-29 22:28:20.300595

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd1faa1d9a06c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('consulta_juridica')
    op.drop_index('ix_users_username', table_name='users')
    op.drop_table('users')
    op.drop_table('cliente')
    op.drop_table('produto')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('produto',
    sa.Column('pk_produto', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('nome', sa.VARCHAR(length=140), autoincrement=False, nullable=True),
    sa.Column('quantidade', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('valor', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('data_insercao', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('pk_produto', name='produto_pkey'),
    sa.UniqueConstraint('nome', name='produto_nome_key')
    )
    op.create_table('cliente',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('cliente_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('nome_cliente', sa.VARCHAR(length=80), autoincrement=False, nullable=False),
    sa.Column('cpf_cliente', sa.VARCHAR(length=11), autoincrement=False, nullable=False),
    sa.Column('data_cadastro', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('data_atualizacao', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='cliente_pkey'),
    sa.UniqueConstraint('cpf_cliente', name='cliente_cpf_cliente_key'),
    postgresql_ignore_search_path=False
    )
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('username', sa.VARCHAR(length=64), autoincrement=False, nullable=True),
    sa.Column('password_hash', sa.VARCHAR(length=128), autoincrement=False, nullable=True),
    sa.Column('name', sa.VARCHAR(length=64), autoincrement=False, nullable=True),
    sa.Column('image', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='users_pkey')
    )
    op.create_index('ix_users_username', 'users', ['username'], unique=False)
    op.create_table('consulta_juridica',
    sa.Column('pk_consulta', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('nome_cliente', sa.VARCHAR(length=80), autoincrement=False, nullable=True),
    sa.Column('cpf_cliente', sa.VARCHAR(length=11), autoincrement=False, nullable=True),
    sa.Column('data_consulta', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('horario_consulta', postgresql.TIME(), autoincrement=False, nullable=True),
    sa.Column('detalhes_consulta', sa.VARCHAR(length=200), autoincrement=False, nullable=True),
    sa.Column('cliente_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['cliente_id'], ['cliente.id'], name='consulta_juridica_cliente_id_fkey'),
    sa.PrimaryKeyConstraint('pk_consulta', name='consulta_juridica_pkey'),
    sa.UniqueConstraint('cpf_cliente', name='consulta_juridica_cpf_cliente_key'),
    sa.UniqueConstraint('nome_cliente', name='consulta_juridica_nome_cliente_key')
    )
    # ### end Alembic commands ###