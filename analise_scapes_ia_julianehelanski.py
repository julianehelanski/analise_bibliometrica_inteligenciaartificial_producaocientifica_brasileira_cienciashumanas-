"""
================================================================================
ANÁLISE COMPLETA - CATÁLOGO DE TESES CAPES SOBRE INTELIGÊNCIA ARTIFICIAL
================================================================================

VERSÃO 2.0 - GRÁFICOS INDIVIDUAIS COM FUNDO BRANCO

INSTRUÇÕES DE USO:
1. Salve este arquivo como: analise_teses_ia_v2.py
2. Coloque o arquivo "catalogo_teses_analise.xlsx" na MESMA pasta
3. Abra no Spyder ou execute: python analise_teses_ia_v2.py
4. Os gráficos serão exibidos UM POR VEZ (pressione Enter para próximo)
5. Todos os gráficos são salvos automaticamente

REQUISITOS:
pip install pandas numpy matplotlib seaborn openpyxl

NOVIDADES DESTA VERSÃO:
✓ Fundo branco em todos os gráficos
✓ Cada gráfico é exibido individualmente
✓ Maior qualidade visual
✓ Melhor para apresentações

================================================================================
"""

# =============================================================================
# IMPORTAÇÕES
# =============================================================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re
import os
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# CONFIGURAÇÕES DE VISUALIZAÇÃO - FUNDO BRANCO
# =============================================================================
plt.style.use('default')  # Estilo padrão (fundo branco)
sns.set_style("whitegrid")  # Grade sutil com fundo branco
sns.set_palette("husl")

# Configurar todos os fundos como branco
plt.rcParams['figure.figsize'] = (12, 7)
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['savefig.facecolor'] = 'white'
plt.rcParams['savefig.edgecolor'] = 'none'
plt.rcParams['figure.dpi'] = 100
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 13
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titleweight'] = 'bold'

print("="*80)
print("ANÁLISE DO CATÁLOGO DE TESES CAPES - INTELIGÊNCIA ARTIFICIAL")
print("="*80)
print("\nVERSÃO 2.0 - Gráficos Individuais com Fundo Branco")
print("="*80)

# =============================================================================
# 1. CARREGAR DADOS
# =============================================================================
print("\n[1/10] Carregando dados...")

if not os.path.exists('catalogo_teses_analise.xlsx'):
    print("\n❌ ERRO: Arquivo 'catalogo_teses_analise.xlsx' não encontrado!")
    print("   Certifique-se que o arquivo está na mesma pasta deste script.")
    exit()

df = pd.read_excel('catalogo_teses_analise.xlsx', sheet_name='Dados Completos')

# 🔧 LIMPEZA: Remover linhas de cabeçalho duplicadas
df = df[df['id'] != 'col-md-1'].copy()
df = df[df['titulo'].notna()].copy()
df = df[df['autor'].notna()].copy()

