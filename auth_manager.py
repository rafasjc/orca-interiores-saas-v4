"""
Sistema de Autenticação e Gerenciamento de Usuários
"""

import streamlit as st
import sqlite3
import hashlib
import json
from datetime import datetime, timedelta
from typing import Dict, Optional
from config import Config

class AuthManager:
    def __init__(self):
        self.db_path = "usuarios.db"
        self.init_database()
        self.create_demo_users()
    
    def init_database(self):
        """Inicializa o banco de dados"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE NOT NULL,
                    senha_hash TEXT NOT NULL,
                    nome TEXT NOT NULL,
                    plano TEXT DEFAULT 'free',
                    projetos_mes INTEGER DEFAULT 0,
                    data_criacao TEXT NOT NULL,
                    ultimo_login TEXT,
                    ativo BOOLEAN DEFAULT 1
                )
            ''')
            
            conn.commit()
            conn.close()
        except Exception as e:
            st.error(f"Erro ao inicializar banco: {e}")
    
    def hash_password(self, password: str) -> str:
        """Gera hash da senha"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_demo_users(self):
        """Cria usuários demo para teste"""
        demo_users = [
            {
                'email': 'demo@orcainteriores.com',
                'senha': 'demo123',
                'nome': 'Usuário Demo',
                'plano': 'pro'
            },
            {
                'email': 'arquiteto@teste.com',
                'senha': 'arq123',
                'nome': 'Arquiteto Teste',
                'plano': 'basic'
            },
            {
                'email': 'marceneiro@teste.com',
                'senha': 'marc123',
                'nome': 'Marceneiro Teste',
                'plano': 'enterprise'
            }
        ]
        
        for user in demo_users:
            self.create_user(
                user['email'],
                user['senha'],
                user['nome'],
                user['plano']
            )
    
    def create_user(self, email: str, password: str, nome: str, plano: str = 'free') -> bool:
        """Cria novo usuário"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            senha_hash = self.hash_password(password)
            data_criacao = datetime.now().isoformat()
            
            cursor.execute('''
                INSERT OR IGNORE INTO usuarios 
                (email, senha_hash, nome, plano, data_criacao)
                VALUES (?, ?, ?, ?, ?)
            ''', (email, senha_hash, nome, plano, data_criacao))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            st.error(f"Erro ao criar usuário: {e}")
            return False
    
    def authenticate(self, email: str, password: str) -> Optional[Dict]:
        """Autentica usuário"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            senha_hash = self.hash_password(password)
            
            cursor.execute('''
                SELECT id, email, nome, plano, projetos_mes, data_criacao
                FROM usuarios 
                WHERE email = ? AND senha_hash = ? AND ativo = 1
            ''', (email, senha_hash))
            
            result = cursor.fetchone()
            
            if result:
                # Atualizar último login
                cursor.execute('''
                    UPDATE usuarios 
                    SET ultimo_login = ? 
                    WHERE email = ?
                ''', (datetime.now().isoformat(), email))
                
                conn.commit()
                
                user_data = {
                    'id': result[0],
                    'email': result[1],
                    'nome': result[2],
                    'plano': result[3],
                    'projetos_mes': result[4],
                    'data_criacao': result[5]
                }
                
                conn.close()
                return user_data
            
            conn.close()
            return None
        except Exception as e:
            st.error(f"Erro na autenticação: {e}")
            return None
    
    def increment_project_count(self, user_id: int):
        """Incrementa contador de projetos do usuário"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE usuarios 
                SET projetos_mes = projetos_mes + 1 
                WHERE id = ?
            ''', (user_id,))
            
            conn.commit()
            conn.close()
        except Exception as e:
            st.error(f"Erro ao incrementar contador: {e}")
    
    def check_project_limit(self, usuario: Dict) -> bool:
        """Verifica se usuário pode criar mais projetos"""
        plano_info = Config.PLANOS.get(usuario['plano'], Config.PLANOS['free'])
        limite = plano_info['projetos_mes']
        
        if limite == 999999:  # Ilimitado
            return True
        
        return usuario['projetos_mes'] < limite
    
    def show_login_form(self):
        """Exibe formulário de login"""
        st.markdown("""
        <div class="main-header">
            <h1>🏠 Orça Interiores SaaS</h1>
            <p>Sistema Profissional de Orçamento de Marcenaria</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("### 🔐 Acesso ao Sistema")
            
            with st.form("login_form"):
                email = st.text_input("📧 Email", placeholder="seu@email.com")
                password = st.text_input("🔒 Senha", type="password", placeholder="Sua senha")
                
                col_login, col_demo = st.columns(2)
                
                with col_login:
                    login_button = st.form_submit_button("🚀 Entrar", use_container_width=True)
                
                with col_demo:
                    demo_button = st.form_submit_button("🧪 Conta Demo", use_container_width=True)
            
            if login_button and email and password:
                user = self.authenticate(email, password)
                if user:
                    st.session_state.user = user
                    st.success(f"✅ Bem-vindo, {user['nome']}!")
                    st.rerun()
                else:
                    st.error("❌ Email ou senha incorretos!")
            
            if demo_button:
                # Login automático com conta demo
                user = self.authenticate("demo@orcainteriores.com", "demo123")
                if user:
                    st.session_state.user = user
                    st.success(f"✅ Logado como {user['nome']} (Conta Demo)")
                    st.rerun()
            
            # Informações das contas demo
            st.markdown("---")
            st.markdown("### 🧪 Contas Demo Disponíveis")
            
            demo_accounts = [
                ("demo@orcainteriores.com", "demo123", "Plano Pro"),
                ("arquiteto@teste.com", "arq123", "Plano Básico"),
                ("marceneiro@teste.com", "marc123", "Plano Empresarial")
            ]
            
            for email, senha, plano in demo_accounts:
                st.markdown(f"**{email}** | Senha: `{senha}` | {plano}")
    
    def show_user_dashboard(self, usuario: Dict):
        """Exibe dashboard do usuário na sidebar"""
        with st.sidebar:
            st.markdown("---")
            st.markdown("### 👤 Minha Conta")
            
            plano_info = Config.PLANOS.get(usuario['plano'], Config.PLANOS['free'])
            
            st.markdown(f"**Nome:** {usuario['nome']}")
            st.markdown(f"**Email:** {usuario['email']}")
            st.markdown(f"**Plano:** {plano_info['nome']}")
            
            # Progresso de projetos
            if plano_info['projetos_mes'] != 999999:
                progresso = usuario['projetos_mes'] / plano_info['projetos_mes']
                st.progress(progresso)
                st.markdown(f"**Projetos:** {usuario['projetos_mes']}/{plano_info['projetos_mes']}")
            else:
                st.markdown(f"**Projetos:** {usuario['projetos_mes']} (Ilimitado)")
            
            # Recursos do plano
            st.markdown("**Recursos:**")
            for recurso in plano_info['recursos']:
                st.markdown(f"✅ {recurso}")
            
            if st.button("🚪 Sair", use_container_width=True):
                del st.session_state.user
                st.rerun()
    
    def is_authenticated(self) -> bool:
        """Verifica se usuário está autenticado"""
        return 'user' in st.session_state
    
    def get_current_user(self) -> Optional[Dict]:
        """Retorna usuário atual"""
        return st.session_state.get('user', None)

