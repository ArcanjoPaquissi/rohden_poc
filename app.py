# -*- coding: utf-8 -*-
import os
from flask import Flask, render_template
import pandas as pd
import plotly.express as px

app = Flask(__name__)

@app.route('/')
def dashboard():
    df = pd.read_csv('data/obras.csv', encoding='utf-8')
    fig = px.bar(df, x='Região', y='Obras', title='Obras mapeadas por região',
                 color='Região', text='Obras')
    fig.update_traces(textposition='outside')
    fig.update_layout(
        plot_bgcolor='#0f172a',
        paper_bgcolor='#0f172a',
        font=dict(color='white', size=14),
        title_font=dict(size=20, color='#22d3ee')
    )
    graph_html = fig.to_html(full_html=False)
    return render_template('dashboard.html', graph=graph_html)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