df['area_normalizada'] = df['area'].str.upper().str.strip()
df['decada'] = (df['ano_defesa'] // 10 * 10).astype('Int64')

print(f"✓ {len(df)} publicações carregadas (IDs 1-100)")
print(f"✓ Período: {int(df['ano_defesa'].min())}-{int(df['ano_defesa'].max())}")

# =============================================================================
# 2. CLASSIFICAÇÃO POR FOCO EM IA
# =============================================================================
print("\n[2/10] Classificando por foco em IA...")

keywords_ia_forte = [
    'inteligência artificial', 'ia ', 'artificial intelligence',
    'machine learning', 'deep learning', 'redes neurais', 'neural networks',
    'aprendizado de máquina', 'algoritmo', 'chatbot', 'gpt', 'llm'
]

keywords_ia_relacionada = [
    'transhumanismo', 'robótica', 'automação', 'digitalização',
    'tecnologia digital', 'computacional', 'dados', 'big data',
    'internet', 'online', 'virtual', 'cibernético'
]

def classificar_foco_ia(titulo):
    if pd.isna(titulo):
        return 'Outros Temas'
    titulo_lower = titulo.lower()
    for keyword in keywords_ia_forte:
        if keyword in titulo_lower:
            return 'IA - Foco Central'
    for keyword in keywords_ia_relacionada:
        if keyword in titulo_lower:
            return 'IA - Foco Relacionado'
    return 'Outros Temas'

df['foco_ia'] = df['titulo'].apply(classificar_foco_ia)
foco_counts = df['foco_ia'].value_counts()

print("✓ Classificação concluída:")
for foco, count in foco_counts.items():
    print(f"  - {foco}: {count} ({count/len(df)*100:.1f}%)")

# =============================================================================
# 3. ANÁLISE TEMPORAL
# =============================================================================
print("\n[3/10] Analisando tendências temporais...")

pub_por_ano = df.groupby('ano_defesa').size().reset_index(name='quantidade')
pub_por_ano['ano_defesa'] = pub_por_ano['ano_defesa'].astype(int)
pub_por_ano = pub_por_ano.sort_values('ano_defesa')

anos_recentes = pub_por_ano[pub_por_ano['ano_defesa'] >= 2020]['quantidade'].sum()
crescimento = ((pub_por_ano.iloc[-1]['quantidade'] - pub_por_ano.iloc[0]['quantidade']) / 
               pub_por_ano.iloc[0]['quantidade'] * 100)

print(f"✓ Crescimento: {crescimento:.0f}% (2013→2023)")
print(f"✓ Últimos 3 anos: {anos_recentes} publicações ({anos_recentes/len(df)*100:.1f}%)")

# =============================================================================
# 4. ANÁLISE POR NÍVEL
# =============================================================================
print("\n[4/10] Analisando nível acadêmico...")

nivel_counts = df['nivel'].value_counts()
nivel_ano = df.groupby(['ano_defesa', 'nivel']).size().unstack(fill_value=0)

print(f"✓ Mestrados: {nivel_counts.get('Mestrado', 0)} ({nivel_counts.get('Mestrado', 0)/len(df)*100:.1f}%)")
print(f"✓ Doutorados: {nivel_counts.get('Doutorado', 0)} ({nivel_counts.get('Doutorado', 0)/len(df)*100:.1f}%)")

# =============================================================================
# 5. TOP 10 ÁREAS
# =============================================================================
print("\n[5/10] Identificando top 10 áreas...")

area_counts = df['area_normalizada'].value_counts()
top10_areas = area_counts.head(10)

print("✓ Top 3 áreas:")
for i, (area, count) in enumerate(top10_areas.head(3).items(), 1):
    print(f"  {i}. {area}: {count} ({count/len(df)*100:.1f}%)")

# =============================================================================
# 6. OUTRAS ÁREAS
# =============================================================================
print("\n[6/10] Analisando áreas fora do top 10...")

outras_areas = area_counts[10:]
print(f"✓ {len(outras_areas)} áreas diferentes")
print(f"✓ {outras_areas.sum()} publicações ({outras_areas.sum()/len(df)*100:.1f}%)")

# =============================================================================
# 7. TOP 10 INSTITUIÇÕES
# =============================================================================
print("\n[7/10] Identificando top 10 instituições...")

inst_counts = df['instituicao'].value_counts()
top10_inst = inst_counts.head(10)

print("✓ Top 3 instituições:")
for i, (inst, count) in enumerate(top10_inst.head(3).items(), 1):
    print(f"  {i}. {inst}: {count} ({count/len(df)*100:.1f}%)")

# =============================================================================
# 8. TIPO DE INSTITUIÇÃO
# =============================================================================
print("\n[8/10] Classificando tipo de instituição...")

def classificar_instituicao(nome):
    """Classifica instituições por tipo - VERSÃO CORRIGIDA"""
    if pd.isna(nome):
        return 'Não especificado'
    
    nome_upper = str(nome).upper()
    
    # ⭐ CASOS ESPECIAIS - Instituições Federais sem "FEDERAL" no nome
    federais_especiais = [
        'UNIVERSIDADE DE BRASÍLIA',
        'FUNDACAO GETULIO VARGAS'
    ]
    for fed in federais_especiais:
        if fed in nome_upper:
            return 'Federal'
    
    # ⭐ CASOS ESPECIAIS - Instituições Estaduais sem "ESTADUAL" no nome
    estaduais_especiais = [
        'UNIVERSIDADE DE SÃO PAULO',
        'UNIVERSIDADE DO ESTADO DO RIO DE JANEIRO'
    ]
    for est in estaduais_especiais:
        if est in nome_upper:
            return 'Estadual'
    
    # Classificação padrão por palavras-chave
    if 'FEDERAL' in nome_upper or 'CEFET' in nome_upper:
        return 'Federal'
    elif 'ESTADUAL' in nome_upper:
        return 'Estadual'
    elif 'MUNICIPAL' in nome_upper:
        return 'Municipal'
    elif 'PONTIFÍCIA' in nome_upper or 'CATÓLICA' in nome_upper or 'METODISTA' in nome_upper:
        return 'Confessional'
    else:
        return 'Particular/Comunitária'

df['tipo_instituicao'] = df['instituicao'].apply(classificar_instituicao)
tipo_counts = df['tipo_instituicao'].value_counts()

print("✓ Distribuição por tipo (CORRIGIDA):")
for tipo, count in tipo_counts.items():
    print(f"  - {tipo}: {count} ({count/len(df)*100:.1f}%)")

# =============================================================================
# 9. ANÁLISE DE TERMOS-CHAVE
# =============================================================================
print("\n[9/10] Extraindo termos-chave dos títulos...")

stopwords = {'de', 'da', 'do', 'e', 'a', 'o', 'em', 'para', 'com', 'por', 
             'uma', 'um', 'as', 'os', 'na', 'no', 'à', 'ao', 'dos', 'das'}

todos_termos = []
for titulo in df['titulo'].dropna():
    termos = re.findall(r'\b[a-záàâãéèêíïóôõöúçñA-ZÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ]+\b', titulo.lower())
    termos_filtrados = [t for t in termos if len(t) > 3 and t not in stopwords]
    todos_termos.extend(termos_filtrados)

termo_counts = Counter(todos_termos)
top_termos = termo_counts.most_common(10)

print("✓ Top 5 termos:")
for termo, count in top_termos[:5]:
    print(f"  - {termo}: {count}")

# =============================================================================
# 10. GERAR VISUALIZAÇÕES INDIVIDUAIS
# =============================================================================
print("\n[10/10] Gerando visualizações individuais...")
print("\n" + "="*80)
print("Os gráficos serão exibidos um por vez.")
print("Feche a janela ou pressione 'q' para ir ao próximo gráfico.")
print("="*80 + "\n")

# Criar pasta para salvar gráficos
if not os.path.exists('graficos'):
    os.makedirs('graficos')

# GRÁFICO 1: Distribuição Temporal
print("📊 Gráfico 1/9: Distribuição de Publicações por Ano")
fig, ax = plt.subplots(figsize=(12, 7), facecolor='white')
ax.plot(pub_por_ano['ano_defesa'], pub_por_ano['quantidade'], 
        marker='o', linewidth=3, markersize=10, color='#2E86AB')
ax.fill_between(pub_por_ano['ano_defesa'], pub_por_ano['quantidade'], alpha=0.2, color='#2E86AB')

# Título com informações
n_anos = len(pub_por_ano)
ax.set_title(f'Distribuição de Publicações por Ano\nTotal: {len(df)} publicações | Período: {n_anos} anos ({int(pub_por_ano["ano_defesa"].min())}-{int(pub_por_ano["ano_defesa"].max())})', 
             fontweight='bold', fontsize=13, pad=20)
ax.set_xlabel('Ano', fontsize=12)
ax.set_ylabel('Número de Publicações', fontsize=12)
ax.grid(True, alpha=0.3, linestyle='--')
ax.set_facecolor('white')
for i, row in pub_por_ano.iterrows():
    ax.text(row['ano_defesa'], row['quantidade'] + 0.5, str(row['quantidade']), 
            ha='center', va='bottom', fontweight='bold', fontsize=9)
plt.tight_layout()
plt.savefig('graficos/01_distribuicao_temporal.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.show()

# GRÁFICO 2: Foco em IA
print("\n📊 Gráfico 2/9: Distribuição por Foco em IA")
fig, ax = plt.subplots(figsize=(12, 7), facecolor='white')
colors_foco = ['#E63946', '#F77F00', '#06A77D']
bars = ax.bar(range(len(foco_counts)), foco_counts.values, color=colors_foco, edgecolor='black', linewidth=1.5)
ax.set_xticks(range(len(foco_counts)))
ax.set_xticklabels(foco_counts.index, fontsize=11)

# Título com informações
n_categorias = len(foco_counts)
ax.set_title(f'Distribuição por Foco em IA\nTotal: {len(df)} publicações | {n_categorias} categorias de foco', 
             fontweight='bold', fontsize=13, pad=20)
ax.set_ylabel('Quantidade', fontsize=12)
ax.set_facecolor('white')
ax.grid(True, alpha=0.3, axis='y', linestyle='--')
for i, (bar, v) in enumerate(zip(bars, foco_counts.values)):
    pct = (v/len(df))*100
    ax.text(bar.get_x() + bar.get_width()/2, v + 1.5, f'{v}\n({pct:.1f}%)', 
            ha='center', fontweight='bold', fontsize=11)
plt.tight_layout()
plt.savefig('graficos/02_foco_ia.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.show()

# GRÁFICO 3: Nível Acadêmico (Pizza)
print("\n📊 Gráfico 3/9: Distribuição por Nível Acadêmico")
fig, ax = plt.subplots(figsize=(10, 8), facecolor='white')
colors_nivel = ['#06A77D', '#005377']
wedges, texts, autotexts = ax.pie(nivel_counts.values, labels=nivel_counts.index, 
                                     autopct='%1.1f%%', startangle=90, colors=colors_nivel,
                                     textprops={'fontsize': 12, 'weight': 'bold'},
                                     explode=(0.05, 0.05))

# Título com informações
n_niveis = len(nivel_counts)
ax.set_title(f'Distribuição por Nível Acadêmico\nTotal: {len(df)} publicações ({nivel_counts.iloc[0]} Mestrados + {nivel_counts.iloc[1]} Doutorados)', 
             fontweight='bold', fontsize=13, pad=20)
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
    autotext.set_fontsize(13)
plt.tight_layout()
plt.savefig('graficos/03_nivel_academico.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.show()

# GRÁFICO 4: Top 10 Áreas
print("\n📊 Gráfico 4/9: Top 10 Áreas Temáticas")
fig, ax = plt.subplots(figsize=(12, 8), facecolor='white')
y_pos = np.arange(len(top10_areas))
bars = ax.barh(y_pos, top10_areas.values, color='#D62828', edgecolor='black', linewidth=1.5)
ax.set_yticks(y_pos)
ax.set_yticklabels(top10_areas.index, fontsize=11)
ax.invert_yaxis()

# Título com informações
total_areas = len(area_counts)
total_top10 = top10_areas.sum()
pct_top10 = (total_top10/len(df))*100
ax.set_title(f'Top 10 Áreas Temáticas (de {total_areas} áreas)\nTotal analisado: {len(df)} publicações | Top 10 representa: {total_top10} ({pct_top10:.1f}%)', 
             fontweight='bold', fontsize=13, pad=20)
ax.set_xlabel('Quantidade', fontsize=12)
ax.set_facecolor('white')
ax.grid(True, alpha=0.3, axis='x', linestyle='--')
for i, v in enumerate(top10_areas.values):
    pct = (v/len(df))*100
    ax.text(v + 0.5, i, f'{v} ({pct:.1f}%)', va='center', fontweight='bold', fontsize=10)
plt.tight_layout()
plt.savefig('graficos/04_top10_areas.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.show()

# GRÁFICO 5: Evolução Mestrado vs Doutorado
print("\n📊 Gráfico 5/9: Evolução de Mestrado vs Doutorado")
fig, ax = plt.subplots(figsize=(12, 7), facecolor='white')
nivel_ano.plot(kind='area', ax=ax, stacked=True, alpha=0.7, 
              color=['#06A77D', '#005377'], linewidth=2)

# Título com informações
total_mestrado = nivel_counts.get('Mestrado', 0)
total_doutorado = nivel_counts.get('Doutorado', 0)
ax.set_title(f'Evolução de Mestrado vs Doutorado ao Longo do Tempo\nTotal: {len(df)} publicações ({total_mestrado} Mestrados + {total_doutorado} Doutorados)', 
             fontweight='bold', fontsize=13, pad=20)
ax.set_xlabel('Ano', fontsize=12)
ax.set_ylabel('Quantidade', fontsize=12)
ax.legend(title='Nível', fontsize=11, title_fontsize=12)
ax.grid(True, alpha=0.3, linestyle='--')
ax.set_facecolor('white')
plt.tight_layout()
plt.savefig('graficos/05_evolucao_mestrado_doutorado.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.show()

# GRÁFICO 6: Top 10 Instituições
print("\n📊 Gráfico 6/9: Top 10 Instituições")
fig, ax = plt.subplots(figsize=(12, 8), facecolor='white')
y_pos = np.arange(len(top10_inst))
bars = ax.barh(y_pos, top10_inst.values, color='#F77F00', edgecolor='black', linewidth=1.5)
ax.set_yticks(y_pos)
labels = [inst[:45] + '...' if len(inst) > 45 else inst for inst in top10_inst.index]
ax.set_yticklabels(labels, fontsize=10)
ax.invert_yaxis()

# Título com informações
total_inst = len(inst_counts)
total_top10 = top10_inst.sum()
pct_top10 = (total_top10/len(df))*100
ax.set_title(f'Top 10 Instituições (de {total_inst} instituições)\nTotal analisado: {len(df)} publicações | Top 10 representa: {total_top10} ({pct_top10:.1f}%)', 
             fontweight='bold', fontsize=13, pad=20)
ax.set_xlabel('Quantidade', fontsize=12)
ax.set_facecolor('white')
ax.grid(True, alpha=0.3, axis='x', linestyle='--')
for i, v in enumerate(top10_inst.values):
    pct = (v/len(df))*100
    ax.text(v + 0.2, i, f'{v} ({pct:.1f}%)', va='center', fontweight='bold', fontsize=10)
plt.tight_layout()
plt.savefig('graficos/06_top10_instituicoes.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.show()

# GRÁFICO 7: Distribuição de Páginas
print("\n📊 Gráfico 7/9: Distribuição do Número de Páginas")
fig, ax = plt.subplots(figsize=(12, 7), facecolor='white')
paginas_limpo = df['num_paginas'].dropna()
ax.hist(paginas_limpo, bins=25, color='#118AB2', edgecolor='black', alpha=0.8, linewidth=1.5)

# Título com informações
n_com_paginas = len(paginas_limpo)
media = paginas_limpo.mean()
mediana = paginas_limpo.median()
ax.set_title(f'Distribuição do Número de Páginas\nTotal analisado: {n_com_paginas} publicações (de {len(df)}) | Média: {media:.0f} | Mediana: {mediana:.0f}', 
             fontweight='bold', fontsize=13, pad=20)
ax.set_xlabel('Número de Páginas', fontsize=12)
ax.set_ylabel('Frequência', fontsize=12)
ax.axvline(mediana, color='red', linestyle='--', linewidth=3, 
           label=f'Mediana: {mediana:.0f} páginas')
ax.legend(fontsize=11, loc='upper right')
ax.set_facecolor('white')
ax.grid(True, alpha=0.3, axis='y', linestyle='--')
plt.tight_layout()
plt.savefig('graficos/07_distribuicao_paginas.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.show()

# GRÁFICO 8: Tipo de Instituição
print("\n📊 Gráfico 8/9: Distribuição por Tipo de Instituição")
fig, ax = plt.subplots(figsize=(12, 7), facecolor='white')

# Ordenar por quantidade (decrescente)
tipo_counts_sorted = tipo_counts.sort_values(ascending=False)

colors_tipo = ['#06A77D', '#F18F01', '#C73E1D', '#A23B72', '#5E60CE']
bars = ax.bar(range(len(tipo_counts_sorted)), tipo_counts_sorted.values, 
              color=colors_tipo[:len(tipo_counts_sorted)], edgecolor='black', linewidth=1.5)
ax.set_xticks(range(len(tipo_counts_sorted)))
ax.set_xticklabels(tipo_counts_sorted.index, fontsize=11, rotation=15, ha='right')

# Título com informações
n_tipos = len(tipo_counts_sorted)
ax.set_title(f'Distribuição por Tipo de Instituição\nTotal: {len(df)} publicações | {n_tipos} tipos | Setor Público: {tipo_counts_sorted.get("Federal", 0) + tipo_counts_sorted.get("Estadual", 0)} ({(tipo_counts_sorted.get("Federal", 0) + tipo_counts_sorted.get("Estadual", 0))/len(df)*100:.1f}%)', 
             fontweight='bold', fontsize=13, pad=20)
ax.set_ylabel('Quantidade', fontsize=12)
ax.set_facecolor('white')
ax.grid(True, alpha=0.3, axis='y', linestyle='--')
for i, (bar, v) in enumerate(zip(bars, tipo_counts_sorted.values)):
    pct = (v/len(df))*100
    ax.text(bar.get_x() + bar.get_width()/2, v + 1, f'{v}\n({pct:.1f}%)', 
            ha='center', fontweight='bold', fontsize=10)
plt.tight_layout()
plt.savefig('graficos/08_tipo_instituicao.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.show()

# GRÁFICO 9: Evolução das Top 3 Áreas
print("\n📊 Gráfico 9/9: Evolução Temporal - Top 3 Áreas")
fig, ax = plt.subplots(figsize=(12, 7), facecolor='white')
top3_areas = top10_areas.head(3).index
colors_top3 = ['#E63946', '#F77F00', '#06A77D']
for i, (area, color) in enumerate(zip(top3_areas, colors_top3)):
    evolucao = df[df['area_normalizada'] == area].groupby('ano_defesa').size()
    ax.plot(evolucao.index, evolucao.values, marker='o', label=area, 
            linewidth=3, color=color, markersize=10)

# Título com informações
total_top3 = top10_areas.head(3).sum()
pct_top3 = (total_top3/len(df))*100
ax.set_title(f'Evolução Temporal - Top 3 Áreas Temáticas\nTotal das top 3: {total_top3} publicações ({pct_top3:.1f}% do total de {len(df)})', 
             fontweight='bold', fontsize=13, pad=20)
ax.set_xlabel('Ano', fontsize=12)
ax.set_ylabel('Publicações', fontsize=12)
ax.legend(fontsize=11, loc='upper left')
ax.grid(True, alpha=0.3, linestyle='--')
ax.set_facecolor('white')
plt.tight_layout()
plt.savefig('graficos/09_evolucao_top3_areas.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.show()

print("\n✅ Todos os 9 gráficos foram salvos na pasta 'graficos/'")
print("   Cada gráfico inclui informações contextuais sobre o total e categorias analisadas")

# =============================================================================
# 11. EXPORTAR RESULTADOS EM EXCEL
# =============================================================================
print("\n" + "="*80)
print("Exportando resultados detalhados...")
print("="*80)

output_excel = 'resultados_detalhados_teses_ia.xlsx'

with pd.ExcelWriter(output_excel, engine='openpyxl') as writer:
    resumo = pd.DataFrame({
        'Métrica': [
            'Total de Publicações', 'Período Analisado', 'Mestrados', 'Doutorados',
            'IA - Foco Central', 'IA - Foco Relacionado', 'Outros Temas',
            'Número de Áreas', 'Número de Instituições', 'Crescimento (%)',
            'Concentração Últimos 3 anos (%)'
        ],
        'Valor': [
            len(df), f"{int(df['ano_defesa'].min())} - {int(df['ano_defesa'].max())}",
            nivel_counts.get('Mestrado', 0), nivel_counts.get('Doutorado', 0),
            foco_counts.get('IA - Foco Central', 0), foco_counts.get('IA - Foco Relacionado', 0),
            foco_counts.get('Outros Temas', 0), len(area_counts), len(inst_counts),
            f"{crescimento:.0f}%", f"{anos_recentes/len(df)*100:.1f}%"
        ]
    })
    resumo.to_excel(writer, sheet_name='Resumo Geral', index=False)
    pub_por_ano.to_excel(writer, sheet_name='Publicações por Ano', index=False)
    top10_areas.to_frame('Quantidade').to_excel(writer, sheet_name='Top 10 Áreas')
    top10_inst.to_frame('Quantidade').to_excel(writer, sheet_name='Top 10 Instituições')
    foco_counts.to_frame('Quantidade').to_excel(writer, sheet_name='Foco em IA')
    outras_areas.to_frame('Quantidade').to_excel(writer, sheet_name='Outras Áreas')
    termos_df = pd.DataFrame(top_termos, columns=['Termo', 'Frequência'])
    termos_df.to_excel(writer, sheet_name='Top Termos', index=False)
    df.to_excel(writer, sheet_name='Dataset Completo', index=False)

print(f"✓ Resultados salvos: {output_excel}")

# =============================================================================
# 12. RELATÓRIO FINAL
# =============================================================================
print("\n" + "="*80)
print("RELATÓRIO FINAL - INSIGHTS PRINCIPAIS")
print("="*80)

print(f"""
📊 RESUMO EXECUTIVO:

1. VOLUME E CRESCIMENTO:
   • Total de {len(df)} teses/dissertações analisadas
   • Período: {int(df['ano_defesa'].min())} a {int(df['ano_defesa'].max())}
   • Crescimento: {crescimento:.0f}% (primeiro ao último ano)
   • Concentração últimos 3 anos: {anos_recentes/len(df)*100:.1f}%
   • Pico: {int(pub_por_ano.iloc[-1]['ano_defesa'])} com {int(pub_por_ano.iloc[-1]['quantidade'])} publicações

2. FOCO EM INTELIGÊNCIA ARTIFICIAL:
   • IA como foco central: {foco_counts.get('IA - Foco Central', 0)} ({foco_counts.get('IA - Foco Central', 0)/len(df)*100:.1f}%)
   • IA como tema relacionado: {foco_counts.get('IA - Foco Relacionado', 0)} ({foco_counts.get('IA - Foco Relacionado', 0)/len(df)*100:.1f}%)
   • Outros temas: {foco_counts.get('Outros Temas', 0)} ({foco_counts.get('Outros Temas', 0)/len(df)*100:.1f}%)

3. NÍVEL ACADÊMICO:
   • Mestrados: {nivel_counts.get('Mestrado', 0)} ({nivel_counts.get('Mestrado', 0)/len(df)*100:.1f}%)
   • Doutorados: {nivel_counts.get('Doutorado', 0)} ({nivel_counts.get('Doutorado', 0)/len(df)*100:.1f}%)
   • Razão M/D: {nivel_counts.get('Mestrado', 0)/nivel_counts.get('Doutorado', 1):.2f}

4. ÁREAS DOMINANTES:
   • Top 1: {top10_areas.index[0]} ({top10_areas.iloc[0]} trabalhos)
   • Top 2: {top10_areas.index[1]} ({top10_areas.iloc[1]} trabalhos)
   • Top 3: {top10_areas.index[2]} ({top10_areas.iloc[2]} trabalhos)
   • Top 10 representa: {top10_areas.sum()/len(df)*100:.1f}% do total
   • Outras áreas: {len(outras_areas)} diferentes ({outras_areas.sum()} trabalhos)

5. INSTITUIÇÕES LÍDERES:
   • Top 1: {top10_inst.index[0]} ({top10_inst.iloc[0]} trabalhos)
   • Top 2: {top10_inst.index[1]} ({top10_inst.iloc[1]} trabalhos)
   • Top 3: {top10_inst.index[2]} ({top10_inst.iloc[2]} trabalhos)
   • Total de instituições: {len(inst_counts)}
   • Top 10 representa: {top10_inst.sum()/len(df)*100:.1f}% do total

6. TIPO DE INSTITUIÇÃO (CORRIGIDO):
   • Federal: {tipo_counts.get('Federal', 0)} ({tipo_counts.get('Federal', 0)/len(df)*100:.1f}%)
   • Estadual: {tipo_counts.get('Estadual', 0)} ({tipo_counts.get('Estadual', 0)/len(df)*100:.1f}%)
   • Particular/Comunitária: {tipo_counts.get('Particular/Comunitária', 0)} ({tipo_counts.get('Particular/Comunitária', 0)/len(df)*100:.1f}%)
   • Confessional: {tipo_counts.get('Confessional', 0)} ({tipo_counts.get('Confessional', 0)/len(df)*100:.1f}%)
   • Setor Público Total: {tipo_counts.get('Federal', 0) + tipo_counts.get('Estadual', 0)} ({(tipo_counts.get('Federal', 0) + tipo_counts.get('Estadual', 0))/len(df)*100:.1f}%)

7. CARACTERÍSTICAS METODOLÓGICAS:
   • Média de páginas (Mestrado): {df[df['nivel']=='Mestrado']['num_paginas'].mean():.0f}
   • Média de páginas (Doutorado): {df[df['nivel']=='Doutorado']['num_paginas'].mean():.0f}
   • Mediana geral: {df['num_paginas'].median():.0f} páginas
""")

print("="*80)
print("ANÁLISE CONCLUÍDA COM SUCESSO!")
print("="*80)
