"""
Analisador de Arquivos 3D
"""

import streamlit as st
import io
from typing import Dict, List, Optional

class FileAnalyzer:
    def __init__(self):
        self.supported_formats = ['obj', 'dae', 'stl', 'ply']
    
    def analyze_file(self, uploaded_file) -> Optional[Dict]:
        """Analisa arquivo 3D uploadado"""
        if not uploaded_file:
            return None
        
        try:
            # Verificar extensão
            file_extension = uploaded_file.name.split('.')[-1].lower()
            if file_extension not in self.supported_formats:
                st.error(f"❌ Formato não suportado: {file_extension}")
                return None
            
            # Ler conteúdo do arquivo
            file_content = uploaded_file.read()
            file_size_mb = len(file_content) / (1024 * 1024)
            
            # Simular análise do arquivo (versão simplificada para teste)
            componentes = self._simulate_component_analysis(uploaded_file.name, file_size_mb)
            
            return {
                'nome_arquivo': uploaded_file.name,
                'tamanho_mb': round(file_size_mb, 2),
                'formato': file_extension.upper(),
                'componentes': componentes,
                'total_componentes': len(componentes),
                'area_total_m2': sum(comp['area_m2'] for comp in componentes),
                'status': 'sucesso'
            }
            
        except Exception as e:
            st.error(f"❌ Erro ao analisar arquivo: {e}")
            return None
    
    def _simulate_component_analysis(self, filename: str, file_size_mb: float) -> List[Dict]:
        """Simula análise de componentes baseada no arquivo"""
        
        # Determinar tipo de projeto baseado no nome do arquivo
        filename_lower = filename.lower()
        
        if 'cozinha' in filename_lower or 'kitchen' in filename_lower:
            return self._generate_kitchen_components()
        elif 'banheiro' in filename_lower or 'bathroom' in filename_lower:
            return self._generate_bathroom_components()
        elif 'quarto' in filename_lower or 'bedroom' in filename_lower:
            return self._generate_bedroom_components()
        elif 'escritorio' in filename_lower or 'office' in filename_lower:
            return self._generate_office_components()
        else:
            # Projeto genérico baseado no tamanho do arquivo
            if file_size_mb < 1:
                return self._generate_small_project()
            elif file_size_mb < 5:
                return self._generate_medium_project()
            else:
                return self._generate_large_project()
    
    def _generate_kitchen_components(self) -> List[Dict]:
        """Gera componentes típicos de cozinha"""
        return [
            {
                'id': 'armario_superior_1',
                'nome': 'Armário Superior Esquerdo',
                'tipo': 'armario_superior',
                'largura_cm': 80,
                'altura_cm': 70,
                'profundidade_cm': 35,
                'area_m2': 1.89,
                'material_sugerido': 'MDF 15mm',
                'acessorios': ['dobradica', 'dobradica', 'puxador']
            },
            {
                'id': 'armario_superior_2',
                'nome': 'Armário Superior Central',
                'tipo': 'armario_superior',
                'largura_cm': 120,
                'altura_cm': 70,
                'profundidade_cm': 35,
                'area_m2': 2.73,
                'material_sugerido': 'MDF 15mm',
                'acessorios': ['dobradica', 'dobradica', 'dobradica', 'dobradica', 'puxador', 'puxador']
            },
            {
                'id': 'armario_inferior_1',
                'nome': 'Armário Inferior com Gavetas',
                'tipo': 'armario_inferior',
                'largura_cm': 60,
                'altura_cm': 85,
                'profundidade_cm': 55,
                'area_m2': 2.15,
                'material_sugerido': 'MDF 18mm',
                'acessorios': ['corredicao', 'corredicao', 'corredicao', 'puxador', 'puxador', 'puxador']
            },
            {
                'id': 'bancada',
                'nome': 'Bancada Principal',
                'tipo': 'bancada',
                'largura_cm': 240,
                'altura_cm': 4,
                'profundidade_cm': 60,
                'area_m2': 1.44,
                'material_sugerido': 'Melamina 15mm',
                'acessorios': []
            }
        ]
    
    def _generate_bathroom_components(self) -> List[Dict]:
        """Gera componentes típicos de banheiro"""
        return [
            {
                'id': 'gabinete_pia',
                'nome': 'Gabinete da Pia',
                'tipo': 'gabinete',
                'largura_cm': 80,
                'altura_cm': 60,
                'profundidade_cm': 45,
                'area_m2': 1.68,
                'material_sugerido': 'MDF 18mm',
                'acessorios': ['dobradica', 'dobradica', 'puxador']
            },
            {
                'id': 'espelheira',
                'nome': 'Espelheira com Porta',
                'tipo': 'espelheira',
                'largura_cm': 60,
                'altura_cm': 70,
                'profundidade_cm': 15,
                'area_m2': 0.84,
                'material_sugerido': 'MDF 15mm',
                'acessorios': ['dobradica', 'puxador']
            }
        ]
    
    def _generate_bedroom_components(self) -> List[Dict]:
        """Gera componentes típicos de quarto"""
        return [
            {
                'id': 'guarda_roupa',
                'nome': 'Guarda-Roupa 6 Portas',
                'tipo': 'guarda_roupa',
                'largura_cm': 270,
                'altura_cm': 220,
                'profundidade_cm': 60,
                'area_m2': 8.45,
                'material_sugerido': 'MDF 18mm',
                'acessorios': ['dobradica'] * 12 + ['puxador'] * 6
            },
            {
                'id': 'comoda',
                'nome': 'Cômoda 4 Gavetas',
                'tipo': 'comoda',
                'largura_cm': 120,
                'altura_cm': 80,
                'profundidade_cm': 45,
                'area_m2': 2.88,
                'material_sugerido': 'MDF 15mm',
                'acessorios': ['corredicao'] * 4 + ['puxador'] * 4
            }
        ]
    
    def _generate_office_components(self) -> List[Dict]:
        """Gera componentes típicos de escritório"""
        return [
            {
                'id': 'mesa_escritorio',
                'nome': 'Mesa de Escritório',
                'tipo': 'mesa',
                'largura_cm': 150,
                'altura_cm': 75,
                'profundidade_cm': 70,
                'area_m2': 1.05,
                'material_sugerido': 'MDF 18mm',
                'acessorios': []
            },
            {
                'id': 'estante_livros',
                'nome': 'Estante para Livros',
                'tipo': 'estante',
                'largura_cm': 80,
                'altura_cm': 180,
                'profundidade_cm': 30,
                'area_m2': 3.24,
                'material_sugerido': 'MDF 15mm',
                'acessorios': []
            }
        ]
    
    def _generate_small_project(self) -> List[Dict]:
        """Projeto pequeno genérico"""
        return [
            {
                'id': 'componente_1',
                'nome': 'Prateleira Simples',
                'tipo': 'prateleira',
                'largura_cm': 80,
                'altura_cm': 20,
                'profundidade_cm': 25,
                'area_m2': 0.60,
                'material_sugerido': 'MDF 15mm',
                'acessorios': []
            }
        ]
    
    def _generate_medium_project(self) -> List[Dict]:
        """Projeto médio genérico"""
        return [
            {
                'id': 'armario_1',
                'nome': 'Armário Padrão',
                'tipo': 'armario',
                'largura_cm': 100,
                'altura_cm': 200,
                'profundidade_cm': 50,
                'area_m2': 4.50,
                'material_sugerido': 'MDF 18mm',
                'acessorios': ['dobradica', 'dobradica', 'puxador']
            },
            {
                'id': 'prateleira_1',
                'nome': 'Prateleira Interna',
                'tipo': 'prateleira',
                'largura_cm': 95,
                'altura_cm': 2,
                'profundidade_cm': 45,
                'area_m2': 0.43,
                'material_sugerido': 'MDF 15mm',
                'acessorios': []
            }
        ]
    
    def _generate_large_project(self) -> List[Dict]:
        """Projeto grande genérico"""
        return [
            {
                'id': 'modulo_1',
                'nome': 'Módulo Principal',
                'tipo': 'modulo',
                'largura_cm': 200,
                'altura_cm': 220,
                'profundidade_cm': 60,
                'area_m2': 7.20,
                'material_sugerido': 'MDF 18mm',
                'acessorios': ['dobradica'] * 6 + ['puxador'] * 3
            },
            {
                'id': 'modulo_2',
                'nome': 'Módulo Secundário',
                'tipo': 'modulo',
                'largura_cm': 150,
                'altura_cm': 180,
                'profundidade_cm': 45,
                'area_m2': 4.05,
                'material_sugerido': 'MDF 15mm',
                'acessorios': ['dobradica'] * 4 + ['puxador'] * 2
            },
            {
                'id': 'bancada_integrada',
                'nome': 'Bancada Integrada',
                'tipo': 'bancada',
                'largura_cm': 350,
                'altura_cm': 4,
                'profundidade_cm': 60,
                'area_m2': 2.10,
                'material_sugerido': 'Melamina 15mm',
                'acessorios': []
            }
        ]
    
    def show_analysis_results(self, analise: Dict):
        """Exibe resultados da análise"""
        if not analise:
            return
        
        st.markdown("### 📊 Análise do Arquivo 3D")
        
        # Informações do arquivo
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📁 Arquivo", analise['nome_arquivo'])
        
        with col2:
            st.metric("📏 Tamanho", f"{analise['tamanho_mb']} MB")
        
        with col3:
            st.metric("🔧 Componentes", analise['total_componentes'])
        
        with col4:
            st.metric("📐 Área Total", f"{analise['area_total_m2']:.2f} m²")
        
        # Detalhes dos componentes
        st.markdown("### 🧩 Componentes Identificados")
        
        for i, comp in enumerate(analise['componentes']):
            with st.expander(f"🔹 {comp['nome']} - {comp['area_m2']:.2f} m²"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Tipo:** {comp['tipo'].replace('_', ' ').title()}")
                    st.markdown(f"**Material:** {comp['material_sugerido']}")
                    st.markdown(f"**Dimensões:** {comp['largura_cm']}×{comp['altura_cm']}×{comp['profundidade_cm']} cm")
                
                with col2:
                    st.markdown(f"**Área:** {comp['area_m2']:.2f} m²")
                    if comp['acessorios']:
                        acessorios_count = {}
                        for acessorio in comp['acessorios']:
                            acessorios_count[acessorio] = acessorios_count.get(acessorio, 0) + 1
                        
                        st.markdown("**Acessórios:**")
                        for acessorio, qtd in acessorios_count.items():
                            st.markdown(f"• {qtd}x {acessorio.replace('_', ' ').title()}")
                    else:
                        st.markdown("**Acessórios:** Nenhum")

