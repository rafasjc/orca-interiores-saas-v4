"""
Configurações da Aplicação Orça Interiores SaaS
"""

import streamlit as st

class Config:
    # Informações da aplicação
    APP_NAME = "🏠 Orça Interiores SaaS"
    APP_DESCRIPTION = "Sistema Profissional de Orçamento de Marcenaria"
    APP_VERSION = "1.0.0"
    
    # Configurações de arquivo
    MAX_FILE_SIZE_MB = 500
    ALLOWED_EXTENSIONS = ['obj', 'dae', 'stl', 'ply']
    
    # Cores do tema
    CORES = {
        'primaria': '#2E86AB',
        'secundaria': '#A23B72',
        'sucesso': '#F18F01',
        'fundo': '#F5F5F5'
    }
    
    # Planos de assinatura
    PLANOS = {
        'free': {
            'nome': 'Gratuito',
            'preco': 0,
            'projetos_mes': 3,
            'recursos': [
                'Upload de arquivos 3D',
                'Orçamento básico',
                'Relatório simples'
            ]
        },
        'basic': {
            'nome': 'Básico',
            'preco': 49.90,
            'projetos_mes': 50,
            'recursos': [
                'Todos recursos gratuitos',
                'Visualização 3D',
                'Preços atualizados',
                'Relatórios detalhados'
            ]
        },
        'pro': {
            'nome': 'Profissional',
            'preco': 99.90,
            'projetos_mes': 200,
            'recursos': [
                'Todos recursos básicos',
                'API de integração',
                'White label',
                'Suporte prioritário'
            ]
        },
        'enterprise': {
            'nome': 'Empresarial',
            'preco': 299.90,
            'projetos_mes': 999999,
            'recursos': [
                'Todos recursos profissionais',
                'Multi-usuários',
                'Customização completa',
                'Suporte dedicado'
            ]
        }
    }
    
    # Preços de materiais (Léo Madeiras)
    PRECOS_MATERIAIS = {
        'MDF 15mm': {
            'preco_m2': 69.15,
            'desperdicio': 0.15,
            'descricao': 'MDF Cru 15mm'
        },
        'MDF 18mm': {
            'preco_m2': 82.50,
            'desperdicio': 0.15,
            'descricao': 'MDF Cru 18mm'
        },
        'Compensado 15mm': {
            'preco_m2': 64.00,
            'desperdicio': 0.12,
            'descricao': 'Compensado Naval 15mm'
        },
        'Melamina 15mm': {
            'preco_m2': 89.50,
            'desperdicio': 0.10,
            'descricao': 'Melamina Branca 15mm'
        }
    }
    
    # Preços de acessórios
    PRECOS_ACESSORIOS = {
        'comum': {
            'dobradica': 12.50,
            'corredicao': 25.00,
            'puxador': 8.00,
            'fechadura': 15.00,
            'parafuso': 0.50
        },
        'premium': {
            'dobradica': 28.00,
            'corredicao': 65.00,
            'puxador': 25.00,
            'fechadura': 45.00,
            'parafuso': 1.20
        }
    }
    
    @staticmethod
    def get_page_config():
        """Configuração da página Streamlit"""
        return {
            'page_title': Config.APP_NAME,
            'page_icon': '🏠',
            'layout': 'wide',
            'initial_sidebar_state': 'expanded'
        }
    
    @staticmethod
    def get_css_styles():
        """Estilos CSS customizados"""
        return f"""
        <style>
        .main-header {{
            background: linear-gradient(90deg, {Config.CORES['primaria']}, {Config.CORES['secundaria']});
            padding: 2rem;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
            animation: fadeIn 1s ease-in;
        }}
        
        .metric-card {{
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-left: 4px solid {Config.CORES['primaria']};
            margin-bottom: 1rem;
        }}
        
        .success-card {{
            background: linear-gradient(135deg, #d4edda, #c3e6cb);
            padding: 1.5rem;
            border-radius: 10px;
            border-left: 4px solid #28a745;
            margin: 1rem 0;
        }}
        
        .plan-card {{
            background: white;
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            text-align: center;
            margin: 1rem 0;
            transition: transform 0.3s ease;
        }}
        
        .plan-card:hover {{
            transform: translateY(-5px);
        }}
        
        .fade-in {{
            animation: fadeIn 1s ease-in;
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .stButton > button {{
            background: linear-gradient(90deg, {Config.CORES['primaria']}, {Config.CORES['secundaria']});
            color: white;
            border: none;
            border-radius: 25px;
            padding: 0.5rem 2rem;
            font-weight: bold;
            transition: all 0.3s ease;
        }}
        
        .stButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }}
        </style>
        """

