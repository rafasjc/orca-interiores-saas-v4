"""
Engine de Orçamento Profissional
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from typing import Dict, List
from config import Config

class OrcamentoEngine:
    def __init__(self):
        self.config = Config()
    
    def calcular_orcamento(self, analise: Dict, configuracoes: Dict) -> Dict:
        """Calcula orçamento completo baseado na análise"""
        if not analise or not analise.get('componentes'):
            return {}
        
        try:
            # Calcular custos por componente
            componentes_detalhados = []
            custo_total_material = 0
            custo_total_acessorios = 0
            custo_total_corte = 0
            
            for comp in analise['componentes']:
                detalhes = self._calcular_componente(comp, configuracoes)
                componentes_detalhados.append(detalhes)
                
                custo_total_material += detalhes['custo_material']
                custo_total_acessorios += detalhes['custo_acessorios']
                custo_total_corte += detalhes['custo_corte']
            
            # Calcular totais
            subtotal = custo_total_material + custo_total_acessorios + custo_total_corte
            
            # Aplicar margem de lucro
            margem = configuracoes.get('margem_lucro', 30) / 100
            valor_margem = subtotal * margem
            
            # Calcular mão de obra (baseado na complexidade)
            complexidade = configuracoes.get('complexidade', 'media')
            percentual_mao_obra = {
                'simples': 0.20,
                'media': 0.35,
                'complexa': 0.50,
                'premium': 0.70
            }.get(complexidade, 0.35)
            
            custo_mao_obra = subtotal * percentual_mao_obra
            
            # Total final
            total_final = subtotal + valor_margem + custo_mao_obra
            
            return {
                'componentes': componentes_detalhados,
                'resumo': {
                    'area_total_m2': analise['area_total_m2'],
                    'total_componentes': len(componentes_detalhados),
                    'custo_material': custo_total_material,
                    'custo_acessorios': custo_total_acessorios,
                    'custo_corte': custo_total_corte,
                    'subtotal': subtotal,
                    'custo_mao_obra': custo_mao_obra,
                    'valor_margem': valor_margem,
                    'total_final': total_final,
                    'preco_por_m2': total_final / analise['area_total_m2'] if analise['area_total_m2'] > 0 else 0
                },
                'configuracoes': configuracoes,
                'data_orcamento': datetime.now().isoformat(),
                'fonte_precos': 'Léo Madeiras - Atualizado em 30/06/2025'
            }
            
        except Exception as e:
            st.error(f"Erro ao calcular orçamento: {e}")
            return {}
    
    def _calcular_componente(self, componente: Dict, configuracoes: Dict) -> Dict:
        """Calcula custo de um componente específico"""
        # Obter preços do material
        material = configuracoes.get('material', 'MDF 15mm')
        info_material = Config.PRECOS_MATERIAIS.get(material, Config.PRECOS_MATERIAIS['MDF 15mm'])
        
        # Calcular área com desperdício
        area_base = componente['area_m2']
        desperdicio = info_material['desperdicio']
        area_com_desperdicio = area_base * (1 + desperdicio)
        
        # Custo do material
        custo_material = area_com_desperdicio * info_material['preco_m2']
        
        # Calcular acessórios
        tipo_acessorio = configuracoes.get('acessorios', 'comum')
        precos_acessorios = Config.PRECOS_ACESSORIOS.get(tipo_acessorio, Config.PRECOS_ACESSORIOS['comum'])
        
        custo_acessorios = 0
        acessorios_detalhados = {}
        
        for acessorio in componente.get('acessorios', []):
            preco_unitario = precos_acessorios.get(acessorio, 0)
            custo_acessorios += preco_unitario
            
            if acessorio in acessorios_detalhados:
                acessorios_detalhados[acessorio]['quantidade'] += 1
                acessorios_detalhados[acessorio]['custo_total'] += preco_unitario
            else:
                acessorios_detalhados[acessorio] = {
                    'quantidade': 1,
                    'preco_unitario': preco_unitario,
                    'custo_total': preco_unitario
                }
        
        # Calcular custo de corte
        custo_corte = self._calcular_custo_corte(componente)
        
        # Total do componente
        custo_total = custo_material + custo_acessorios + custo_corte
        
        return {
            'id': componente['id'],
            'nome': componente['nome'],
            'tipo': componente['tipo'],
            'area_m2': area_base,
            'area_com_desperdicio': area_com_desperdicio,
            'material': material,
            'custo_material': custo_material,
            'custo_acessorios': custo_acessorios,
            'custo_corte': custo_corte,
            'custo_total': custo_total,
            'acessorios_detalhados': acessorios_detalhados,
            'preco_por_m2': custo_total / area_base if area_base > 0 else 0
        }
    
    def _calcular_custo_corte(self, componente: Dict) -> float:
        """Calcula custo de corte baseado no componente"""
        # Estimar metros lineares de corte baseado nas dimensões
        largura_m = componente['largura_cm'] / 100
        altura_m = componente['altura_cm'] / 100
        profundidade_m = componente['profundidade_cm'] / 100
        
        # Perímetro aproximado para cortes
        perimetro = 2 * (largura_m + profundidade_m) + 2 * (altura_m + profundidade_m)
        
        # Custo por metro linear de corte
        custo_por_metro = 2.50
        
        # Furos para acessórios
        num_furos = len([a for a in componente.get('acessorios', []) if a in ['dobradica', 'fechadura']])
        custo_furos = num_furos * 1.50
        
        # Taxa mínima por peça
        taxa_minima = 15.00
        
        custo_total = max(perimetro * custo_por_metro + custo_furos, taxa_minima)
        
        return custo_total
    
    def gerar_graficos(self, orcamento: Dict) -> Dict:
        """Gera gráficos para visualização"""
        if not orcamento or not orcamento.get('resumo'):
            return {}
        
        resumo = orcamento['resumo']
        
        # Gráfico de pizza - Distribuição de custos
        labels = ['Material', 'Acessórios', 'Corte/Usinagem', 'Mão de Obra', 'Margem']
        values = [
            resumo['custo_material'],
            resumo['custo_acessorios'],
            resumo['custo_corte'],
            resumo['custo_mao_obra'],
            resumo['valor_margem']
        ]
        
        fig_pizza = px.pie(
            values=values,
            names=labels,
            title="Distribuição de Custos",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        
        # Gráfico de barras - Custo por componente
        componentes = orcamento.get('componentes', [])
        if componentes:
            nomes = [comp['nome'] for comp in componentes]
            custos = [comp['custo_total'] for comp in componentes]
            
            fig_barras = px.bar(
                x=nomes,
                y=custos,
                title="Custo por Componente",
                labels={'x': 'Componentes', 'y': 'Custo (R$)'},
                color=custos,
                color_continuous_scale='viridis'
            )
            fig_barras.update_xaxis(tickangle=45)
        else:
            fig_barras = None
        
        # Gráfico de área - Custo por m²
        if componentes:
            areas = [comp['area_m2'] for comp in componentes]
            precos_m2 = [comp['preco_por_m2'] for comp in componentes]
            
            fig_area = px.scatter(
                x=areas,
                y=precos_m2,
                size=[comp['custo_total'] for comp in componentes],
                hover_name=nomes,
                title="Custo por m² vs Área",
                labels={'x': 'Área (m²)', 'y': 'Preço por m² (R$)'},
                color=custos,
                color_continuous_scale='plasma'
            )
        else:
            fig_area = None
        
        return {
            'pizza': fig_pizza,
            'barras': fig_barras,
            'area': fig_area
        }
    
    def gerar_relatorio_detalhado(self, orcamento: Dict, cliente: str, ambiente: str) -> str:
        """Gera relatório detalhado em texto"""
        if not orcamento:
            return ""
        
        resumo = orcamento['resumo']
        data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        relatorio = f"""
