"""
Orça Interiores SaaS - Aplicação Principal
Sistema Profissional de Orçamento de Marcenaria
"""

import streamlit as st
import json
from typing import Dict, List

# Imports dos módulos
from config import Config
from auth_manager import AuthManager
from file_analyzer import FileAnalyzer
from orcamento_engine import OrcamentoEngine

# Configuração da página
st.set_page_config(**Config.get_page_config())

# CSS customizado
st.markdown(Config.get_css_styles(), unsafe_allow_html=True)

# Inicializar componentes
@st.cache_resource
def init_components():
    """Inicializa componentes da aplicação"""
    return {
        'auth': AuthManager(),
        'analyzer': FileAnalyzer(),
        'orcamento': OrcamentoEngine()
    }

def main():
    """Função principal da aplicação"""
    # Inicializar componentes
    components = init_components()
    auth_manager = components['auth']
    
    # Verificar autenticação
    if not auth_manager.is_authenticated():
        auth_manager.show_login_form()
        return
    
    # Usuário autenticado - mostrar aplicação
    usuario = auth_manager.get_current_user()
    mostrar_aplicacao_principal(components, usuario)

def mostrar_aplicacao_principal(components: Dict, usuario: Dict):
    """Mostra aplicação principal para usuário autenticado"""
    auth_manager = components['auth']
    file_analyzer = components['analyzer']
    orcamento_engine = components['orcamento']
    
    # Dashboard do usuário na sidebar
    auth_manager.show_user_dashboard(usuario)
    
    # Verificar limite de projetos
    if not auth_manager.check_project_limit(usuario):
        st.error("❌ Limite de projetos atingido para seu plano!")
        st.info("💎 Faça upgrade para continuar criando orçamentos.")
        return
    
    # Header principal
    st.markdown("""
    <div class="main-header fade-in">
        <h1>🏠 Orça Interiores SaaS</h1>
        <p>Sistema Profissional de Orçamento de Marcenaria</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar com configurações
    with st.sidebar:
        st.markdown("---")
        st.markdown("### ⚙️ Configurações do Orçamento")
        
        # Configurações de material
        material = st.selectbox(
            "📦 Material Principal",
            options=list(Config.PRECOS_MATERIAIS.keys()),
            index=0
        )
        
        # Tipo de acessórios
        acessorios = st.selectbox(
            "🔧 Tipo de Acessórios",
            options=['comum', 'premium'],
            format_func=lambda x: x.title()
        )
        
        # Complexidade do projeto
        complexidade = st.selectbox(
            "⚡ Complexidade",
            options=['simples', 'media', 'complexa', 'premium'],
            index=1,
            format_func=lambda x: x.replace('_', ' ').title()
        )
        
        # Margem de lucro
        margem_lucro = st.slider(
            "💰 Margem de Lucro (%)",
            min_value=10,
            max_value=50,
            value=30,
            step=5
        )
        
        # Preços atuais da Léo Madeiras
        st.markdown("---")
        st.markdown("### 💲 Preços Atuais")
        st.caption("🔗 Fonte: [Léo Madeiras](https://www.leomadeiras.com.br/)")
        st.caption("📅 Atualizado em 30/06/2025")
        
        for mat, info in Config.PRECOS_MATERIAIS.items():
            st.markdown(f"**{mat}:** R$ {info['preco_m2']:.2f}/m²")
    
    # Área principal
    st.markdown("### 📁 Upload do Projeto 3D")
    
    # Informações do projeto
    col1, col2 = st.columns(2)
    
    with col1:
        cliente = st.text_input("👤 Nome do Cliente", placeholder="Ex: João Silva")
    
    with col2:
        ambiente = st.text_input("🏠 Ambiente", placeholder="Ex: Cozinha, Banheiro, Quarto")
    
    # Upload de arquivo
    uploaded_file = st.file_uploader(
        "📎 Selecione o arquivo 3D",
        type=['obj', 'dae', 'stl', 'ply'],
        help=f"Formatos suportados: {', '.join(file_analyzer.supported_formats).upper()}"
    )
    
    if uploaded_file and cliente and ambiente:
        # Botão para analisar
        if st.button("🚀 Analisar Projeto", type="primary", use_container_width=True):
            with st.spinner("🔍 Analisando arquivo 3D..."):
                # Analisar arquivo
                analise = file_analyzer.analyze_file(uploaded_file)
                
                if analise:
                    # Incrementar contador de projetos
                    auth_manager.increment_project_count(usuario['id'])
                    
                    # Configurações do orçamento
                    configuracoes = {
                        'material': material,
                        'acessorios': acessorios,
                        'complexidade': complexidade,
                        'margem_lucro': margem_lucro
                    }
                    
                    # Calcular orçamento
                    with st.spinner("💰 Calculando orçamento..."):
                        orcamento = orcamento_engine.calcular_orcamento(analise, configuracoes)
                    
                    if orcamento:
                        # Salvar no session state
                        st.session_state.analise = analise
                        st.session_state.orcamento = orcamento
                        st.session_state.cliente = cliente
                        st.session_state.ambiente = ambiente
                        
                        st.success("✅ Análise concluída com sucesso!")
                        st.rerun()
    
    # Mostrar resultados se disponíveis
    if hasattr(st.session_state, 'orcamento') and st.session_state.orcamento:
        mostrar_resultados(
            st.session_state.analise,
            st.session_state.orcamento,
            st.session_state.cliente,
            st.session_state.ambiente,
            orcamento_engine
        )

def mostrar_resultados(analise: Dict, orcamento: Dict, cliente: str, ambiente: str, orcamento_engine: OrcamentoEngine):
    """Mostra resultados da análise e orçamento"""
    
    st.markdown("---")
    
    # Tabs para diferentes visualizações
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Resumo", "🧩 Componentes", "📈 Gráficos", "📄 Relatório"])
    
    with tab1:
        st.markdown("### 📊 Resumo do Orçamento")
        
        resumo = orcamento['resumo']
        
        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "💰 Valor Total",
                f"R$ {resumo['total_final']:,.2f}",
                delta=f"R$ {resumo['preco_por_m2']:,.2f}/m²"
            )
        
        with col2:
            st.metric(
                "📐 Área Total",
                f"{resumo['area_total_m2']:.2f} m²",
                delta=f"{resumo['total_componentes']} componentes"
            )
        
        with col3:
            st.metric(
                "🔧 Material",
                f"R$ {resumo['custo_material']:,.2f}",
                delta=f"{(resumo['custo_material']/resumo['total_final']*100):.1f}%"
            )
        
        with col4:
            st.metric(
                "⚙️ Mão de Obra",
                f"R$ {resumo['custo_mao_obra']:,.2f}",
                delta=f"{(resumo['custo_mao_obra']/resumo['total_final']*100):.1f}%"
            )
        
        # Breakdown detalhado
        st.markdown("### 💸 Breakdown de Custos")
        
        breakdown_data = {
            'Item': ['Material', 'Acessórios', 'Corte/Usinagem', 'Mão de Obra', 'Margem'],
            'Valor (R$)': [
                resumo['custo_material'],
                resumo['custo_acessorios'],
                resumo['custo_corte'],
                resumo['custo_mao_obra'],
                resumo['valor_margem']
            ],
            'Percentual (%)': [
                round(resumo['custo_material']/resumo['total_final']*100, 1),
                round(resumo['custo_acessorios']/resumo['total_final']*100, 1),
                round(resumo['custo_corte']/resumo['total_final']*100, 1),
                round(resumo['custo_mao_obra']/resumo['total_final']*100, 1),
                round(resumo['valor_margem']/resumo['total_final']*100, 1)
            ]
        }
        
        st.dataframe(breakdown_data, use_container_width=True)
    
    with tab2:
        st.markdown("### 🧩 Detalhamento por Componente")
        
        for comp in orcamento['componentes']:
            with st.expander(f"🔹 {comp['nome']} - R$ {comp['custo_total']:,.2f}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Tipo:** {comp['tipo'].replace('_', ' ').title()}")
                    st.markdown(f"**Área:** {comp['area_m2']:.2f} m²")
                    st.markdown(f"**Material:** {comp['material']}")
                    st.markdown(f"**Preço/m²:** R$ {comp['preco_por_m2']:,.2f}")
                
                with col2:
                    st.markdown("**Custos:**")
                    st.markdown(f"• Material: R$ {comp['custo_material']:,.2f}")
                    st.markdown(f"• Acessórios: R$ {comp['custo_acessorios']:,.2f}")
                    st.markdown(f"• Corte: R$ {comp['custo_corte']:,.2f}")
                    st.markdown(f"**Total: R$ {comp['custo_total']:,.2f}**")
                
                if comp['acessorios_detalhados']:
                    st.markdown("**Acessórios:**")
                    for acessorio, info in comp['acessorios_detalhados'].items():
                        st.markdown(f"• {info['quantidade']}x {acessorio.replace('_', ' ').title()} @ R$ {info['preco_unitario']:.2f}")
    
    with tab3:
        st.markdown("### 📈 Visualizações")
        
        # Gerar gráficos
        graficos = orcamento_engine.gerar_graficos(orcamento)
        
        if graficos.get('pizza'):
            st.plotly_chart(graficos['pizza'], use_container_width=True)
        
        if graficos.get('barras'):
            st.plotly_chart(graficos['barras'], use_container_width=True)
        
        if graficos.get('area'):
            st.plotly_chart(graficos['area'], use_container_width=True)
    
    with tab4:
        st.markdown("### 📄 Relatório Detalhado")
        
        # Gerar relatório
        relatorio = orcamento_engine.gerar_relatorio_detalhado(orcamento, cliente, ambiente)
        
        # Mostrar relatório
        st.markdown(relatorio)
        
        # Botão para download
        st.download_button(
            label="📥 Baixar Relatório (JSON)",
            data=json.dumps({
                'cliente': cliente,
                'ambiente': ambiente,
                'analise': analise,
                'orcamento': orcamento
            }, indent=2, ensure_ascii=False),
            file_name=f"orcamento_{cliente.replace(' ', '_')}_{ambiente.replace(' ', '_')}.json",
            mime="application/json"
        )

if __name__ == "__main__":
    main()

