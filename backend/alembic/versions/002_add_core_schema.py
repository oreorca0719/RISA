"""add core schema

Revision ID: 002
Revises: 001
Create Date: 2026-04-27
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:

    # 1. user_relations — 부모-학생 연동 (추후 기능 대비)
    op.create_table(
        'user_relations',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('parent_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('student_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint('parent_id', 'student_id', name='uq_user_relations'),
    )
    op.create_index('ix_user_relations_parent_id', 'user_relations', ['parent_id'])
    op.create_index('ix_user_relations_student_id', 'user_relations', ['student_id'])

    # 2. texts — 텍스트 풀 (AI 생성 + 관리자 검수)
    op.create_table(
        'texts',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('grade', sa.Enum('elem4', 'elem5', 'elem6', name='textgrade'), nullable=False),
        sa.Column('genre', sa.Enum('narrative', 'expository', name='textgenre'), nullable=False),
        sa.Column('level', sa.Enum('low', 'mid', 'high', name='textlevel'), nullable=False),
        sa.Column('word_count', sa.Integer(), nullable=True),
        sa.Column('status', sa.Enum('draft', 'reviewing', 'approved', name='textstatus'), nullable=False, server_default='draft'),
        sa.Column('source', sa.Enum('ai_generated', 'manual', name='textsource'), nullable=False, server_default='ai_generated'),
        sa.Column('metadata', JSONB(), nullable=True),  # 7원칙 검수 메모 등
        sa.Column('created_by', sa.Integer(), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now()),
    )
    op.create_index('ix_texts_grade_genre_level', 'texts', ['grade', 'genre', 'level'])
    op.create_index('ix_texts_status', 'texts', ['status'])

    # 3. diagnosis_sessions — 진단 세션 (재시도 허용, 이력 전체 보관)
    op.create_table(
        'diagnosis_sessions',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('student_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('text_id', sa.Integer(), sa.ForeignKey('texts.id', ondelete='SET NULL'), nullable=True),
        sa.Column('status', sa.Enum('in_progress', 'completed', 'abandoned', name='sessionstatus'), nullable=False, server_default='in_progress'),
        sa.Column('started_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index('ix_diagnosis_sessions_student_id', 'diagnosis_sessions', ['student_id'])

    # 4. fluency_results — 유창성 결과 (음독/묵독)
    op.create_table(
        'fluency_results',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('session_id', sa.Integer(), sa.ForeignKey('diagnosis_sessions.id', ondelete='CASCADE'), nullable=False),
        sa.Column('type', sa.Enum('oral', 'silent', name='fluencytype'), nullable=False),
        # 음독
        sa.Column('reading_time_seconds', sa.Float(), nullable=True),
        sa.Column('total_syllables', sa.Integer(), nullable=True),
        sa.Column('error_count', sa.Integer(), nullable=True),
        sa.Column('automaticity_score', sa.Float(), nullable=True),   # 10초당 정확 음절 수
        sa.Column('accuracy_score', sa.Float(), nullable=True),       # 1 - (오류수/총음절수)
        # 묵독
        sa.Column('silent_reading_time', sa.Float(), nullable=True),
        sa.Column('comprehension_check_score', sa.Float(), nullable=True),
        sa.Column('raw_data', JSONB(), nullable=True),  # STT 원시 데이터 등
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_fluency_results_session_id', 'fluency_results', ['session_id'])

    # 5. comprehension_results — 독해 이해 결과 (사실적/추론적/비판적)
    op.create_table(
        'comprehension_results',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('session_id', sa.Integer(), sa.ForeignKey('diagnosis_sessions.id', ondelete='CASCADE'), nullable=False),
        sa.Column('question_type', sa.Enum('factual', 'inferential', 'critical', name='questiontype'), nullable=False),
        sa.Column('question_index', sa.Integer(), nullable=False),
        sa.Column('answer', sa.Text(), nullable=True),
        sa.Column('is_correct', sa.Boolean(), nullable=True),
        sa.Column('score', sa.Float(), nullable=True),
        sa.Column('ai_feedback', sa.Text(), nullable=True),  # Claude API 채점 피드백
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_comprehension_results_session_id', 'comprehension_results', ['session_id'])

    # 6. reader_profiles — 독자 유형 분류 결과
    op.create_table(
        'reader_profiles',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('student_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('session_id', sa.Integer(), sa.ForeignKey('diagnosis_sessions.id', ondelete='SET NULL'), nullable=True),
        sa.Column('reader_type', sa.Enum('avid', 'intermittent', 'non_reader', name='readertype'), nullable=False),
        sa.Column('reading_level', sa.Enum('low', 'mid', 'high', name='readinglevel'), nullable=False),
        sa.Column('fluency_score', sa.Float(), nullable=True),
        sa.Column('comprehension_score', sa.Float(), nullable=True),
        sa.Column('total_score', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_reader_profiles_student_id', 'reader_profiles', ['student_id'])

    # 7. prescriptions — 처방 결과 (DB 영구 저장)
    op.create_table(
        'prescriptions',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('student_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('session_id', sa.Integer(), sa.ForeignKey('diagnosis_sessions.id', ondelete='SET NULL'), nullable=True),
        sa.Column('profile_id', sa.Integer(), sa.ForeignKey('reader_profiles.id', ondelete='SET NULL'), nullable=True),
        sa.Column('prescription_matrix', sa.String(10), nullable=True),  # 예: "C-1", "A-3"
        sa.Column('recommended_texts', JSONB(), nullable=True),   # 추천 텍스트 ID 목록
        sa.Column('ai_recommendation', sa.Text(), nullable=True), # Claude API 처방 텍스트
        sa.Column('reading_goal', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_prescriptions_student_id', 'prescriptions', ['student_id'])

    # 8. reports — 리포팅 (학생/학부모/교사 대상)
    op.create_table(
        'reports',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('student_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('session_id', sa.Integer(), sa.ForeignKey('diagnosis_sessions.id', ondelete='SET NULL'), nullable=True),
        sa.Column('target_role', sa.Enum('student', 'parent', 'teacher', name='reportrole'), nullable=False),
        sa.Column('content', JSONB(), nullable=False),  # 리포트 내용 (JSON)
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_reports_student_id', 'reports', ['student_id'])


def downgrade() -> None:
    op.drop_table('reports')
    op.drop_table('prescriptions')
    op.drop_table('reader_profiles')
    op.drop_table('comprehension_results')
    op.drop_table('fluency_results')
    op.drop_table('diagnosis_sessions')
    op.drop_table('texts')
    op.drop_table('user_relations')

    for enum in ['reportrole', 'readinglevel', 'readertype', 'questiontype',
                 'fluencytype', 'sessionstatus', 'textsource', 'textstatus',
                 'textlevel', 'textgenre', 'textgrade']:
        op.execute(f'DROP TYPE IF EXISTS {enum}')
