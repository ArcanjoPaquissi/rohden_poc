# -*- coding: utf-8 -*-
from flask import Flask, render_template
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

app = Flask(__name__)

# Configurações do Flask
app.config['DEBUG'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Dados simulados para a POC
dados_obras = {
    'Região': ['Sul', 'Sudeste', 'Centro-Oeste', 'Nordeste', 'Norte'],
    'Obras': [145, 89, 45, 32, 18],
    'Potencial_Receita': [12.5, 8.2, 4.1, 2.8, 1.6]
}

dados_comparativo = {
    'Período': ['Antes da POC\n(Método Tradicional)', 'Após POC\n(Plataforma Digital)'],
    'Obras_Identificadas': [18, 52],
    'Taxa_Conversao': [15, 38],
    'Tempo_Prospecção_dias': [45, 12]
}

dados_timeline = {
    'Fase': ['Planejamento', 'Desenvolvimento', 'Testes', 'Validação', 'Decisão'],
    'Duração_dias': [30, 60, 45, 30, 15],
    'Status': ['Concluído', 'Concluído', 'Em andamento', 'Aguardando', 'Aguardando']
}

@app.route('/')
def home():
    try:
        return render_template('home.html')
    except Exception as e:
        return f"Erro ao carregar home.html: {str(e)}", 500

@app.route('/como-funciona')
def como_funciona():
    try:
        return render_template('como_funciona.html')
    except Exception as e:
        return f"Erro ao carregar como_funciona.html: {str(e)}", 500

@app.route('/dashboard')
def dashboard():
    try:
        df = pd.DataFrame(dados_obras)
        
        fig1 = px.bar(df, x='Região', y='Obras',
                      title='Obras Identificadas por Região (Fase POC)',
                      color='Região', text='Obras')
        fig1.update_traces(textposition='outside')
        fig1.update_layout(
            plot_bgcolor='#0f172a',
            paper_bgcolor='#0f172a',
            font=dict(color='white', size=14),
            title_font=dict(size=20, color='#22d3ee'),
            showlegend=False
        )
        
        fig2 = px.pie(df, values='Potencial_Receita', names='Região',
                      title='Potencial de Receita por Região (R$ milhões)')
        fig2.update_layout(
            plot_bgcolor='#0f172a',
            paper_bgcolor='#0f172a',
            font=dict(color='white', size=14),
            title_font=dict(size=20, color='#22d3ee')
        )
        
        graph1_html = fig1.to_html(full_html=False)
        graph2_html = fig2.to_html(full_html=False)
        
        return render_template('dashboard.html', 
                             graph1=graph1_html, 
                             graph2=graph2_html,
                             total_obras=df['Obras'].sum(),
                             receita_potencial=df['Potencial_Receita'].sum())
    except Exception as e:
        return f"Erro no dashboard: {str(e)}", 500

@app.route('/comparativo')
def comparativo():
    try:
        df = pd.DataFrame(dados_comparativo)
        
        fig1 = px.bar(df, x='Período', y='Obras_Identificadas',
                      title='Comparativo: Obras Identificadas por Trimestre',
                      text='Obras_Identificadas',
                      color='Período')
        fig1.update_traces(textposition='outside')
        fig1.update_layout(
            plot_bgcolor='#0f172a',
            paper_bgcolor='#0f172a',
            font=dict(color='white', size=14),
            title_font=dict(size=18, color='#22d3ee'),
            showlegend=False
        )
        
        fig2 = px.bar(df, x='Período', y='Taxa_Conversao',
                      title='Taxa de Conversão (%)',
                      text='Taxa_Conversao',
                      color='Período')
        fig2.update_traces(textposition='outside')
        fig2.update_layout(
            plot_bgcolor='#0f172a',
            paper_bgcolor='#0f172a',
            font=dict(color='white', size=14),
            title_font=dict(size=18, color='#22d3ee'),
            showlegend=False
        )
        
        fig3 = px.bar(df, x='Período', y='Tempo_Prospecção_dias',
                      title='Tempo Médio de Prospecção (dias)',
                      text='Tempo_Prospecção_dias',
                      color='Período')
        fig3.update_traces(textposition='outside')
        fig3.update_layout(
            plot_bgcolor='#0f172a',
            paper_bgcolor='#0f172a',
            font=dict(color='white', size=14),
            title_font=dict(size=18, color='#22d3ee'),
            showlegend=False
        )
        
        graph1_html = fig1.to_html(full_html=False)
        graph2_html = fig2.to_html(full_html=False)
        graph3_html = fig3.to_html(full_html=False)
        
        melhoria_obras = ((52 - 18) / 18) * 100
        melhoria_conversao = ((38 - 15) / 15) * 100
        melhoria_tempo = ((45 - 12) / 45) * 100
        
        return render_template('comparativo.html',
                             graph1=graph1_html,
                             graph2=graph2_html,
                             graph3=graph3_html,
                             melhoria_obras=round(melhoria_obras, 1),
                             melhoria_conversao=round(melhoria_conversao, 1),
                             melhoria_tempo=round(melhoria_tempo, 1))
    except Exception as e:
        return f"Erro no comparativo: {str(e)}", 500

@app.route('/metodologia')
def metodologia():
    try:
        df = pd.DataFrame(dados_timeline)
        
        fig = go.Figure()
        
        cores = {'Concluído': '#10b981', 'Em andamento': '#f59e0b', 'Aguardando': '#6b7280'}
        
        for i, row in df.iterrows():
            fig.add_trace(go.Bar(
                y=[row['Fase']],
                x=[row['Duração_dias']],
                orientation='h',
                name=row['Status'],
                marker=dict(color=cores[row['Status']]),
                text=f"{row['Duração_dias']} dias",
                textposition='inside',
                showlegend=i == 0 or row['Status'] != df.iloc[i-1]['Status']
            ))
        
        fig.update_layout(
            title='Timeline da POC - Fases e Prazos',
            xaxis_title='Duração (dias)',
            yaxis_title='',
            barmode='stack',
            plot_bgcolor='#0f172a',
            paper_bgcolor='#0f172a',
            font=dict(color='white', size=14),
            title_font=dict(size=20, color='#22d3ee'),
            height=400
        )
        
        graph_html = fig.to_html(full_html=False)
        
        return render_template('metodologia.html', graph=graph_html)
    except Exception as e:
        return f"Erro na metodologia: {str(e)}", 500

@app.route('/custos')
def custos():
    try:
        categorias = ['Desenvolvimento\nTecnológico', 'Treinamento\nde Equipes', 
                      'Infraestrutura\nDigital', 'Consultoria\nRegulatória']
        valores = [280, 120, 180, 170]
        
        fig = px.bar(x=categorias, y=valores,
                     title='Distribuição de Custos da POC (em R$ mil)',
                     text=valores,
                     color=categorias)
        fig.update_traces(texttemplate='R$ %{text}k', textposition='outside')
        fig.update_layout(
            plot_bgcolor='#0f172a',
            paper_bgcolor='#0f172a',
            font=dict(color='white', size=14),
            title_font=dict(size=20, color='#22d3ee'),
            showlegend=False,
            xaxis_title='',
            yaxis_title='Custo (R$ mil)'
        )
        
        graph_html = fig.to_html(full_html=False)
        
        return render_template('custos.html', 
                             graph=graph_html,
                             custo_total=sum(valores),
                             roi_estimado=245)
    except Exception as e:
        return f"Erro nos custos: {str(e)}", 500

@app.route('/decisao')
def decisao():
    try:
        return render_template('decisao.html')
    except Exception as e:
        return f"Erro na decisão: {str(e)}", 500

@app.errorhandler(404)
def page_not_found(e):
    return """
    <h1>Página não encontrada (404)</h1>
    <p>A página que você procura não existe.</p>
    <a href="/">Voltar para página inicial</a>
    """, 404

@app.errorhandler(500)
def internal_error(e):
    return f"""
    <h1>Erro interno do servidor (500)</h1>
    <p>Detalhes: {str(e)}</p>
    <a href="/">Voltar para página inicial</a>
    """, 500

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 POC ROHDEN - SERVIDOR INICIANDO")
    print("=" * 60)
    print("📍 Acesse: http://localhost:5000")
    print("📍 Ou: http://127.0.0.1:5000")
    print("=" * 60)
    print("\n✅ Rotas disponíveis:")
    print("   / (Home)")
    print("   /como-funciona")
    print("   /dashboard")
    print("   /comparativo")
    print("   /metodologia")
    print("   /custos")
    print("   /decisao")
    print("\n⚠️  Pressione CTRL+C para parar o servidor\n")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)