# 📋 ORÇAMENTO DETALHADO - ORÇA INTERIORES

**Data:** {data_atual}
**Cliente:** {cliente}
**Ambiente:** {ambiente}

---

## 📊 RESUMO EXECUTIVO

• **Área Total:** {resumo['area_total_m2']:.2f} m²
• **Total de Componentes:** {resumo['total_componentes']}
• **Valor Total:** R$ {resumo['total_final']:,.2f}
• **Preço por m²:** R$ {resumo['preco_por_m2']:,.2f}

---

## 💰 BREAKDOWN DE CUSTOS

| Item | Valor | Percentual |
|------|-------|------------|
| Material | R$ {resumo['custo_material']:,.2f} | {(resumo['custo_material']/resumo['total_final']*100):.1f}% |
| Acessórios | R$ {resumo['custo_acessorios']:,.2f} | {(resumo['custo_acessorios']/resumo['total_final']*100):.1f}% |
| Corte/Usinagem | R$ {resumo['custo_corte']:,.2f} | {(resumo['custo_corte']/resumo['total_final']*100):.1f}% |
| Mão de Obra | R$ {resumo['custo_mao_obra']:,.2f} | {(resumo['custo_mao_obra']/resumo['total_final']*100):.1f}% |
| Margem | R$ {resumo['valor_margem']:,.2f} | {(resumo['valor_margem']/resumo['total_final']*100):.1f}% |

**TOTAL:** R$ {resumo['total_final']:,.2f}

---

## 🧩 DETALHAMENTO POR COMPONENTE

"""
        
        for comp in orcamento.get('componentes', []):
            relatorio += f"""
### {comp['nome']}

• **Tipo:** {comp['tipo'].replace('_', ' ').title()}
• **Área:** {comp['area_m2']:.2f} m²
• **Material:** {comp['material']}
• **Custo Total:** R$ {comp['custo_total']:,.2f}

**Breakdown:**
- Material: R$ {comp['custo_material']:,.2f}
- Acessórios: R$ {comp['custo_acessorios']:,.2f}
- Corte: R$ {comp['custo_corte']:,.2f}

"""
            
            if comp['acessorios_detalhados']:
                relatorio += "**Acessórios:**\n"
                for acessorio, info in comp['acessorios_detalhados'].items():
                    relatorio += f"- {info['quantidade']}x {acessorio.replace('_', ' ').title()} @ R$ {info['preco_unitario']:.2f} = R$ {info['custo_total']:.2f}\n"
            
            relatorio += "\n---\n"
        
        relatorio += f"""

## ⚙️ CONFIGURAÇÕES UTILIZADAS

• **Material Principal:** {orcamento['configuracoes'].get('material', 'MDF 15mm')}
• **Tipo de Acessórios:** {orcamento['configuracoes'].get('acessorios', 'Comum').title()}
• **Complexidade:** {orcamento['configuracoes'].get('complexidade', 'Média').title()}
• **Margem de Lucro:** {orcamento['configuracoes'].get('margem_lucro', 30)}%

---

## 📝 OBSERVAÇÕES

• Preços baseados na tabela da Léo Madeiras (atualizada em 30/06/2025)
• Valores incluem desperdício de material conforme padrão da indústria
• Mão de obra calculada baseada na complexidade do projeto
• Orçamento válido por 30 dias
• Não inclui entrega e instalação

---

**Orçamento gerado pelo sistema Orça Interiores SaaS**
*Sistema Profissional de Orçamento de Marcenaria*
"""
        
        return relatorio

