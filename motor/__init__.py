"""Motor determinístico da Revista Diária (sem LLM).

Submódulos:
- config:      lê editorias/editorias.yaml (as editorias como dados).
- curriculo:   cursor + syllabus → a aula do dia; avança o cursor.
- diagramador: encaixa as matérias nos slots do template e grava a edição.
- qa:          lint estrutural antes de publicar.
"""
